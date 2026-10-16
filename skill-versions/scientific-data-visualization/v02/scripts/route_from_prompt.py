#!/usr/bin/env python3
"""Build an auditable visual-recommendation packet from a table and analytical prompt.

The packet intentionally separates renderable first choices from conditional
visual candidates. It is evidence for the AI Skill, not a significance claim.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from inspect_data import load_table, profile as inspect_profile
from chart_support import SUPPORTED


GOAL_RULES = {
    "distribution": (r"分布|离散|异常|偏态|箱线|小提琴|ecdf|density|histogram|直方", ["histogram", "kde", "box", "violin", "ecdf"]),
    "comparison": (r"比较|差异|组间|treat|control|group", ["dot", "box", "violin", "bar"]),
    "paired": (r"配对|前后|before|after|repeated", ["paired", "dot"]),
    "association": (r"相关|关系|回归|association|correlation|relationship", ["scatter", "hexbin", "regression-diagnostics", "correlation"]),
    "trend": (r"趋势|时序|时间|过程|trend|time|series", ["line", "control"]),
    "composition": (r"构成|占比|贡献|缺陷|pareto|composition", ["pareto", "stacked-bar", "bar"]),
    "matrix": (r"矩阵|热图|相关矩阵|matrix|heatmap", ["correlation", "heatmap"]),
    "quality": (r"质量|稳定|控制图|control|process", ["control", "pareto"]),
    "classification": (r"分类|预测性能|roc|auc|precision|recall|混淆|classification", ["roc", "pr", "confusion"]),
    "reduction": (r"降维|主成分|pca|projection|特征空间", ["pca"]),
    "diagnostic": (r"诊断|qq|正态|杠杆|残差|leverage|residual", ["qq", "leverage", "regression-diagnostics"]),
    "geospatial": (r"地理|地图|经纬度|latitude|longitude|geo|map", ["geo-scatter"]),
    "finance": (r"K线|OHLC|开高低收|candlestick|金融|stock", ["candlestick"]),
    "surface": (r"曲面|surface|3D|三维|地形", ["surface3d"]),
    "waterfall": (r"瀑布|waterfall|增量", ["waterfall"]),
    "bubble": (r"气泡|bubble|第三变量大小", ["bubble"]),
    "polar": (r"极坐标|polar|径向|radial", ["polar-heatmap", "radial-bubble"]),
    "pyramid": (r"人口金字塔|population pyramid|pyramid", ["population-pyramid"]),
    "connected": (r"连接条|connected bar|有序条形", ["connected-bar"]),
    "spectra": (r"XRD|XPS|光谱|spectrum|spectra", ["xrd-waterfall", "xps-waterfall", "color-waterfall"]),
    "chord": (r"和弦|chord|网络关联", ["chord"]),
    "floating3d": (r"浮动柱|floating bar|3D bar", ["floating-bar3d"]),
}
LABELS = {
    "line": "Line plot / 折线图", "scatter": "Scatter plot / 散点图", "hexbin": "Hexbin density / 六边形密度图", "regression-diagnostics": "Residual diagnostics / 回归残差图",
    "bar": "Bar chart / 条形图", "stacked-bar": "Stacked bar / 堆叠条形图", "dot": "Individual observations / 原始点图", "paired": "Paired slope plot / 配对斜率图",
    "box": "Box plot / 箱线图", "violin": "Violin plot / 小提琴图", "ecdf": "ECDF / 经验累积分布", "histogram": "Histogram / 直方图", "kde": "KDE / 核密度图",
    "heatmap": "Heatmap / 热图", "correlation": "Correlation matrix / 相关矩阵", "pca": "PCA projection / PCA 投影", "roc": "ROC curve / ROC 曲线", "pr": "Precision-recall curve / PR 曲线", "confusion": "Confusion matrix / 混淆矩阵", "qq": "Q-Q plot / Q-Q 图", "leverage": "Leverage plot / 杠杆图", "geo-scatter": "Geographic scatter / 经纬度散点", "candlestick": "Candlestick / K线", "waterfall": "Waterfall / 瀑布图", "waterfall-lines": "Waterfall lines / 瀑布线", "xrd-waterfall": "XRD waterfall / XRD 瀑布", "xps-waterfall": "XPS waterfall / XPS 瀑布", "color-waterfall": "Color waterfall / 彩色瀑布", "bubble": "Bubble chart / 气泡图", "surface3d": "3D surface / 三维曲面", "floating-bar3d": "Floating 3D bars / 浮动三维柱", "polar-heatmap": "Polar heatmap / 极坐标热图", "radial-bubble": "Radial bubble / 径向气泡", "population-pyramid": "Population pyramid / 人口金字塔", "connected-bar": "Connected bar / 连接条形图", "chord": "Chord diagram / 和弦图", "pareto": "Pareto chart / 帕累托图", "control": "Control chart / 控制图",
}


def task_dimensions(prompt: str) -> list[str]:
    lowered = prompt.casefold()
    return [goal for goal, (pattern, _) in GOAL_RULES.items() if re.search(pattern, lowered, flags=re.IGNORECASE)] or ["unspecified"]


def direct_candidates(facts: dict, goals: list[str]) -> tuple[list[dict], list[dict]]:
    fields = facts["fields"]
    numeric = [field["name"] for field in fields if field["inferred_role"] == "numeric_measurement"]
    categorical = [field["name"] for field in fields if field["inferred_role"] == "categorical_group"]
    identifiers = [field["name"] for field in fields if field["inferred_role"] == "identifier"]
    ordered = [field["name"] for field in fields if field["inferred_role"] == "datetime" or re.search(r"time|date|year|month|时间|日期|年份|月份", field["name"], flags=re.IGNORECASE)]
    group_sizes = facts["group_sizes"]
    minimum_group_n = min((min(sizes.values()) for sizes in group_sizes.values() if sizes), default=0)
    quality = facts["numeric_quality"]
    proposals, rejected = [], []
    ordered_ids = []
    for goal in goals:
        ordered_ids.extend(GOAL_RULES.get(goal, ("", []))[1])
    for chart_id in dict.fromkeys(ordered_ids):
        eligible, reason, caution = False, "", None
        if chart_id == "dot":
            eligible, reason = bool(numeric and categorical and minimum_group_n >= 1), "requires one numeric measure and one grouping field; displays every observed value"
        elif chart_id in {"box", "ecdf"}:
            eligible, reason = bool(numeric and categorical and minimum_group_n >= 3), "requires one numeric measure, one grouping field, and at least three observations in every displayed group"
            if eligible and minimum_group_n < 10:
                caution = "Small groups: show all observations; do not rely on distribution shape alone."
        elif chart_id == "violin":
            eligible, reason = bool(numeric and categorical and minimum_group_n >= 10), "requires one numeric measure, one grouping field, and at least ten observations in every displayed group to support density shape"
        elif chart_id == "bar":
            eligible, reason = bool(numeric and categorical and minimum_group_n >= 10), "requires a numeric measure, grouping field, and at least ten observations per mean-summary group"
            if not eligible and numeric and categorical:
                caution = "Mean-only bars are blocked for small groups; use a distribution display."
        elif chart_id == "scatter":
            eligible, reason = len(numeric) >= 2, "requires two numeric variables with nonzero variance"
            if eligible and any("strong_skew" in quality[column]["shape_flags"] for column in numeric[:2]):
                caution = "Strong skew detected: inspect transformation and outliers before adding a fitted line."
        elif chart_id == "hexbin":
            eligible, reason = bool(len(numeric) >= 2 and facts["rows"] >= 30), "requires two numeric variables and at least thirty observations to avoid a sparse density grid"
        elif chart_id == "regression-diagnostics":
            eligible, reason = bool(len(numeric) >= 2 and facts["rows"] >= 8), "requires a pre-specified two-variable regression and at least eight usable observations"
            caution = "This is a diagnostic display, not a regression recommendation or adequacy proof."
        elif chart_id == "paired":
            eligible, reason = bool(numeric and categorical and identifiers and facts["semantic_hints"]["has_subject_id_hint"]), "requires an explicit subject identifier and confirmed complete matched condition cells"
            caution = "The router cannot prove pairing completeness; the renderer rejects incomplete or duplicated subject-condition cells."
        elif chart_id == "line":
            eligible, reason = bool(numeric and ordered), "requires a numeric measure and an explicit ordered time/process field"
        elif chart_id == "control":
            eligible, reason = bool(numeric and ordered and facts["rows"] >= 20), "requires ordered process data with at least twenty observations"
        elif chart_id == "heatmap":
            eligible, reason = bool((len(categorical) >= 2 and numeric) or len(numeric) >= 3), "requires a condition matrix with numeric values or enough numeric variables for a correlation matrix"
        elif chart_id == "correlation":
            eligible, reason = len(numeric) >= 3, "requires at least three numeric variables with nonzero variance"
        elif chart_id == "pca":
            eligible, reason = bool(len(numeric) >= 3 and facts["rows"] >= 10), "requires at least three numeric features and ten observations"
            caution = "PCA is exploratory; confirm scaling, missing-data handling and feature interpretation before using it as evidence."
        elif chart_id in {"roc", "pr", "confusion"}:
            eligible, reason = bool(numeric and categorical and facts["rows"] >= 20), "requires an explicit binary outcome, a score or predicted class field, and at least twenty observations"
            caution = "The router cannot infer which field is the observed outcome versus a model score; confirm the mapping before rendering."
        elif chart_id == "qq":
            eligible, reason = bool(numeric and facts["rows"] >= 8), "requires a numeric residual or continuous sample with at least eight observations"
        elif chart_id == "leverage":
            eligible, reason = bool(len(numeric) >= 2 and facts["rows"] >= 8), "requires a numeric predictor/outcome pair and at least eight observations"
            caution = "Leverage is model-specific; confirm the fitted model and predictor mapping."
        elif chart_id == "geo-scatter":
            eligible, reason = bool(facts["semantic_hints"]["has_geo_hint"] and len(numeric) >= 2), "requires explicit longitude/latitude fields and an optional numeric magnitude"
            caution = "Coordinate scatter has no CRS transform or basemap; confirm coordinate reference system."
        elif chart_id == "candlestick":
            eligible, reason = bool(facts["rows"] >= 5 and len(numeric) >= 4), "requires ordered time and open/high/low/close numeric fields"
            caution = "Confirm market session, adjusted prices and OHLC provenance before interpretation."
        elif chart_id == "waterfall":
            eligible, reason = bool(numeric and categorical), "requires ordered additive increments and a categorical step field"
        elif chart_id == "bubble":
            eligible, reason = bool(len(numeric) >= 3), "requires numeric x, y and an explicitly declared size field"
        elif chart_id == "surface3d":
            eligible, reason = bool(len(numeric) >= 3 and facts["rows"] >= 10), "requires three numeric coordinates and documented surface sampling semantics"
            caution = "3D surfaces can hide values; use only when a surface interpretation is scientifically justified."
        elif chart_id == "polar-heatmap":
            eligible, reason = bool(len(numeric) >= 3 and facts["rows"] >= 10), "requires angular, radial and value fields with at least ten observations"
        elif chart_id == "radial-bubble":
            eligible, reason = bool(len(numeric) >= 3 and facts["rows"] >= 5), "requires numeric angle, radius and bubble-size fields"
        elif chart_id == "population-pyramid":
            eligible, reason = bool(categorical and len(numeric) >= 2), "requires one category field and two comparable numeric sides"
        elif chart_id == "connected-bar":
            eligible, reason = bool(numeric and categorical), "requires a genuinely ordered categorical axis and one numeric response"
            caution = "Do not use connected bars for unordered categories; use a regular bar or dot plot instead."
        elif chart_id in {"waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall"}:
            eligible, reason = bool(numeric and categorical), "requires ordered numeric x/y and a series field for spectra or stacked traces"
        elif chart_id == "floating-bar3d":
            eligible, reason = bool(len(numeric) >= 3 and facts["rows"] >= 5), "requires three numeric coordinates and documented 3D bar bases"
        elif chart_id == "chord":
            eligible, reason = bool(numeric and len(categorical) >= 2), "requires source, target and nonnegative association-weight fields"
        elif chart_id == "pareto":
            eligible, reason = bool(numeric and categorical), "requires categorical contributions and a nonnegative count/burden measure"
            if eligible:
                caution = "Confirm that the numeric field is a count or additive burden before using Pareto ordering."
        elif chart_id == "stacked-bar":
            eligible, reason = bool(len(categorical) >= 2 and numeric), "requires two categorical dimensions and a nonnegative additive measure"
            caution = "Confirm that stacks represent parts of a common total; use a separate distribution chart for individual measurements."
        elif chart_id == "histogram":
            eligible, reason = bool(numeric and facts["rows"] >= 5), "requires one numeric measure and at least five observations"
        elif chart_id == "kde":
            eligible, reason = bool(numeric and facts["rows"] >= 10), "requires one numeric measure and at least ten observations to support a density estimate"
        item = {"id": chart_id, "label": LABELS[chart_id], "renderable": chart_id in SUPPORTED, "reason": reason, "suggested_mapping": suggested_mapping(chart_id, numeric, categorical, identifiers, ordered)}
        if caution:
            item["caution"] = caution
        (proposals if eligible else rejected).append(item)
    return proposals, rejected


def suggested_mapping(chart_id: str, numeric: list[str], categorical: list[str], identifiers: list[str], ordered: list[str]) -> dict:
    """Suggest fields conservatively; final semantics still require user confirmation."""
    value = numeric[0] if numeric else None
    relation = numeric[:2]
    group = categorical[0] if categorical else None
    if chart_id in {"histogram", "kde"}:
        return {"x": value}
    if chart_id in {"scatter", "hexbin", "regression-diagnostics"}:
        return {"x": relation[0] if relation else None, "y": relation[1] if len(relation) > 1 else None}
    if chart_id == "correlation":
        return {"variables": numeric}
    if chart_id == "pca":
        return {"variables": numeric}
    if chart_id in {"roc", "pr"}:
        return {"actual": categorical[0] if categorical else None, "score": value, "positive_value": None}
    if chart_id == "confusion":
        return {"actual": categorical[0] if categorical else None, "predicted": categorical[1] if len(categorical) > 1 else None}
    if chart_id == "qq":
        return {"x": value}
    if chart_id == "leverage":
        return {"x": relation[0] if relation else None, "y": relation[1] if len(relation) > 1 else None}
    if chart_id == "geo-scatter":
        longitude = next((field for field in numeric if re.search(r"lon|longitude|经度", field, flags=re.IGNORECASE)), None)
        latitude = next((field for field in numeric if re.search(r"lat|latitude|纬度", field, flags=re.IGNORECASE)), None)
        return {"longitude": longitude, "latitude": latitude, "value": value}
    if chart_id == "candlestick":
        return {"x": ordered[0] if ordered else None, "open": next((field for field in numeric if re.search(r"open|开", field, flags=re.IGNORECASE)), None), "high": next((field for field in numeric if re.search(r"high|高", field, flags=re.IGNORECASE)), None), "low": next((field for field in numeric if re.search(r"low|低", field, flags=re.IGNORECASE)), None), "close": next((field for field in numeric if re.search(r"close|收", field, flags=re.IGNORECASE)), None)}
    if chart_id == "waterfall":
        return {"x": group, "y": value}
    if chart_id == "bubble":
        return {"x": relation[0] if relation else None, "y": relation[1] if len(relation) > 1 else None, "size": relation[2] if len(relation) > 2 else None}
    if chart_id == "surface3d":
        return {"x": relation[0] if relation else None, "y": relation[1] if len(relation) > 1 else None, "z": relation[2] if len(relation) > 2 else None}
    if chart_id == "polar-heatmap":
        return {"theta": relation[0] if relation else None, "radius": relation[1] if len(relation) > 1 else None, "value": relation[2] if len(relation) > 2 else None}
    if chart_id == "radial-bubble":
        return {"theta": relation[0] if relation else None, "radius": relation[1] if len(relation) > 1 else None, "size": relation[2] if len(relation) > 2 else None}
    if chart_id == "population-pyramid":
        return {"category": group, "left": relation[0] if relation else None, "right": relation[1] if len(relation) > 1 else None}
    if chart_id == "connected-bar":
        return {"x": group, "y": value, "x_ordered": True}
    if chart_id in {"waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall"}:
        return {"x": relation[0] if relation else None, "y": relation[1] if len(relation) > 1 else None, "series": group}
    if chart_id == "floating-bar3d":
        return {"x": relation[0] if relation else None, "y": relation[1] if len(relation) > 1 else None, "z": relation[2] if len(relation) > 2 else None}
    if chart_id == "chord":
        return {"source": categorical[0] if categorical else None, "target": categorical[1] if len(categorical) > 1 else None, "value": value}
    if chart_id in {"paired"}:
        return {"x": group, "y": value, "subject": identifiers[0] if identifiers else None}
    if chart_id in {"line", "control"}:
        return {"x": ordered[0] if ordered else None, "y": next((field for field in numeric if field not in ordered), value)}
    if chart_id == "heatmap":
        return {"x": categorical[0] if categorical else None, "y": categorical[1] if len(categorical) > 1 else None, "value": value}
    if chart_id == "stacked-bar":
        return {"x": categorical[0] if categorical else None, "hue": categorical[1] if len(categorical) > 1 else None, "y": value}
    return {"x": group, "y": value}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("--prompt", required=True, help="Analytical question or intended claim; not merely a chart name.")
    parser.add_argument("--sheet")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--confirm-semantics", action="store_true", help="Confirm that units, experimental unit, grouping, pairing, and ordering were reviewed.")
    args = parser.parse_args()
    facts = inspect_profile(load_table(args.data, args.sheet))
    goals = task_dimensions(args.prompt)
    primary, rejected = direct_candidates(facts, goals)
    primary = primary[:args.limit]
    payload = {
        "version": 2,
        "task_dimensions": goals,
        "data_profile": facts,
        "primary_renderable_candidates": primary,
        "conditional_visual_candidates": [
            {"id": item["id"], "label": item["label"], "reason": item["reason"], "status": "not-currently-suitable"}
            for item in rejected[:args.limit]
        ],
        "inference_boundary": "Visual routing does not establish significance, causality, model adequacy, or a valid statistical test.",
    }
    if args.confirm_semantics:
        payload.update({"status": "eligible-visual-routing", "recommendations": primary})
    else:
        payload.update({"status": "needs-confirmation", "recommendations": [], "missing": ["确认测量单位、实验单位、分组含义、配对/独立性，以及时间/类别顺序后，使用 --confirm-semantics。"]})
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
