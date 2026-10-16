#!/usr/bin/env python3
"""Run the reproducible inspect -> route -> recommend -> specify workflow.

The command deliberately stops before rendering when field semantics are not
confirmed. It creates a complete evidence directory rather than silently
guessing an experimental unit, pairing, or time ordering.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

import build_recommendation_packet
import inspect_data
import route_from_prompt


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_THEME = ROOT / "assets" / "themes" / "general-bilingual.yaml"


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def starter_spec(data: Path, candidate: dict[str, Any], theme: Path, output_dir: Path) -> tuple[dict[str, Any] | None, list[str]]:
    mapping = candidate.get("suggested_mapping", {})
    figure: dict[str, Any] = {"type": candidate["id"]}
    missing: list[str] = []
    for key, value in mapping.items():
        if value is None:
            missing.append(f"figure.{key}")
        else:
            figure[key] = value
    if candidate["id"] == "paired" and "subject" not in figure:
        missing.append("figure.subject")
    if missing:
        return None, sorted(set(missing))
    figure["labels"] = {"title": f"Starter: {candidate['label']}", "x": str(mapping.get("x", "")), "y": str(mapping.get("y", ""))}
    spec = {
        "version": 1,
        "data": {"path": str(data.resolve())},
        "theme": {"path": str(theme.resolve())},
        "figure": figure,
        "output": {"stem": "figure", "formats": ["png", "svg", "pdf"]},
        "notes": ["Generated as a starter only. Confirm units, experimental unit, ordering, pairing and intended claim before rendering.", f"Router reason: {candidate['reason']}"],
    }
    return spec, []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--theme", type=Path, default=DEFAULT_THEME)
    parser.add_argument("--confirm-semantics", action="store_true")
    parser.add_argument("--statistics-packet", type=Path)
    parser.add_argument("--conditional-method", action="append", default=[])
    parser.add_argument("--not-applicable", action="append", default=[])
    parser.add_argument("--render", action="store_true", help="Render the starter only when --confirm-semantics is supplied")
    args = parser.parse_args()
    if not args.data.exists():
        parser.error(f"data source does not exist: {args.data}")
    if not args.theme.exists():
        parser.error(f"theme does not exist: {args.theme}")
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    frame = inspect_data.load_table(args.data, args.sheet)
    profile = inspect_data.profile(frame)
    goals = route_from_prompt.task_dimensions(args.prompt)
    primary, rejected = route_from_prompt.direct_candidates(profile, goals)
    primary = primary[:3]
    route = {"version": 2, "status": "eligible-visual-routing" if args.confirm_semantics else "needs-confirmation", "prompt": args.prompt, "task_dimensions": goals, "data_profile": profile, "primary_renderable_candidates": primary, "conditional_visual_candidates": rejected[:3], "recommendations": primary if args.confirm_semantics else [], "missing": [] if args.confirm_semantics else ["确认测量单位、实验单位、分组含义、配对/独立性，以及时间/类别顺序。"]}
    write_json(out / "data-profile.json", profile)
    write_json(out / "visual-route.json", route)
    stats = json.loads(args.statistics_packet.read_text(encoding="utf-8")) if args.statistics_packet else None
    recommendation = build_recommendation_packet.build(stats, route, args.conditional_method, args.not_applicable)
    write_json(out / "recommendation.json", recommendation)
    manifest: dict[str, Any] = {"version": 1, "status": "needs-confirmation", "source": str(args.data.resolve()), "artifacts": ["data-profile.json", "visual-route.json", "recommendation.json"]}
    if not args.confirm_semantics:
        manifest["missing"] = route["missing"]
    elif not primary:
        manifest["status"] = "blocked"; manifest["missing"] = ["没有满足数据契约的可渲染候选图。"]
    else:
        spec, missing = starter_spec(args.data, primary[0], args.theme, out)
        if spec is None:
            manifest["status"] = "needs-confirmation"; manifest["missing"] = missing
        else:
            (out / "starter-spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
            manifest["status"] = "specified"; manifest["artifacts"].append("starter-spec.yaml")
            if args.render:
                render_dir = out / "rendered"
                completed = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_figure.py"), str(out / "starter-spec.yaml"), "--output-dir", str(render_dir)], capture_output=True, text=True)
                render_report = render_dir / "render-report.json"
                manifest["render_returncode"] = completed.returncode
                if render_report.exists():
                    manifest["render_report"] = "rendered/render-report.json"; manifest["artifacts"].append("rendered/render-report.json")
                if completed.returncode == 0:
                    manifest["status"] = "rendered"
                else:
                    manifest["status"] = "failed"; manifest["render_error"] = completed.stdout[-2000:]
    write_json(out / "workflow-manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    raise SystemExit(0 if manifest["status"] in {"needs-confirmation", "specified", "rendered"} else 2)


if __name__ == "__main__":
    main()
