#!/usr/bin/env python3
"""Query a compact tier of the visual-reference catalogue without loading it into prompt context."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from chart_support import support_status


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "assets" / "reference-catalogue.yaml"


def source_ids(names: list[str]) -> dict[str, str]:
    """Use stable short source IDs in normal responses; expose paths only on demand."""
    corpus = ROOT.parent / "figures"
    all_names = sorted(path.name for path in corpus.glob("*.png"))
    return {name: f"src-{all_names.index(name) + 1:02d}" for name in names}


def normalise(value: str) -> str:
    return "".join(ch for ch in value.casefold() if ch.isalnum())


def all_types(categories: list[dict]) -> list[tuple[dict, dict, dict]]:
    return [(category, subcategory, variant)
            for category in categories
            for subcategory in category["subcategories"]
            for variant in subcategory["variants"]]


def compact_record(category: dict, subcategory: dict, variant: dict) -> dict:
    return {
        "id": variant["id"],
        "label": variant["label"],
        "family": f"{category['id']}/{subcategory['id']}",
        "status": support_status(variant["id"]),
        "catalogue_status": variant.get("status", "catalogued"),
        "evidence": list(source_ids(subcategory["sources"]).values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--categories", action="store_true", help="List only tier-1 families.")
    group.add_argument("--category", help="List minor families in one tier-1 family.")
    group.add_argument("--type-id", help="Return one exact chart type.")
    group.add_argument("--search", help="Return compact title/ID matches for a user phrase.")
    group.add_argument("--source-id", help="Return the original screenshot path for one source ID.")
    parser.add_argument("--detail", action="store_true", help="Attach grammar, data contract, and original source names to --type-id.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum candidates for --search (default: 5).")
    args = parser.parse_args()
    catalogue = yaml.safe_load(CATALOGUE.read_text(encoding="utf-8"))
    categories = catalogue["categories"]
    if args.categories:
        result = [{"id": item["id"], "label": item["label"]} for item in categories]
    elif args.category:
        category = next((item for item in categories if item["id"] == args.category), None)
        if category is None:
            raise SystemExit(f"Unknown category: {args.category}")
        result = {"id": category["id"], "label": category["label"], "subcategories": [
            {"id": sub["id"], "label": sub["label"], "type_count": len(sub["variants"])}
            for sub in category["subcategories"]
        ]}
    elif args.search:
        needle = normalise(args.search)
        candidates = []
        for category, subcategory, variant in all_types(categories):
            haystack = normalise(f"{variant['id']} {variant['label']} {category['label']} {subcategory['label']}")
            if needle and needle in haystack:
                candidates.append(compact_record(category, subcategory, variant))
        result = {"query": args.search, "candidate_count": len(candidates), "candidates": candidates[:args.limit]}
    elif args.source_id:
        corpus = ROOT.parent / "figures"
        screenshots = sorted(corpus.glob("*.png"))
        try:
            position = int(args.source_id.removeprefix("src-")) - 1
            source = screenshots[position]
        except (ValueError, IndexError):
            raise SystemExit(f"Unknown source-id: {args.source_id}")
        result = {"id": args.source_id, "path": str(source), "exists": source.exists()}
    else:
        found = next(((category, subcategory, variant) for category, subcategory, variant in all_types(categories)
                      if variant["id"] == args.type_id), None)
        if found is None:
            raise SystemExit(f"Unknown type-id: {args.type_id}")
        category, subcategory, variant = found
        result = compact_record(category, subcategory, variant)
        if args.detail:
            result["visual_grammar"] = subcategory["grammar"]
            result["data_shape"] = subcategory["data_shape"]
            result["observed_source_images"] = subcategory["sources"]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
