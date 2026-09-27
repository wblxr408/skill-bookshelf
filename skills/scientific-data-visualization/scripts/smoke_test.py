#!/usr/bin/env python3
"""Exercise every supported plot type through the public renderer CLI."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts" / "render_figure.py"
THEME = ROOT / "assets" / "themes" / "journal-bilingual.yaml"


def rendered_successfully(completed: subprocess.CompletedProcess[str], report: dict, output: Path) -> bool:
    """Require both renderer completion and the machine-readable visual gate."""
    return (
        completed.returncode == 0
        and report.get("status") == "rendered"
        and report.get("visual_qa", {}).get("status") == "passed"
        and output.exists()
    )


def specification(chart_type: str) -> dict:
    common = {
        "version": 1,
        "data": {"path": "data.csv", "layout": "long"},
        "theme": {"path": str(THEME)},
        "figure": {"type": chart_type, "x": "time", "y": "value", "labels": {"title": f"Smoke {chart_type}", "x": "Time", "y": "Value"}},
        "output": {"stem": chart_type, "formats": ["png"]},
    }
    if chart_type in {"box", "violin", "ecdf", "bar", "pareto", "dot", "paired"}:
        common["figure"].update({"x": "group", "y": "value"})
    if chart_type in {"scatter", "regression-diagnostics"}:
        common["figure"]["regression"] = True
    if chart_type == "line":
        common["figure"].update({"y_lower": "lower", "y_upper": "upper"})
    if chart_type in {"histogram", "kde"}:
        common["figure"] = {"type": chart_type, "x": "value", "labels": {"title": f"Smoke {chart_type}", "x": "Value"}}
    if chart_type == "paired":
        common["figure"]["subject"] = "subject"
    if chart_type == "stacked-bar":
        common["figure"].update({"x": "group", "y": "value", "hue": "condition", "statistic": "sum"})
    if chart_type == "correlation":
        common["figure"] = {"type": "correlation", "variables": ["time", "value", "other"], "labels": {"title": "Smoke correlation"}}
    if chart_type == "multi-panel":
        common["figure"] = {"type": "multi-panel", "columns": 2, "panels": [
            {"type": "line", "x": "time", "y": "value", "y_lower": "lower", "y_upper": "upper", "labels": {"title": "Trend", "x": "Time", "y": "Value"}},
            {"type": "scatter", "x": "time", "y": "value", "labels": {"title": "Association", "x": "Time", "y": "Value"}},
        ]}
    if chart_type == "pca":
        common["figure"] = {"type": "pca", "variables": ["time", "value", "other"], "hue": "group", "labels": {"title": "Smoke PCA"}}
    if chart_type in {"roc", "pr"}:
        common["figure"] = {"type": chart_type, "actual": "actual", "score": "score", "positive_value": 1, "labels": {"title": f"Smoke {chart_type}"}}
    if chart_type == "confusion":
        common["figure"] = {"type": "confusion", "actual": "actual", "predicted": "predicted", "labels": {"title": "Smoke confusion"}}
    if chart_type == "geo-scatter":
        common["figure"] = {"type": "geo-scatter", "longitude": "longitude", "latitude": "latitude", "value": "value", "labels": {"title": "Smoke geo"}}
    if chart_type == "candlestick":
        common["figure"] = {"type": "candlestick", "x": "time", "open": "open", "high": "high", "low": "low", "close": "close", "labels": {"title": "Smoke OHLC"}}
    if chart_type == "waterfall":
        common["figure"] = {"type": "waterfall", "x": "group", "y": "value", "labels": {"title": "Smoke waterfall"}}
    if chart_type == "bubble":
        common["figure"] = {"type": "bubble", "x": "time", "y": "value", "size": "size", "labels": {"title": "Smoke bubble"}}
    if chart_type == "surface3d":
        common["figure"] = {"type": "surface3d", "x": "time", "y": "group_num", "z": "value", "labels": {"title": "Smoke surface"}}
    if chart_type == "polar-heatmap":
        common["figure"] = {"type": "polar-heatmap", "theta": "time", "radius": "group_num", "value": "value", "labels": {"title": "Smoke polar"}}
    if chart_type == "radial-bubble":
        common["figure"] = {"type": "radial-bubble", "theta": "theta", "radius": "radius", "size": "size", "labels": {"title": "Smoke radial"}}
    if chart_type == "population-pyramid":
        common["figure"] = {"type": "population-pyramid", "category": "group", "left": "left", "right": "right", "labels": {"title": "Smoke pyramid"}}
    if chart_type in {"waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall"}:
        common["figure"] = {"type": chart_type, "x": "time", "y": "value", "series": "group", "labels": {"title": f"Smoke {chart_type}"}}
    if chart_type == "floating-bar3d":
        common["figure"] = {"type": "floating-bar3d", "x": "time", "y": "group_num", "z": "value", "labels": {"title": "Smoke floating"}}
    if chart_type == "chord":
        common["figure"] = {"type": "chord", "source": "group", "target": "condition", "value": "value", "labels": {"title": "Smoke chord"}}
    if chart_type == "heatmap":
        common["figure"].update({"x": "condition", "y": "group", "value": "value"})
    return common


def main() -> None:
    rows = []
    for group, offset in [("A", 0), ("B", 2), ("C", 4)]:
        # Twelve observations per group satisfy the renderer's mean-bar gate.
        for time in range(1, 13):
            value = time + offset
            actual = time % 2
            rows.append({"time": time, "subject": time, "group": group, "group_num": offset / 2, "condition": f"C{(time - 1) % 3 + 1}", "value": value, "lower": value - 0.5, "upper": value + 0.5, "other": time**2 + offset, "actual": actual, "predicted": actual if time % 4 else 1 - actual, "score": (time + offset) / 20, "longitude": 100 + time / 10, "latitude": 30 + offset / 10, "size": time, "theta": time / 2, "radius": 1 + offset / 2, "left": time + offset + 1, "right": time + 2, "open": value - 0.2, "high": value + 0.5, "low": value - 0.5, "close": value + 0.1})
    with tempfile.TemporaryDirectory(prefix="scientific-data-visualization-") as directory:
        root = Path(directory)
        data = pd.DataFrame(rows)
        data.to_csv(root / "data.csv", index=False)
        results = {}
        for chart_type in ["line", "scatter", "hexbin", "regression-diagnostics", "qq", "leverage", "bar", "stacked-bar", "dot", "paired", "box", "violin", "ecdf", "histogram", "kde", "heatmap", "correlation", "pca", "roc", "pr", "confusion", "geo-scatter", "candlestick", "waterfall", "waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall", "bubble", "surface3d", "floating-bar3d", "polar-heatmap", "radial-bubble", "population-pyramid", "connected-bar", "chord", "pareto", "control", "multi-panel"]:
            spec_path = root / f"{chart_type}.yaml"
            spec_path.write_text(yaml.safe_dump(specification(chart_type), sort_keys=False), encoding="utf-8")
            out = root / chart_type
            completed = subprocess.run([sys.executable, str(RENDERER), str(spec_path), "--output-dir", str(out)], capture_output=True, text=True)
            report_path = out / "render-report.json"
            report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
            passed = rendered_successfully(completed, report, out / f"{chart_type}.png")
            results[chart_type] = {"passed": passed, "stderr": completed.stderr.strip(), "errors": report.get("errors", []), "visual_qa": report.get("visual_qa", {}).get("status", "missing")}
        data.to_excel(root / "data.xlsx", index=False, sheet_name="Measurements")
        excel_spec = specification("line")
        excel_spec["data"] = {"path": "data.xlsx", "sheet": "Measurements", "layout": "long"}
        excel_path = root / "xlsx-line.yaml"
        excel_path.write_text(yaml.safe_dump(excel_spec, sort_keys=False), encoding="utf-8")
        excel_out = root / "xlsx-line"
        completed = subprocess.run([sys.executable, str(RENDERER), str(excel_path), "--output-dir", str(excel_out)], capture_output=True, text=True)
        report_path = excel_out / "render-report.json"
        report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
        results["xlsx-input"] = {"passed": rendered_successfully(completed, report, excel_out / "line.png"), "stderr": completed.stderr.strip(), "errors": report.get("errors", []), "visual_qa": report.get("visual_qa", {}).get("status", "missing")}
        print(json.dumps(results, indent=2))
        if not all(item["passed"] for item in results.values()):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
