#!/usr/bin/env python3
"""Execute a qualified two- or three-factor ANOVA and save an auditable result."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

from inspect_data import load_table


def native(value: Any) -> Any:
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    raise TypeError(type(value).__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path); parser.add_argument("--sheet")
    parser.add_argument("--outcome", required=True); parser.add_argument("--factors", required=True, help="exactly two or three comma-separated categorical factor fields")
    parser.add_argument("--eligibility", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sum-of-squares", choices=["II", "III"], default="II")
    args = parser.parse_args()
    factors = [name.strip() for name in args.factors.split(",") if name.strip()]
    if len(factors) not in {2, 3}:
        parser.error("--factors must name exactly two or three fields")
    expected = f"{'two' if len(factors) == 2 else 'three'}-way-anova"
    packet = json.loads(args.eligibility.read_text(encoding="utf-8"))
    approved = {item.get("method_id") for item in packet.get("recommendations", [])}
    if packet.get("status") != "eligible" or expected not in approved:
        raise ValueError(f"eligibility must be status eligible with method_id {expected}")
    frame = load_table(args.data, args.sheet)
    missing = [name for name in [args.outcome, *factors] if name not in frame.columns]
    if missing:
        raise ValueError(f"unknown columns: {missing}")
    subset = frame[[args.outcome, *factors]].dropna().copy()
    if not pd.api.types.is_numeric_dtype(subset[args.outcome]):
        raise ValueError("outcome must be numeric")
    for factor in factors:
        # Patsy does not yet accept pandas' nullable StringDtype in all supported
        # combinations; an object Series keeps categorical levels intact.
        subset[factor] = pd.Series(subset[factor].astype(str).to_numpy(dtype=object), index=subset.index, dtype=object)
    cells = subset.groupby(factors, observed=True).size()
    if cells.empty or cells.min() < 3 or len(cells) != int(np.prod([subset[factor].nunique() for factor in factors])):
        raise ValueError("requires complete factorial cells with at least three observations per cell")
    formula = f"Q('{args.outcome}') ~ " + " * ".join(f"C(Q('{factor}'))" for factor in factors)
    model = ols(formula, data=subset).fit()
    table = anova_lm(model, typ=2 if args.sum_of_squares == "II" else 3)
    residuals = model.resid
    shapiro = stats.shapiro(residuals) if len(residuals) <= 5000 else None
    grouped = [part[args.outcome].to_numpy() for _, part in subset.groupby(factors, observed=True)]
    levene = stats.levene(*grouped, center="median")
    total_ss = float(table["sum_sq"].sum())
    rows = []
    for term, row in table.iterrows():
        record = {"term": str(term), "sum_sq": float(row["sum_sq"]), "df": float(row["df"])}
        if pd.notna(row.get("F")): record["F"] = float(row["F"])
        if pd.notna(row.get("PR(>F)")): record["p_value"] = float(row["PR(>F)"])
        if term != "Residual": record["eta_squared"] = float(row["sum_sq"] / total_ss) if total_ss else None
        rows.append(record)
    report = {"status": "completed-factorial-anova", "method_id": expected, "source": str(args.data.resolve()), "outcome": args.outcome, "factors": factors, "formula": formula, "rows_used": len(subset), "minimum_cell_n": int(cells.min()), "sum_of_squares_type": args.sum_of_squares, "anova": rows, "diagnostics": {"residual_shapiro": None if shapiro is None else {"statistic": float(shapiro.statistic), "p_value": float(shapiro.pvalue)}, "levene_median": {"statistic": float(levene.statistic), "p_value": float(levene.pvalue)}}, "boundary": "This computes a factorial ANOVA after qualification. Interpret effects only with the pre-specified design, residual diagnostics, cell independence and multiplicity plan; it does not establish causality."}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=native), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, default=native))


if __name__ == "__main__":
    main()
