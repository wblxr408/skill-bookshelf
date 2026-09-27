#!/usr/bin/env python3
"""Profile a CSV/XLSX file before a chart decision; never changes the source data."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


def load_table(path: Path, sheet: str | int | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        if sheet is not None and str(sheet).isdigit():
            sheet = int(sheet)
        return pd.read_excel(path, sheet_name=sheet if sheet is not None else 0)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, encoding="utf-8-sig")
    raise ValueError("Only CSV, XLSX, and XLS inputs are supported.")


def infer_role(series: pd.Series, name: str) -> str:
    name_hint = str(name).casefold()
    if re.search(r"(^|[_\-\s])(id|identifier|subject|participant|patient)([_\-\s]|$)|编号|受试|个体", name_hint):
        return "identifier"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric_measurement"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    unique = series.nunique(dropna=True)
    if unique <= max(12, len(series) * 0.05):
        return "categorical_group"
    return "identifier_or_text"


def numeric_diagnostics(series: pd.Series) -> dict:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return {"valid_n": 0, "zero_variance": True, "shape_flags": ["no_valid_values"]}
    q1, median, q3 = (float(values.quantile(q)) for q in (0.25, 0.5, 0.75))
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = int(((values < lower) | (values > upper)).sum()) if iqr > 0 else 0
    skew = float(values.skew()) if len(values) >= 3 else None
    flags = []
    if len(values) < 8:
        flags.append("small_sample")
    if values.nunique() < 2:
        flags.append("zero_variance")
    if float((values == 0).mean()) >= 0.25:
        flags.append("substantial_zero_mass")
    if skew is not None and abs(skew) >= 1:
        flags.append("strong_skew")
    if outliers:
        flags.append("iqr_outliers_present")
    return {
        "valid_n": int(len(values)), "min": round(float(values.min()), 6), "max": round(float(values.max()), 6),
        "median": round(median, 6), "iqr": round(iqr, 6), "skew": None if skew is None else round(skew, 6),
        "zero_fraction": round(float((values == 0).mean()), 6), "outlier_count_iqr": outliers,
        "unique_fraction": round(float(values.nunique() / len(values)), 6), "zero_variance": values.nunique() < 2,
        "shape_flags": flags,
    }


def correlation_summary(df: pd.DataFrame, columns: list[str]) -> list[dict]:
    if len(columns) < 2:
        return []
    matrix = df[columns].corr(numeric_only=True)
    pairs = []
    for index, left in enumerate(columns):
        for right in columns[index + 1:]:
            value = matrix.loc[left, right]
            if pd.notna(value):
                pairs.append({"left": left, "right": right, "pearson_r": round(float(value), 6), "abs_r": round(abs(float(value)), 6)})
    return sorted(pairs, key=lambda pair: pair["abs_r"], reverse=True)[:10]


def profile(df: pd.DataFrame) -> dict:
    columns = []
    numeric_columns = []
    categorical_columns = []
    for name in df.columns:
        s = df[name]
        role = infer_role(s, str(name))
        item = {
            "name": str(name), "dtype": str(s.dtype), "inferred_role": role,
            "missing": int(s.isna().sum()), "missing_rate": round(float(s.isna().mean()), 4),
            "unique": int(s.nunique(dropna=True)),
        }
        if role == "numeric_measurement":
            numeric_columns.append(str(name))
            item["summary"] = {
                key: (None if pd.isna(value) else round(float(value), 6))
                for key, value in s.describe(percentiles=[0.25, 0.5, 0.75]).to_dict().items()
            }
        elif role == "categorical_group":
            categorical_columns.append(str(name))
            item["top_values"] = {str(k): int(v) for k, v in s.value_counts(dropna=False).head(10).items()}
        columns.append(item)

    group_sizes = {}
    for name in categorical_columns:
        counts = df[name].value_counts(dropna=False)
        group_sizes[name] = {str(k): int(v) for k, v in counts.items()}
    numeric_quality = {}
    for name in numeric_columns:
        numeric_quality[name] = numeric_diagnostics(df[name])

    candidates = []
    if len(numeric_columns) >= 2:
        candidates.append("scatter: examine relationship between two numeric variables")
        candidates.append("heatmap: inspect a numeric matrix or grouped condition grid")
    if numeric_columns and categorical_columns:
        candidates.extend([
            "box or violin: compare distributions across groups",
            "ecdf: compare complete distributions without binning",
            "pareto: rank categorical contributions when the numeric value is a count or burden",
        ])
    names = " ".join(str(column).casefold() for column in df.columns)
    ordered_hint = bool(re.search(r"time|date|year|month|时间|日期|年份|月份", names))
    if numeric_columns and ordered_hint:
        candidates.append("line or control: only after confirming an explicit ordered time/process column and sampling interval")
    warnings = [
        "Field roles are inferred. Confirm units, experimental unit, grouping variable, pairing, and time ordering before charting.",
        "Candidate charts are visual candidates, not statistical recommendations or evidence of significance.",
    ]
    for name, sizes in group_sizes.items():
        if sizes and min(sizes.values()) < 3:
            warnings.append(f"Grouping column '{name}' contains a group with fewer than three rows; distribution summaries are blocked by the renderer.")
        elif sizes and min(sizes.values()) < 10:
            warnings.append(f"Grouping column '{name}' has small groups (minimum n={min(sizes.values())}); show individual observations and avoid mean-only bars.")
    for name, quality in numeric_quality.items():
        if quality["zero_variance"]:
            warnings.append(f"Numeric field '{name}' has zero variance; association, regression, and many inferential methods are unsuitable.")
    return {
        "rows": int(len(df)), "columns": int(len(df.columns)), "duplicate_rows": int(df.duplicated().sum()),
        "fields": columns, "group_sizes": group_sizes, "numeric_quality": numeric_quality,
        "correlation_summary": correlation_summary(df, numeric_columns),
        "semantic_hints": {
            "has_time_hint": ordered_hint,
            "has_subject_id_hint": bool(re.search(r"subject|participant|patient|受试|个体|样本.*id", names)),
            "has_geo_hint": bool(re.search(r"lat|lon|latitude|longitude|经度|纬度|省|市|国家|region", names)),
            "has_survival_hint": bool(re.search(r"event|status|censor|事件|结局", names) and re.search(r"time|duration|日期|时间", names)),
        },
        "candidate_chart_families": candidates, "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--sheet", help="XLSX sheet name or zero-based index")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    table = load_table(args.input, args.sheet)
    report = profile(table)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
