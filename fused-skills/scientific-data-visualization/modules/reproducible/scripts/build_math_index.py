#!/usr/bin/env python3
"""Build a compact line index for method-name retrieval and verify math-image coverage."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "assets" / "math-method-catalogue.yaml"
INDEX = ROOT / "assets" / "math-method-index.jsonl"

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    catalogue = yaml.safe_load(CATALOGUE.read_text(encoding="utf-8"))
    rows, sources = [], set()
    for category in catalogue["categories"]:
        sources.add(category["source"])
        for method in category["methods"]:
            rows.append({"id": method["id"], "label": method["label"], "category": category["id"], "role": method["role"], "data_shape": method["data_shape"], "chart_expression": method["chart_expression"]})
    source_dir = (CATALOGUE.parent / catalogue["source_corpus"]["directory"]).resolve()
    actual = {path.name for path in source_dir.glob("*.png")}
    report = {"methods": len(rows), "source_images": len(actual), "unmapped_images": sorted(actual-sources), "missing_images": sorted(sources-actual)}
    if report["unmapped_images"] or report["missing_images"]: raise SystemExit(json.dumps(report, ensure_ascii=False))
    if not args.check:
        INDEX.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))+"\n" for row in rows), encoding="utf-8"); report["index"] = str(INDEX)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
