#!/usr/bin/env python3
"""Validate core integrity, revision, localization, and expansion constraints."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED_NODE = {"id", "type", "title", "year", "summary", "role"}
REQUIRED_EDGE = {"id", "source", "target", "relationship", "explanation", "confidence"}
LANGUAGES = {"zh-CN", "en", "bilingual"}
READER_SUMMARY_REQUIRED = {"background", "problem", "approach", "key_findings", "why_it_matters", "limitations"}


def validate_reader_summary(node_id: str, reader_summary: Any, lang: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(reader_summary, dict):
        return [f"Paper node {node_id} lacks structured reader_summary"], warnings
    if reader_summary.get("audience") != "field_familiar_unread":
        errors.append(f"Paper node {node_id} reader_summary.audience must be field_familiar_unread")
    required_langs = ["zh-CN", "en"] if lang == "bilingual" else [lang]
    for language in required_langs:
        content = reader_summary.get(language)
        if not isinstance(content, dict):
            errors.append(f"Paper node {node_id} reader_summary lacks {language} content")
            continue
        missing = READER_SUMMARY_REQUIRED - content.keys()
        if missing:
            errors.append(f"Paper node {node_id} reader_summary.{language} missing: {sorted(missing)}")
        if not isinstance(content.get("key_findings"), list) or not content.get("key_findings"):
            errors.append(f"Paper node {node_id} reader_summary.{language}.key_findings must be a non-empty array")
        if not isinstance(content.get("limitations"), list) or not content.get("limitations"):
            errors.append(f"Paper node {node_id} reader_summary.{language}.limitations must be a non-empty array")
        concepts = content.get("concepts", [])
        if concepts and not isinstance(concepts, list):
            errors.append(f"Paper node {node_id} reader_summary.{language}.concepts must be an array")
        elif isinstance(concepts, list):
            for i, concept in enumerate(concepts):
                if not isinstance(concept, dict) or not concept.get("term") or not concept.get("explanation"):
                    errors.append(f"Paper node {node_id} reader_summary.{language}.concepts[{i}] needs term and explanation")
        # Heuristic clarity checks; warnings rather than brittle hard failures.
        joined = " ".join(str(content.get(k, "")) for k in ("background", "problem", "approach", "why_it_matters"))
        if len(joined.strip()) < 180:
            warnings.append(f"Paper node {node_id} reader_summary.{language} may be too compressed for an unread-paper audience")
    return errors, warnings


def localized_figure_text(figure: dict[str, Any], scalar: str, map_name: str, language: str) -> str:
    mapping = figure.get(map_name)
    if isinstance(mapping, dict) and isinstance(mapping.get(language), str):
        return mapping[language].strip()
    value = figure.get(scalar)
    return value.strip() if isinstance(value, str) else ""


def validate_featured_figure(
    node_id: str, figure: Any, lang: str, base_dir: Path | None
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if figure is None:
        return errors, warnings
    if not isinstance(figure, dict):
        return [f"Paper node {node_id} featured_figure must be an object or null"], warnings

    if not figure.get("kind"):
        errors.append(f"Paper node {node_id} featured_figure.kind is required")
    source = figure.get("source")
    if not isinstance(source, dict):
        errors.append(f"Paper node {node_id} featured_figure.source is required")
        source = {}
    if not source.get("citation"):
        errors.append(f"Paper node {node_id} featured_figure.source.citation is required")
    rights = source.get("rights_status")
    if not rights:
        errors.append(f"Paper node {node_id} featured_figure.source.rights_status is required")
    elif rights == "unknown":
        warnings.append(f"Paper node {node_id} featured figure has unknown rights/usage status")
    if figure.get("display_kind") == "analyst_reconstruction" and rights != "analyst_original":
        errors.append(f"Paper node {node_id} analyst reconstruction must use rights_status=analyst_original")
    if figure.get("display_kind") != "analyst_reconstruction" and not (source.get("figure_number") or source.get("page")):
        warnings.append(f"Paper node {node_id} featured figure lacks figure number/page")

    required_langs = ["zh-CN", "en"] if lang == "bilingual" else [lang]
    for language in required_langs:
        if not localized_figure_text(figure, "caption", "captions", language):
            errors.append(f"Paper node {node_id} featured figure lacks {language} caption")
        if not localized_figure_text(figure, "alt_text", "alt_texts", language):
            errors.append(f"Paper node {node_id} featured figure lacks {language} alt text")
        if not localized_figure_text(figure, "reader_note", "reader_notes", language):
            warnings.append(f"Paper node {node_id} featured figure lacks {language} reader note")

    if not (figure.get("selection_reason") or figure.get("selection_reasons")):
        warnings.append(f"Paper node {node_id} featured figure lacks a selection reason")

    asset = figure.get("asset")
    if not isinstance(asset, dict):
        errors.append(f"Paper node {node_id} featured_figure.asset is required")
        return errors, warnings
    path_value = asset.get("path")
    url_value = asset.get("url")
    data_uri = asset.get("data_uri")
    if not any(isinstance(x, str) and x.strip() for x in (path_value, url_value, data_uri)):
        errors.append(f"Paper node {node_id} featured figure asset needs path, url, or data_uri")
    if isinstance(data_uri, str) and data_uri and not data_uri.startswith("data:image/"):
        errors.append(f"Paper node {node_id} featured figure data_uri must be an image data URI")
    if isinstance(url_value, str) and url_value and not url_value.startswith("https://"):
        warnings.append(f"Paper node {node_id} featured figure remote URL is not HTTPS")
    if isinstance(path_value, str) and path_value and base_dir is not None:
        raw_path = Path(path_value)
        if raw_path.is_absolute():
            errors.append(f"Paper node {node_id} featured figure path must be relative")
        else:
            resolved = (base_dir / raw_path).resolve()
            try:
                resolved.relative_to(base_dir.resolve())
            except ValueError:
                errors.append(f"Paper node {node_id} featured figure path escapes graph directory")
            else:
                if not resolved.is_file():
                    errors.append(f"Paper node {node_id} featured figure asset not found: {path_value}")
                elif resolved.stat().st_size > 5_000_000:
                    warnings.append(f"Paper node {node_id} featured figure exceeds 5 MB; compress it for HTML embedding")
    return errors, warnings


def validate(data: dict[str, Any], base_dir: Path | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in ("meta", "nodes", "edges"):
        if key not in data:
            errors.append(f"Missing top-level field: {key}")

    meta = data.get("meta", {})
    for field in ("title", "focus", "generated_at"):
        if not isinstance(meta, dict) or not meta.get(field):
            errors.append(f"meta.{field} is required")
    if not meta.get("graph_id"):
        warnings.append("meta.graph_id is missing; incremental expansion cannot be safely targeted")
    revision = meta.get("revision")
    if revision is None:
        warnings.append("meta.revision is missing; assuming legacy revision 1")
        revision = 1
    elif not isinstance(revision, int) or revision < 1:
        errors.append("meta.revision must be an integer >= 1")
    lang = meta.get("output_language", "zh-CN")
    if lang not in LANGUAGES:
        errors.append(f"meta.output_language must be one of {sorted(LANGUAGES)}")
    summary_policy = meta.get("summary_policy")
    if not isinstance(summary_policy, dict):
        warnings.append("meta.summary_policy is missing; defaulting conceptually to field_familiar_unread")
    elif summary_policy.get("audience") != "field_familiar_unread":
        warnings.append("meta.summary_policy.audience is not field_familiar_unread; this version is optimized for unread-paper explanations")

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    if not isinstance(nodes, list):
        errors.append("nodes must be an array")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be an array")
        edges = []

    node_ids: list[str] = []
    paper_count = 0
    featured_figure_count = 0
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"nodes[{index}] must be an object")
            continue
        missing = REQUIRED_NODE - node.keys()
        if missing:
            errors.append(f"nodes[{index}] missing: {sorted(missing)}")
        node_id = node.get("id")
        if isinstance(node_id, str):
            node_ids.append(node_id)
        else:
            errors.append(f"nodes[{index}].id must be a string")
        for field in ("relevance", "quality"):
            if field in node and not (isinstance(node[field], (int, float)) and 0 <= node[field] <= 1):
                errors.append(f"nodes[{index}].{field} must be in [0,1]")
        for field in ("added_in_revision", "updated_in_revision"):
            if field in node and (not isinstance(node[field], int) or node[field] < 1 or node[field] > revision):
                errors.append(f"nodes[{index}].{field} must be in [1, meta.revision]")
        if node.get("type") == "paper":
            paper_count += 1
            reader_errors, reader_warnings = validate_reader_summary(str(node_id), node.get("reader_summary"), lang)
            errors.extend(reader_errors)
            warnings.extend(reader_warnings)
            if node.get("featured_figure") is not None:
                featured_figure_count += 1
            figure_errors, figure_warnings = validate_featured_figure(
                str(node_id), node.get("featured_figure"), lang, base_dir
            )
            errors.extend(figure_errors)
            warnings.extend(figure_warnings)
            publication = node.get("publication")
            if not isinstance(publication, dict):
                warnings.append(f"Paper node {node_id} lacks structured publication metadata")
            else:
                status = publication.get("status")
                primary = publication.get("primary_venue") or {}
                versions = publication.get("versions", [])
                if status == "preprint_only" and primary and primary.get("type") not in (None, "preprint_server"):
                    warnings.append(f"Paper node {node_id} is preprint_only but has a non-preprint primary venue")
                if primary.get("tier") == "top":
                    if not primary.get("tier_basis"):
                        errors.append(f"Top-venue node {node_id} lacks primary_venue.tier_basis")
                    if not primary.get("tier_as_of"):
                        errors.append(f"Top-venue node {node_id} lacks primary_venue.tier_as_of")
                if status != "preprint_only" and not primary.get("name"):
                    warnings.append(f"Published/accepted paper node {node_id} lacks primary venue name")
                if versions and not isinstance(versions, list):
                    errors.append(f"nodes[{index}].publication.versions must be an array")
        if lang == "zh-CN":
            summaries = node.get("summaries", {})
            if isinstance(summaries, dict) and summaries and not summaries.get("zh-CN"):
                warnings.append(f"Node {node_id} has localized summaries but no zh-CN entry")
        if lang == "bilingual":
            summaries = node.get("summaries", {})
            if not isinstance(summaries, dict) or not summaries.get("zh-CN") or not summaries.get("en"):
                warnings.append(f"Bilingual node {node_id} lacks both zh-CN and en summaries")

    figure_policy = meta.get("figure_policy", {})
    if isinstance(figure_policy, dict) and figure_policy.get("enabled") is False and featured_figure_count:
        warnings.append("meta.figure_policy.enabled is false but featured figures are present")
    if paper_count >= 8 and featured_figure_count == paper_count:
        warnings.append("Every paper node has a featured figure; verify that selection is genuinely selective rather than decorative")

    duplicates = [node_id for node_id, count in Counter(node_ids).items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate node IDs: {duplicates}")
    node_set = set(node_ids)

    edge_ids: list[str] = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edges[{index}] must be an object")
            continue
        missing = REQUIRED_EDGE - edge.keys()
        if missing:
            errors.append(f"edges[{index}] missing: {sorted(missing)}")
        edge_id = edge.get("id")
        if isinstance(edge_id, str):
            edge_ids.append(edge_id)
        else:
            errors.append(f"edges[{index}].id must be a string")
        if edge.get("source") not in node_set:
            errors.append(f"edges[{index}] source not found: {edge.get('source')}")
        if edge.get("target") not in node_set:
            errors.append(f"edges[{index}] target not found: {edge.get('target')}")
        relationship = edge.get("relationship")
        if not isinstance(relationship, list) or not relationship:
            errors.append(f"edges[{index}].relationship must be a non-empty array")
        confidence = edge.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append(f"edges[{index}].confidence must be in [0,1]")
        if edge.get("conflict") and not edge.get("conflict_type"):
            warnings.append(f"Conflict edge {edge_id} has no conflict_type")
        if not edge.get("evidence_ids"):
            warnings.append(f"Edge {edge_id} has no evidence_ids")
        for field in ("added_in_revision", "updated_in_revision"):
            if field in edge and (not isinstance(edge[field], int) or edge[field] < 1 or edge[field] > revision):
                errors.append(f"edges[{index}].{field} must be in [1, meta.revision]")
        if lang == "bilingual":
            explanations = edge.get("explanations", {})
            if not isinstance(explanations, dict) or not explanations.get("zh-CN") or not explanations.get("en"):
                warnings.append(f"Bilingual edge {edge_id} lacks both zh-CN and en explanations")

    duplicate_edges = [edge_id for edge_id, count in Counter(edge_ids).items() if count > 1]
    if duplicate_edges:
        errors.append(f"Duplicate edge IDs: {duplicate_edges}")

    conflict_edge_ids = {e.get("id") for e in edges if e.get("conflict")}
    conflict_records = data.get("conflicts", [])
    referenced_conflict_edges = {
        edge_id for item in conflict_records if isinstance(item, dict) for edge_id in item.get("edge_ids", [])
    }
    unadjudicated = sorted(conflict_edge_ids - referenced_conflict_edges)
    if unadjudicated:
        warnings.append(f"Conflict edges without conflict record: {unadjudicated}")

    history = meta.get("expansion_history", [])
    if history and not isinstance(history, list):
        errors.append("meta.expansion_history must be an array")
    latest_increment = meta.get("latest_increment")
    if latest_increment is not None:
        if not isinstance(latest_increment, dict):
            errors.append("meta.latest_increment must be an object or null")
        else:
            inc_revision = latest_increment.get("revision")
            if not isinstance(inc_revision, int) or inc_revision < 2:
                errors.append("meta.latest_increment.revision must be an integer >= 2")
            elif inc_revision != revision:
                errors.append("meta.latest_increment.revision must equal meta.revision")
            if not history:
                errors.append("meta.latest_increment requires non-empty meta.expansion_history")
    elif isinstance(revision, int) and revision > 1 and history:
        warnings.append("meta.latest_increment is missing; latest-expansion highlighting will be disabled")

    if isinstance(history, list):
        seen = set()
        for i, item in enumerate(history):
            if not isinstance(item, dict):
                errors.append(f"meta.expansion_history[{i}] must be an object")
                continue
            exp_id = item.get("id")
            if not exp_id:
                warnings.append(f"Expansion history record {i} has no id")
            elif exp_id in seen:
                errors.append(f"Duplicate expansion history id: {exp_id}")
            seen.add(exp_id)
            if item.get("start_node_id") not in node_set:
                warnings.append(f"Expansion {exp_id} start_node_id is not in the current graph")
            if isinstance(item.get("revision"), int) and item["revision"] > revision:
                errors.append(f"Expansion {exp_id} targets future revision {item['revision']}")

    coverage = meta.get("coverage", {})
    if isinstance(coverage, dict):
        if coverage.get("reviewed_nodes") not in (None, len(nodes)):
            warnings.append("meta.coverage.reviewed_nodes does not match node count")
        if coverage.get("reviewed_edges") not in (None, len(edges)):
            warnings.append("meta.coverage.reviewed_edges does not match edge count")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.graph.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("ERROR: top-level JSON must be an object", file=sys.stderr)
        return 2
    errors, warnings = validate(data, args.graph.parent)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"Validation passed: {len(data.get('nodes', []))} nodes, {len(data.get('edges', []))} edges, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
