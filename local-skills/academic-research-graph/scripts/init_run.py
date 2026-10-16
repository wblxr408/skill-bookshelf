#!/usr/bin/env python3
"""Initialize a revisioned Academic Research Graph run directory."""
from __future__ import annotations

import argparse
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")
    return cleaned or "research-graph"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="Run directory name")
    parser.add_argument("--out", default="runs", help="Parent output directory")
    parser.add_argument("--focus", default="", help="Focal research question")
    parser.add_argument("--language", choices=["zh-CN", "en", "bilingual"], default="zh-CN")
    args = parser.parse_args()

    run_dir = Path(args.out) / args.name
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "assets").mkdir(exist_ok=True)
    (run_dir / "history").mkdir(exist_ok=True)
    (run_dir / "expansions").mkdir(exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    graph_id = f"arg:{slug(args.name)}:{uuid.uuid4().hex[:10]}"
    graph = {
        "meta": {
            "graph_id": graph_id,
            "revision": 1,
            "parent_revision": None,
            "title": args.name.replace("-", " ").title(),
            "focus": args.focus,
            "output_language": args.language,
            "generated_at": now,
            "search_cutoff": now[:10],
            "sources": [],
            "coverage": {},
            "terminology_glossary": {},
            "summary_policy": {
                "audience": "field_familiar_unread",
                "exposition_depth": "explanatory",
                "explain_background": True,
                "define_paper_specific_terms": True,
                "expand_acronyms_on_first_use": True,
                "name_comparison_baselines": True,
                "require_limitations_and_scope": True,
            },
            "figure_policy": {
                "enabled": True,
                "selection_mode": "selective",
                "max_per_paper": 1,
                "prefer_kinds": ["method_overview", "architecture", "pipeline", "conceptual_diagram", "qualitative_result"],
                "require_source_attribution": True,
                "require_alt_text": True,
                "embed_local_assets": True,
                "allow_remote_images": False,
                "max_embedded_bytes": 2500000,
                "max_display_width_px": 1600,
            },
            "expansion_history": [],
            "warnings": ["Research has not been populated yet."],
        },
        "nodes": [],
        "edges": [],
        "conflicts": [],
        "clusters": [],
        "expansions": [],
    }
    (run_dir / "graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    manifest = {
        "run_name": args.name,
        "graph_id": graph_id,
        "revision": 1,
        "created_at": now,
        "focus": args.focus,
        "output_language": args.language,
        "summary_policy": graph["meta"]["summary_policy"],
        "status": "initialized",
        "retrievals": [],
        "warnings": [],
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    for name in ["candidate_ledger.jsonl", "papers.jsonl", "evidence.jsonl"]:
        (run_dir / name).touch()
    heading = "核心问题" if args.language != "en" else "Focal question"
    (run_dir / "research_report.md").write_text(
        f"# {graph['meta']['title']}\n\n**{heading}:** {args.focus}\n\n"
        f"**Graph revision:** 1\n",
        encoding="utf-8",
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
