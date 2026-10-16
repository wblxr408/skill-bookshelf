#!/usr/bin/env python3
"""Rank JSONL candidate papers using transparent weighted features."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_WEIGHTS = {
    "focus_relevance": 0.30,
    "lineage_importance": 0.15,
    "bridge_centrality": 0.12,
    "methodological_novelty": 0.12,
    "conflict_likelihood": 0.10,
    "benchmark_or_repo_evidence": 0.08,
    "recency_frontier": 0.08,
    "evidence_quality": 0.05,
}


def clamp(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def score(record: dict[str, Any], weights: dict[str, float]) -> float:
    features = record.get("features", record)
    return round(sum(clamp(features.get(key, 0)) * weight for key, weight in weights.items()), 6)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at line {lineno}: {exc}") from exc
        if not isinstance(obj, dict):
            raise ValueError(f"Line {lineno} is not a JSON object")
        rows.append(obj)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--top", type=int, default=0, help="Keep only top N; 0 keeps all")
    args = parser.parse_args()

    rows = load_jsonl(args.input)
    for row in rows:
        row["priority_score"] = score(row, DEFAULT_WEIGHTS)
    rows.sort(key=lambda row: (row["priority_score"], row.get("year") or 0), reverse=True)
    if args.top > 0:
        rows = rows[: args.top]

    output = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + ("\n" if rows else "")
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
