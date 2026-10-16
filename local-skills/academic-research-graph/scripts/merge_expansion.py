#!/usr/bin/env python3
"""Safely merge an evidence-reviewed node-expansion patch into a graph revision."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def merge_value(old: Any, new: Any) -> Any:
    """Non-destructive recursive merge; lists are unioned by value or id."""
    if isinstance(old, dict) and isinstance(new, dict):
        result = copy.deepcopy(old)
        for key, value in new.items():
            result[key] = merge_value(result[key], value) if key in result else copy.deepcopy(value)
        return result
    if isinstance(old, list) and isinstance(new, list):
        result = copy.deepcopy(old)
        ids = {item.get("id"): i for i, item in enumerate(result) if isinstance(item, dict) and item.get("id")}
        for item in new:
            if isinstance(item, dict) and item.get("id") in ids:
                idx = ids[item["id"]]
                result[idx] = merge_value(result[idx], item)
            elif item not in result:
                result.append(copy.deepcopy(item))
        return result
    return copy.deepcopy(new)


def upsert_records(base: list[dict[str, Any]], patch: list[dict[str, Any]], revision: int) -> tuple[list[dict[str, Any]], int, int]:
    result = copy.deepcopy(base)
    index = {item.get("id"): i for i, item in enumerate(result) if item.get("id")}
    added = updated = 0
    for item in patch:
        item_id = item.get("id")
        if not item_id:
            raise ValueError("Every upsert record must have an id")
        if item_id in index:
            merged = merge_value(result[index[item_id]], item)
            merged["updated_in_revision"] = revision
            result[index[item_id]] = merged
            updated += 1
        else:
            created = copy.deepcopy(item)
            created.setdefault("added_in_revision", revision)
            created.setdefault("updated_in_revision", revision)
            index[item_id] = len(result)
            result.append(created)
            added += 1
    return result, added, updated


def _safe_relative(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"Asset path must be relative: {value}")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Asset path escapes its run directory: {value}") from exc
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stage_patch_figure_assets(patch: dict[str, Any], patch_dir: Path, output_dir: Path) -> int:
    """Copy safe local featured-figure assets into the base run, rewriting collisions."""
    copied = 0
    for node in patch.get("upsert_nodes", []):
        figure = node.get("featured_figure") if isinstance(node, dict) else None
        asset = figure.get("asset") if isinstance(figure, dict) else None
        value = asset.get("path") if isinstance(asset, dict) else None
        if not isinstance(value, str) or not value:
            continue
        source = _safe_relative(patch_dir, value)
        target = _safe_relative(output_dir, value)
        # A patch may reuse an asset that already belongs to the base run.
        if not source.is_file():
            if target.is_file():
                continue
            raise ValueError(f"Featured-figure asset does not exist: {value}")
        if source == target:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            source_hash = _sha256(source)
            if _sha256(target) == source_hash:
                asset.setdefault("sha256", source_hash)
                continue
            target = target.with_name(f"{target.stem}-{source_hash[:8]}{target.suffix}")
            asset["path"] = target.relative_to(output_dir.resolve()).as_posix()
        shutil.copy2(source, target)
        asset.setdefault("sha256", _sha256(target))
        copied += 1
    return copied


def upsert_optional(base: list[dict[str, Any]], patch: list[dict[str, Any]], revision: int) -> tuple[list[dict[str, Any]], int, int]:
    normalized = []
    for i, item in enumerate(patch):
        x = copy.deepcopy(item)
        x.setdefault("id", x.get("edge_id") or x.get("name") or f"record:{i}")
        normalized.append(x)
    return upsert_records(base, normalized, revision)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_graph", type=Path)
    parser.add_argument("patch", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--delta", type=Path)
    parser.add_argument("--no-archive", action="store_true")
    args = parser.parse_args()

    try:
        base = json.loads(args.base_graph.read_text(encoding="utf-8"))
        patch = json.loads(args.patch.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    meta = base.get("meta", {})
    pmeta = patch.get("meta", {})
    graph_id = meta.get("graph_id")
    revision = meta.get("revision")
    if not graph_id or not isinstance(revision, int):
        print("ERROR: base graph lacks meta.graph_id or integer meta.revision", file=sys.stderr)
        return 2
    if pmeta.get("base_graph_id") != graph_id:
        print("ERROR: patch base_graph_id does not match", file=sys.stderr)
        return 2
    if pmeta.get("base_revision") != revision:
        print(f"ERROR: patch targets revision {pmeta.get('base_revision')}, current revision is {revision}", file=sys.stderr)
        return 2

    start_node_id = pmeta.get("start_node_id")
    if start_node_id not in {n.get("id") for n in base.get("nodes", [])}:
        print(f"ERROR: start node not found in base graph: {start_node_id}", file=sys.stderr)
        return 2

    try:
        assets_copied = stage_patch_figure_assets(patch, args.patch.parent, args.output.parent)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    new_revision = revision + 1
    merged = copy.deepcopy(base)
    try:
        merged["nodes"], na, nu = upsert_records(base.get("nodes", []), patch.get("upsert_nodes", []), new_revision)
        merged["edges"], ea, eu = upsert_records(base.get("edges", []), patch.get("upsert_edges", []), new_revision)
        merged["conflicts"], ca, cu = upsert_optional(base.get("conflicts", []), patch.get("upsert_conflicts", []), new_revision)
        merged["clusters"], cla, clu = upsert_optional(base.get("clusters", []), patch.get("upsert_clusters", []), new_revision)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    node_ids = {n.get("id") for n in merged.get("nodes", [])}
    dangling = [e.get("id") for e in merged.get("edges", []) if e.get("source") not in node_ids or e.get("target") not in node_ids]
    if dangling:
        print(f"ERROR: dangling edges after merge: {dangling}", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc).isoformat()
    expansion = {
        "id": pmeta.get("expansion_id"),
        "base_revision": revision,
        "revision": new_revision,
        "start_node_id": start_node_id,
        "focus": pmeta.get("focus", ""),
        "direction": pmeta.get("direction", "both"),
        "output_language": pmeta.get("output_language", meta.get("output_language", "zh-CN")),
        "summary_policy": pmeta.get("summary_policy", meta.get("summary_policy", {})),
        "figure_policy": pmeta.get("figure_policy", meta.get("figure_policy", {})),
        "created_at": pmeta.get("created_at"),
        "merged_at": now,
        "search_cutoff": pmeta.get("search_cutoff"),
        "sources": pmeta.get("sources", []),
        "delta": {
            "nodes_added": na, "nodes_updated": nu,
            "edges_added": ea, "edges_updated": eu,
            "conflicts_added": ca, "conflicts_updated": cu,
            "clusters_added": cla, "clusters_updated": clu,
            "figure_assets_copied": assets_copied,
        },
        "main_path_reassessment": patch.get("main_path_reassessment", {}),
        "warnings": pmeta.get("warnings", []),
    }
    merged.setdefault("expansions", []).append(expansion)
    merged_meta = merged.setdefault("meta", {})
    merged_meta["parent_revision"] = revision
    merged_meta["revision"] = new_revision
    merged_meta["generated_at"] = now
    if pmeta.get("search_cutoff"):
        merged_meta["search_cutoff"] = max(str(merged_meta.get("search_cutoff", "")), str(pmeta["search_cutoff"]))
    merged_meta["sources"] = sorted(set(merged_meta.get("sources", [])) | set(pmeta.get("sources", [])))
    merged_meta.setdefault("expansion_history", []).append(expansion)
    # Only expansion merges create a "latest increment". A fresh revision-1 graph
    # intentionally has no such marker, so the renderer does not label the entire
    # baseline as newly added/updated.
    merged_meta["latest_increment"] = {
        "revision": new_revision,
        "expansion_id": expansion.get("id"),
        "base_revision": revision,
        "start_node_id": start_node_id,
        "merged_at": now,
    }
    if pmeta.get("output_language"):
        merged_meta["output_language"] = pmeta["output_language"]
    if pmeta.get("summary_policy"):
        merged_meta["summary_policy"] = merge_value(merged_meta.get("summary_policy", {}), pmeta["summary_policy"])
    if pmeta.get("figure_policy"):
        merged_meta["figure_policy"] = merge_value(merged_meta.get("figure_policy", {}), pmeta["figure_policy"])
    coverage = merged_meta.setdefault("coverage", {})
    for key, value in patch.get("coverage_delta", {}).items():
        if isinstance(value, (int, float)) and isinstance(coverage.get(key, 0), (int, float)):
            coverage[key] = coverage.get(key, 0) + value
        else:
            coverage[key] = value
    coverage["reviewed_nodes"] = len(merged.get("nodes", []))
    coverage["reviewed_edges"] = len(merged.get("edges", []))

    for node in merged.get("nodes", []):
        if node.get("id") == start_node_id:
            status = node.setdefault("expansion_status", {})
            status["last_expanded_at"] = now
            status["last_expansion_id"] = expansion["id"]
            status["last_expansion_revision"] = new_revision
            status["expansion_count"] = int(status.get("expansion_count", 0)) + 1
            seeds = node.setdefault("expansion_seed_for", [])
            if expansion["id"] and expansion["id"] not in seeds:
                seeds.append(expansion["id"])
            node["updated_in_revision"] = new_revision
            break

    if not args.no_archive:
        history = args.output.parent / "history"
        history.mkdir(parents=True, exist_ok=True)
        archive = history / f"graph.rev-{revision}.json"
        archive.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    delta = {
        "graph_id": graph_id,
        "from_revision": revision,
        "to_revision": new_revision,
        "expansion": expansion,
        "added_node_ids": [n.get("id") for n in patch.get("upsert_nodes", []) if n.get("id") not in {x.get("id") for x in base.get("nodes", [])}],
        "updated_node_ids": [n.get("id") for n in patch.get("upsert_nodes", []) if n.get("id") in {x.get("id") for x in base.get("nodes", [])}],
        "added_edge_ids": [e.get("id") for e in patch.get("upsert_edges", []) if e.get("id") not in {x.get("id") for x in base.get("edges", [])}],
        "updated_edge_ids": [e.get("id") for e in patch.get("upsert_edges", []) if e.get("id") in {x.get("id") for x in base.get("edges", [])}],
        "figure_assets_copied": assets_copied,
        "notes": patch.get("notes", []),
    }
    delta_path = args.delta or args.output.with_name("delta_report.json")
    delta_path.parent.mkdir(parents=True, exist_ok=True)
    delta_path.write_text(json.dumps(delta, ensure_ascii=False, indent=2), encoding="utf-8")

    lang = merged_meta.get("output_language", "zh-CN")
    if lang == "en":
        md = f"# Expansion delta\n\n- Graph: `{graph_id}`\n- Revision: {revision} → {new_revision}\n- Start node: `{start_node_id}`\n- Focus: {expansion['focus']}\n- Added nodes: {na}; updated nodes: {nu}\n- Added edges: {ea}; updated edges: {eu}\n- Figure assets copied: {assets_copied}\n"
    else:
        md = f"# 增量调研差异\n\n- 图谱：`{graph_id}`\n- 版本：{revision} → {new_revision}\n- 起始节点：`{start_node_id}`\n- 本次焦点：{expansion['focus']}\n- 新增节点：{na}；更新节点：{nu}\n- 新增关系：{ea}；更新关系：{eu}\n- 复制主图资源：{assets_copied}\n"
    delta_path.with_suffix(".md").write_text(md, encoding="utf-8")
    print(args.output)
    print(delta_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
