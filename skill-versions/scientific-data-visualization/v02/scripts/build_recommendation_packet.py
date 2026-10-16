#!/usr/bin/env python3
"""Combine visual and statistical evidence into an executable three-tier recommendation packet.

This script never computes a statistic.  It preserves the strict eligibility
boundary from ``recommend_statistics.py`` while serializing the AI-facing
``首选 / 待确认候选 / 不适用`` contract for downstream use.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def method_catalogue() -> dict[str, dict[str, Any]]:
    source = yaml.safe_load((ROOT / "assets" / "ai-conditional-methods.yaml").read_text(encoding="utf-8"))
    return source["methods"]


def as_tier_item(item: dict[str, Any], verified: bool, status: str, missing: list[str] | None = None) -> dict[str, Any]:
    result = {"method_id": item.get("method_id"), "variant": item.get("variant"), "evidence": item.get("evidence"), "status": status, "verified": verified}
    if missing:
        result["missing"] = missing
    return {key: value for key, value in result.items() if value is not None}


def build(statistics: dict[str, Any] | None, visual: dict[str, Any] | None, conditional_ids: list[str], rejected: list[str]) -> dict[str, Any]:
    tiers: dict[str, list[dict[str, Any]]] = {"首选": [], "待确认候选": [], "不适用": []}
    catalogue = method_catalogue()
    if statistics:
        state = statistics.get("status")
        recommendations = statistics.get("recommendations", [])
        if state == "eligible":
            tiers["首选"].extend(as_tier_item(item, True, "eligible") for item in recommendations)
        elif state == "eligible-development":
            missing = ["训练、预处理、调参、校准和未见测试集评价产物"]
            tiers["待确认候选"].extend(as_tier_item(item, False, "eligible-development", missing) for item in recommendations)
        elif state in {"needs-confirmation", "blocked", "needs-user-choice"}:
            tiers["不适用"].append({"scope": "local strict adapter", "reason": statistics.get("reasons") or statistics.get("missing") or [statistics.get("question", "必要设计信息未确认")], "status": state})
        elif state and state != "not-requested":
            tiers["不适用"].append({"scope": "local strict adapter", "reason": [f"unsupported recommendation packet status: {state}"], "status": state})
    for method_id in conditional_ids:
        method = catalogue.get(method_id)
        if method is None:
            tiers["不适用"].append({"method_id": method_id, "reason": ["不是已登记的 AI 条件方法；不得将其假定为可推荐。"]})
        else:
            tiers["待确认候选"].append({"method_id": method_id, "label": method["label"], "verified": False, "status": "AI_CONDITIONAL", "missing": method["requires"]})
    for raw in rejected:
        method_id, separator, reason = raw.partition(":")
        tiers["不适用"].append({"method_id": method_id, "reason": [reason.strip() if separator and reason.strip() else "调用方声明该方法与当前问题或数据契约冲突。"]})
    visual_summary = []
    if visual:
        visual_summary = visual.get("recommendations") or visual.get("primary_renderable_candidates") or []
    return {
        "version": 1,
        "contract": ["首选", "待确认候选", "不适用"],
        "statistics": tiers,
        "visual_candidates": visual_summary[:3],
        "boundary": "首选仅表示当前数据与已确认契约匹配；只有 verified: true 的本地资格门结果可称为已验证。此包不含或生成任何推断结果、模型指标或因果结论。",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--statistics-packet", type=Path)
    parser.add_argument("--visual-packet", type=Path)
    parser.add_argument("--conditional-method", action="append", default=[])
    parser.add_argument("--not-applicable", action="append", default=[], metavar="METHOD:REASON")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.statistics_packet and not args.visual_packet and not args.conditional_method and not args.not_applicable:
        parser.error("supply at least one evidence packet or method declaration")
    packet = build(read_json(args.statistics_packet) if args.statistics_packet else None, read_json(args.visual_packet) if args.visual_packet else None, args.conditional_method, args.not_applicable)
    text = json.dumps(packet, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
