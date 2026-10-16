#!/usr/bin/env python3
"""Fit PLS, discriminant, binary logistic, or ordinal models with held-out evaluation.

The command requires a matching qualification packet from
``recommend_statistics.py``.  It writes split provenance and real held-out
metrics; it does not turn a development result into a scientific claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.compose import TransformedTargetRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss, mean_absolute_error, mean_squared_error, r2_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler
from statsmodels.miscmodels.ordinal_model import OrderedModel

from inspect_data import load_table


def json_default(value: Any) -> Any:
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError(type(value).__name__)


class OrdinalLogit(BaseEstimator, ClassifierMixin):
    def fit(self, x: np.ndarray, y: np.ndarray) -> "OrdinalLogit":
        self.classes_ = np.asarray(sorted(pd.unique(y)))
        codes = np.asarray(pd.Categorical(y, categories=self.classes_, ordered=True).codes, dtype=int).reshape(-1)
        self.model_ = OrderedModel(codes, np.asarray(x), distr="logit")
        self.result_ = self.model_.fit(method="bfgs", disp=False, maxiter=300)
        return self

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        return np.asarray(self.model_.predict(self.result_.params, exog=np.asarray(x)))

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.classes_[self.predict_proba(x).argmax(axis=1)]


def read_eligibility(path: Path, expected_method: str) -> dict[str, Any]:
    packet = json.loads(path.read_text(encoding="utf-8"))
    actual = {item.get("method_id") for item in packet.get("recommendations", [])}
    accepted = {"eligible", "eligible-development"}
    if packet.get("status") not in accepted or expected_method not in actual:
        raise ValueError(f"eligibility packet must contain {expected_method} with an eligible status")
    return packet


def split_hash(indices: np.ndarray) -> str:
    return hashlib.sha256(",".join(map(str, sorted(map(int, indices)))).encode("utf-8")).hexdigest()


def probability_metrics(y: np.ndarray, proba: np.ndarray, classes: np.ndarray) -> dict[str, float]:
    result: dict[str, float] = {}
    if len(classes) == 2:
        positive = classes[1]
        binary = (y == positive).astype(int)
        result["roc_auc"] = float(roc_auc_score(binary, proba[:, 1]))
        result["brier"] = float(brier_score_loss(binary, proba[:, 1]))
        bins = []
        for lower, upper in zip(np.linspace(0, 1, 6)[:-1], np.linspace(0, 1, 6)[1:]):
            mask = (proba[:, 1] >= lower) & ((proba[:, 1] < upper) if upper < 1 else (proba[:, 1] <= upper))
            if mask.any():
                bins.append({"lower": float(lower), "upper": float(upper), "n": int(mask.sum()), "predicted_mean": float(proba[mask, 1].mean()), "observed_rate": float(binary[mask].mean())})
        result["calibration_bins"] = bins
    else:
        matrix = np.zeros_like(proba)
        for column, label in enumerate(classes):
            matrix[:, column] = (y == label).astype(int)
        result["multiclass_brier"] = float(np.mean(np.sum((proba - matrix) ** 2, axis=1)))
    return result


def classifier_metrics(y: np.ndarray, prediction: np.ndarray, proba: np.ndarray, classes: np.ndarray, ordinal: bool = False) -> dict[str, float]:
    result = {"accuracy": float(accuracy_score(y, prediction)), "balanced_accuracy": float(balanced_accuracy_score(y, prediction))}
    result.update(probability_metrics(y, proba, classes))
    if ordinal:
        lookup = {label: index for index, label in enumerate(classes)}
        result["ordinal_rank_mae"] = float(mean_absolute_error([lookup[v] for v in y], [lookup[v] for v in prediction]))
    return result


def bootstrap_metric_intervals(y: np.ndarray, prediction: np.ndarray, proba: np.ndarray | None, classes: np.ndarray | None, model: str, seed: int, repeats: int = 300) -> dict[str, dict[str, float]]:
    """Percentile intervals describe test-set sampling uncertainty, not population validity."""
    rng = np.random.default_rng(seed); values: dict[str, list[float]] = {}
    for _ in range(repeats):
        indices = rng.integers(0, len(y), len(y)); observed, predicted = y[indices], prediction[indices]
        if model == "pls":
            metrics = {"rmse": float(mean_squared_error(observed, predicted) ** 0.5), "r2": float(r2_score(observed, predicted))}
        else:
            metrics = {"accuracy": float(accuracy_score(observed, predicted)), "balanced_accuracy": float(balanced_accuracy_score(observed, predicted))}
            if proba is not None and classes is not None and len(classes) == 2 and len(np.unique(observed)) == 2:
                metrics["roc_auc"] = float(roc_auc_score((observed == classes[1]).astype(int), proba[indices, 1]))
        for key, value in metrics.items():
            if np.isfinite(value): values.setdefault(key, []).append(value)
    return {key: {"lower_2.5": float(np.quantile(values[key], .025)), "upper_97.5": float(np.quantile(values[key], .975)), "repeats": len(values[key])} for key in values}


def feature_effects(model: Any, predictors: list[str]) -> list[dict[str, Any]] | None:
    estimator = model.named_steps.get("model") if hasattr(model, "named_steps") else model
    coefficients = getattr(estimator, "coef_", None)
    if coefficients is None and hasattr(estimator, "result_"):
        coefficients = np.asarray(estimator.result_.params[:len(predictors)])
    if coefficients is None:
        return None
    values = np.asarray(coefficients)
    return [{"feature": feature, "coefficient": values[:, index].tolist() if values.ndim == 2 else float(values[index])} for index, feature in enumerate(predictors)]


def model_pipeline(kind: str, n_features: int, train_rows: int, discriminant_kind: str) -> tuple[Any, dict[str, list[Any]]]:
    base = [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    if kind == "logistic":
        return Pipeline(base + [("model", LogisticRegression(max_iter=2000, class_weight="balanced"))]), {"model__C": [0.05, 0.2, 1.0, 5.0]}
    if kind == "discriminant":
        if discriminant_kind == "qda":
            return Pipeline(base + [("model", QuadraticDiscriminantAnalysis())]), {"model__reg_param": [0.0, 0.05, 0.15, 0.3]}
        return Pipeline(base + [("model", LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))]), {}
    if kind == "pls":
        maximum = max(1, min(n_features, train_rows - 1, 10))
        return Pipeline(base + [("model", PLSRegression(scale=False, max_iter=1000))]), {"model__n_components": list(range(1, maximum + 1))}
    if kind == "ordinal":
        return Pipeline(base + [("model", OrdinalLogit())]), {}
    raise ValueError(kind)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path); parser.add_argument("--sheet")
    parser.add_argument("--model", required=True, choices=["logistic", "ordinal", "pls", "discriminant"])
    parser.add_argument("--outcome", required=True); parser.add_argument("--predictors", required=True, help="comma-separated numeric predictor columns")
    parser.add_argument("--eligibility", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--test-size", type=float, default=0.2); parser.add_argument("--random-state", type=int, default=20260815)
    parser.add_argument("--external-test", type=Path, help="optional untouched CSV/XLSX test source; when supplied, all source rows are used for training")
    parser.add_argument("--cv-folds", type=int, default=5); parser.add_argument("--discriminant-kind", choices=["lda", "qda"], default="lda")
    parser.add_argument("--model-output", type=Path, help="optional joblib path; defaults beside --output")
    parser.add_argument("--bootstrap-repeats", type=int, default=300)
    args = parser.parse_args()
    expected = {"logistic": "logistic-regression", "ordinal": "ordinal-regression", "pls": "pls", "discriminant": "discriminant-analysis"}[args.model]
    eligibility = read_eligibility(args.eligibility, expected)
    predictors = [value.strip() for value in args.predictors.split(",") if value.strip()]
    frame = load_table(args.data, args.sheet)
    missing = [name for name in [args.outcome, *predictors] if name not in frame.columns]
    if missing:
        raise ValueError(f"unknown columns: {missing}")
    subset = frame[[args.outcome, *predictors]].dropna().copy()
    if len(subset) < 20:
        raise ValueError("at least 20 complete rows are required for a held-out model evaluation")
    x, y = subset[predictors].to_numpy(), subset[args.outcome].to_numpy()
    external = None
    if args.external_test:
        external_frame = load_table(args.external_test, args.sheet)
        missing_external = [name for name in [args.outcome, *predictors] if name not in external_frame.columns]
        if missing_external:
            raise ValueError(f"unknown external-test columns: {missing_external}")
        external = external_frame[[args.outcome, *predictors]].dropna()
        if len(external) < 5:
            raise ValueError("external test source requires at least five complete rows")
    is_classifier = args.model in {"logistic", "ordinal", "discriminant"}
    if is_classifier:
        classes, counts = np.unique(y, return_counts=True)
        if len(classes) < 2 or counts.min() < 5:
            raise ValueError("classification requires at least two classes with five complete observations each")
        if external is not None:
            train_x, train_y = x, y
            test_x, test_y = external[predictors].to_numpy(), external[args.outcome].to_numpy()
            train_rows, test_rows = subset.index.to_numpy(), external.index.to_numpy()
        else:
            x_train, x_test, y_train, y_test, train_rows, test_rows = train_test_split(x, y, subset.index.to_numpy(), test_size=args.test_size, random_state=args.random_state, stratify=y)
            train_x, test_x, train_y, test_y = x_train, x_test, y_train, y_test
        folds = min(args.cv_folds, int(np.unique(train_y, return_counts=True)[1].min()))
        if folds < 2:
            raise ValueError("training split has too few examples per class for cross-validation")
        cv = StratifiedKFold(folds, shuffle=True, random_state=args.random_state)
    else:
        if np.unique(y).size < 3:
            raise ValueError("PLS outcome needs at least three distinct values")
        all_rows = subset.index.to_numpy()
        if external is not None:
            train_x, train_y = x, y
            test_x, test_y = external[predictors].to_numpy(), external[args.outcome].to_numpy()
            train_rows, test_rows = all_rows, external.index.to_numpy()
        else:
            train_x, test_x, train_y, test_y, train_rows, test_rows = train_test_split(x, y, all_rows, test_size=args.test_size, random_state=args.random_state)
        from sklearn.model_selection import KFold
        cv = KFold(min(args.cv_folds, len(train_y)), shuffle=True, random_state=args.random_state)
    estimator, grid = model_pipeline(args.model, len(predictors), len(train_y), args.discriminant_kind)
    if grid:
        scorer = "roc_auc" if args.model == "logistic" else ("neg_root_mean_squared_error" if args.model == "pls" else "balanced_accuracy")
        fitted: Any = GridSearchCV(estimator, grid, scoring=scorer, cv=cv, refit=True).fit(train_x, train_y)
        best = fitted.best_estimator_; selection = {"best_params": fitted.best_params_, "cv_score": float(fitted.best_score_), "scoring": scorer}
    else:
        best = estimator.fit(train_x, train_y); selection = {"best_params": {}, "cv_score": None, "scoring": None}
    prediction = best.predict(test_x)
    if args.model == "pls":
        prediction = np.asarray(prediction).reshape(-1)
        metrics = {"rmse": float(mean_squared_error(test_y, prediction) ** 0.5), "mae": float(mean_absolute_error(test_y, prediction)), "r2": float(r2_score(test_y, prediction))}
    else:
        proba = best.predict_proba(test_x)
        classes_for_metrics = np.asarray(best.classes_ if hasattr(best, "classes_") else best.named_steps["model"].classes_)
        metrics = classifier_metrics(test_y, prediction, proba, classes_for_metrics, ordinal=args.model == "ordinal")
        intervals = bootstrap_metric_intervals(test_y, prediction, proba, classes_for_metrics, args.model, args.random_state, args.bootstrap_repeats)
    if args.model == "pls":
        intervals = bootstrap_metric_intervals(test_y, prediction, None, None, args.model, args.random_state, args.bootstrap_repeats)
        classes_for_metrics = None
    model_path = args.model_output or args.output.with_suffix(".joblib")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best, model_path)
    report = {"status": "completed-external-evaluation" if external is not None else "completed-held-out-evaluation", "model": args.model, "method_id": expected, "eligibility_status": eligibility["status"], "source": str(args.data.resolve()), "external_test_source": str(args.external_test.resolve()) if external is not None else None, "outcome": args.outcome, "predictors": predictors, "rows_used": len(subset), "split_provenance": {"random_state": args.random_state, "test_size": None if external is not None else args.test_size, "train_rows": len(train_rows), "test_rows": len(test_rows), "train_position_sha256": split_hash(train_rows), "test_position_sha256": split_hash(test_rows)}, "selection": selection, "held_out_metrics": metrics, "bootstrap_intervals": intervals, "feature_effects": feature_effects(best, predictors), "serialized_model": str(model_path.resolve()), "boundary": "Metrics use an untouched hold-out or explicitly supplied external source. Bootstrap intervals quantify this evaluation sample only; calibration, external validity and decision thresholds remain separate concerns, not causal or deployment validation."}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, default=json_default))


if __name__ == "__main__":
    main()
