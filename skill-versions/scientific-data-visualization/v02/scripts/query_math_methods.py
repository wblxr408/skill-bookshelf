#!/usr/bin/env python3
"""Search method names without exposing formulas; formulas require --confirmed and a sidecar file."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]; CATALOGUE = ROOT / "assets" / "math-method-catalogue.yaml"; INDEX = ROOT / "assets" / "math-method-index.jsonl"
AUTO_GATED = {
    "two-sample-t", "one-way-anova", "one-way-repeated-anova", "two-way-anova", "three-way-anova", "mann-whitney", "kruskal-wallis", "paired-t", "paired-wilcoxon",
    "friedman", "two-sample-proportion", "logistic-regression", "ordinal-regression", "pearson-correlation", "kaplan-meier", "power-two-sample-t",
    "power-paired-t", "power-two-proportion", "kmeans", "hierarchical-clustering", "partial-correlation", "cox-model", "multiple-linear-regression", "pls", "discriminant-analysis",
}
AI_CONDITIONAL = {
    "column-statistics", "row-statistics", "statistical-table", "crosstab-chi-square", "discrete-frequency",
    "frequency-distribution", "binomial-distribution", "normality-test", "grubbs-outlier", "dixon-q",
    "one-sample-z", "one-sample-variance", "two-sample-variance", "one-sample-proportion",
    "two-way-repeated-anova", "one-sample-wilcoxon", "paired-sign", "two-sample-ks", "mood-median",
    "pca", "weibull-fit", "power-one-proportion", "power-one-sample-t", "power-one-way-anova",
}

def recommendation_status(method_id: str) -> str:
    if method_id in AUTO_GATED:
        return "requires matching eligible packet from recommend_statistics.py; catalogue entry alone is not a recommendation"
    if method_id in AI_CONDITIONAL:
        return "AI may present this as a conditional candidate only; see ai-recommendation-protocol.md for required facts and exclusions"
    return "catalogue-only; no strict automatic recommendation adapter is implemented"

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--categories", action="store_true"); group.add_argument("--search"); group.add_argument("--method-id")
    parser.add_argument("--confirmed", action="store_true"); parser.add_argument("--include-formula", action="store_true"); parser.add_argument("--limit", type=int, default=5); args = parser.parse_args()
    catalogue = yaml.safe_load(CATALOGUE.read_text(encoding="utf-8")); rows = [json.loads(line) for line in INDEX.read_text(encoding="utf-8").splitlines()]
    if args.categories: result = [{"id": c["id"], "label": c["label"], "method_count": len(c["methods"]), "recommendation_boundary": "catalogue entries are not automatic recommendations"} for c in catalogue["categories"]]
    elif args.search:
        query = args.search.casefold(); matches = [r for r in rows if query in f"{r['id']} {r['label']} {r['role']} {r['data_shape']}".casefold()]
        result = {"query": args.search, "matches": [{"id": r["id"], "label": r["label"], "category": r["category"], "role": r["role"], "data_shape": r["data_shape"], "recommendation_status": recommendation_status(r["id"])} for r in matches[:args.limit]]}
    else:
        row = next((r for r in rows if r["id"] == args.method_id), None)
        if row is None: raise SystemExit(f"Unknown method-id: {args.method_id}")
        result = {key: row[key] for key in ("id", "label", "category", "role", "data_shape", "chart_expression")}
        result["recommendation_status"] = recommendation_status(row["id"])
        if args.include_formula and not args.confirmed:
            raise SystemExit("--include-formula requires --confirmed")
        if args.confirmed and args.include_formula:
            formula = ROOT / "assets" / "math-formulas" / f"{row['id']}.md"
            result["formula_context"] = formula.read_text(encoding="utf-8") if formula.exists() else "not catalogued; do not invent a formula"
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == "__main__": main()
