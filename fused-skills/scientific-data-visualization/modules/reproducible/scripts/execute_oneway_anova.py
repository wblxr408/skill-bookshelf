#!/usr/bin/env python3
"""Execute qualified one-way ANOVA with Welch and Holm-adjusted pairwise contrasts."""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.oneway import anova_oneway

from inspect_data import load_table


def holm(p_values: list[float]) -> list[float]:
    order = np.argsort(p_values); adjusted = np.empty(len(p_values), dtype=float); running = 0.0
    for rank, index in enumerate(order):
        value = min(1.0, (len(p_values) - rank) * p_values[index])
        running = max(running, value); adjusted[index] = running
    return adjusted.tolist()


def native(value: Any) -> Any:
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    raise TypeError(type(value).__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path); parser.add_argument("--sheet"); parser.add_argument("--outcome", required=True); parser.add_argument("--group", required=True)
    parser.add_argument("--eligibility", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--variance", choices=["equal", "unequal"], default="equal")
    args = parser.parse_args()
    packet = json.loads(args.eligibility.read_text(encoding="utf-8"))
    if packet.get("status") != "eligible" or "one-way-anova" not in {item.get("method_id") for item in packet.get("recommendations", [])}:
        raise ValueError("eligibility must contain an eligible one-way-anova recommendation")
    frame = load_table(args.data, args.sheet)
    subset = frame[[args.outcome, args.group]].replace([np.inf, -np.inf], np.nan).dropna()
    if not pd.api.types.is_numeric_dtype(subset[args.outcome]) or subset[args.group].nunique() < 3:
        raise ValueError("one-way ANOVA requires a numeric outcome and at least three groups")
    groups = [values.to_numpy(dtype=float) for _, values in subset.groupby(args.group, observed=True)[args.outcome]]
    if min(map(len, groups)) < 3:
        raise ValueError("every group requires at least three observations")
    if args.variance == "unequal":
        omnibus = anova_oneway(np.concatenate(groups), np.concatenate([[index] * len(values) for index, values in enumerate(groups)]), use_var="unequal")
        statistic, p_value, method = float(omnibus.statistic), float(omnibus.pvalue), "Welch ANOVA"
    else:
        omnibus_result = stats.f_oneway(*groups); statistic, p_value, method = float(omnibus_result.statistic), float(omnibus_result.pvalue), "one-way ANOVA"
    labels = list(subset[args.group].drop_duplicates())
    contrasts = []
    raw = []
    for (left, right), (left_values, right_values) in zip(combinations(labels, 2), combinations(groups, 2)):
        result = stats.ttest_ind(left_values, right_values, equal_var=args.variance == "equal")
        raw.append(float(result.pvalue)); contrasts.append({"group_a": str(left), "group_b": str(right), "mean_difference": float(np.mean(left_values) - np.mean(right_values)), "t": float(result.statistic)})
    for index, (item, adjusted) in enumerate(zip(contrasts, holm(raw))):
        item["p_value_raw"] = raw[index]; item["p_value_holm"] = adjusted
    report = {"status": "completed-oneway-anova", "method_id": "one-way-anova", "variant": method, "source": str(args.data.resolve()), "outcome": args.outcome, "group": args.group, "rows_used": len(subset), "omnibus": {"statistic": statistic, "p_value": p_value, "method": method}, "pairwise": {"method": "Welch pairwise t" if args.variance == "unequal" else "pooled pairwise t", "multiplicity": "Holm", "contrasts": contrasts}, "boundary": "Pairwise contrasts are exploratory unless the design, estimand, multiplicity plan and assumptions were pre-specified; this artifact does not establish causality."}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=native), encoding="utf-8"); print(json.dumps(report, ensure_ascii=False, indent=2, default=native))


if __name__ == "__main__":
    main()
