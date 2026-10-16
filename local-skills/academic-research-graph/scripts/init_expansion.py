#!/usr/bin/env python3
"""Create a node-centered expansion workspace and patch skeleton."""
from __future__ import annotations

import argparse
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-") or "node"


def localized(record: dict[str, Any], field: str, lang: str) -> str:
    plural = {"title": "titles", "summary": "summaries", "role": "roles"}.get(field)
    if plural and isinstance(record.get(plural), dict):
        values = record[plural]
        if lang in values:
            return str(values[lang])
        if lang == "bilingual" and "zh-CN" in values:
            return str(values["zh-CN"])
    return str(record.get(field, ""))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("node_id")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--focus", default="")
    parser.add_argument(
        "--direction",
        choices=["backward", "forward", "both", "related", "conflicts", "benchmark_use", "repository"],
        default="both",
    )
    parser.add_argument("--mode", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--candidate-budget", type=int, default=120)
    parser.add_argument("--analysis-budget", type=int, default=35)
    parser.add_argument("--language", choices=["zh-CN", "en", "bilingual"])
    args = parser.parse_args()

    data = json.loads(args.graph.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    graph_id = meta.get("graph_id")
    revision = meta.get("revision")
    if not graph_id or not isinstance(revision, int):
        raise SystemExit("Base graph must contain meta.graph_id and integer meta.revision")
    node = next((n for n in data.get("nodes", []) if n.get("id") == args.node_id), None)
    if not node:
        raise SystemExit(f"Node not found: {args.node_id}")

    lang = args.language or meta.get("output_language", "zh-CN")
    title = localized(node, "title", lang) or args.node_id
    default_focus = (
        f"从“{title}”继续调研其来源、后续工作、关键分支、冲突与最新进展。"
        if lang != "en"
        else f"Continue research from '{title}', covering origins, descendants, important branches, conflicts, and the latest frontier."
    )
    now = datetime.now(timezone.utc).isoformat()
    expansion_id = f"exp:{safe_name(args.node_id)}:{uuid.uuid4().hex[:10]}"
    out = args.out or args.graph.parent / "expansions" / safe_name(expansion_id)
    out.mkdir(parents=True, exist_ok=True)

    request = {
        "operation": "expand",
        "base_graph": str(args.graph),
        "base_graph_id": graph_id,
        "base_revision": revision,
        "start_node_id": args.node_id,
        "start_node_title": node.get("title", title),
        "focus": args.focus or default_focus,
        "direction": args.direction,
        "mode": args.mode,
        "max_depth": max(1, min(8, args.depth)),
        "candidate_budget": max(10, args.candidate_budget),
        "analysis_budget": max(5, args.analysis_budget),
        "output_language": lang,
        "summary_policy": meta.get("summary_policy", {
            "audience": "field_familiar_unread",
            "exposition_depth": "explanatory",
            "explain_background": True,
            "define_paper_specific_terms": True,
            "expand_acronyms_on_first_use": True,
            "name_comparison_baselines": True,
            "require_limitations_and_scope": True,
        }),
        "figure_policy": meta.get("figure_policy", {
            "enabled": True,
            "selection_mode": "selective",
            "max_per_paper": 1,
            "require_source_attribution": True,
            "require_alt_text": True,
            "embed_local_assets": True,
            "allow_remote_images": False,
            "max_embedded_bytes": 2500000,
        }),
        "allow_main_path_revision": True,
        "created_at": now,
    }
    (out / "expansion_request.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    patch = {
        "meta": {
            "expansion_id": expansion_id,
            "base_graph_id": graph_id,
            "base_revision": revision,
            "start_node_id": args.node_id,
            "focus": request["focus"],
            "direction": args.direction,
            "output_language": lang,
            "summary_policy": request["summary_policy"],
            "figure_policy": request["figure_policy"],
            "created_at": now,
            "search_cutoff": now[:10],
            "sources": [],
            "warnings": ["Patch skeleton: populate only after evidence-reviewed research."],
        },
        "upsert_nodes": [],
        "upsert_edges": [],
        "upsert_conflicts": [],
        "upsert_clusters": [],
        "coverage_delta": {},
        "main_path_reassessment": {},
        "notes": [],
    }
    (out / "graph_patch.json").write_text(
        json.dumps(patch, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "candidate_ledger.jsonl").touch()
    (out / "papers.jsonl").touch()
    (out / "evidence.jsonl").touch()
    (out / "expansion_manifest.json").write_text(
        json.dumps(
            {
                "expansion_id": expansion_id,
                "status": "initialized",
                "base_graph_id": graph_id,
                "base_revision": revision,
                "start_node_id": args.node_id,
                "created_at": now,
                "output_language": lang,
                "summary_policy": request["summary_policy"],
                "figure_policy": request["figure_policy"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
