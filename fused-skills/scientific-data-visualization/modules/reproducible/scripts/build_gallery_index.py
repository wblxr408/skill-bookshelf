#!/usr/bin/env python3
"""Build a line-oriented keyword index and fail when a reference screenshot is unclassified."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from chart_support import support_status


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "assets" / "reference-catalogue.yaml"
INDEX = ROOT / "assets" / "chart-keyword-index.jsonl"
FAMILY_TERMS = {
    "exploratory-2d": ["趋势", "时序", "关系", "相关", "散点", "误差", "配对"],
    "distribution-quality": ["分布", "离散", "异常", "质量", "箱线", "小提琴", "直方", "密度", "概率"],
    "comparison-composition": ["比较", "对比", "占比", "组成", "柱状", "条形", "饼", "瀑布"],
    "multivariate-coordinated": ["多变量", "分组", "平行", "网络", "流向", "多面板"],
    "matrix-contour-density": ["热图", "矩阵", "等高线", "密度", "相关性"],
    "geospatial": ["地图", "地理", "区域", "经纬度"],
    "polar-ternary-finance": ["极坐标", "雷达", "三元", "金融", "K线"],
    "three-d-functions": ["三维", "3d", "曲面", "函数"],
    "domain-templates": ["xrd", "xps", "光谱", "模板"],
}
TYPE_ALIASES = ["小提琴", "箱线", "直方", "散点", "气泡", "折线", "阶梯", "样条", "误差", "柱状", "条形", "饼图", "环形", "面积", "瀑布", "桥图", "平行", "桑基", "弦图", "网络", "热图", "等高线", "核密度", "地图", "雷达", "极坐标", "三元", "K线", "三维", "3D", "曲面", "控制", "雨云", "帕累托"]


def terms(*values: str) -> list[str]:
    result = []
    for value in values:
        value = value.replace("/", " ").replace("-", " ")
        result.extend(part.strip("()[]") for part in value.split() if len(part.strip("()[]")) >= 2)
    return list(dict.fromkeys(result))


def direct_terms(variant: dict) -> list[str]:
    raw = f"{variant['id']} {variant['label']}"
    return list(dict.fromkeys([*terms(raw), *(alias for alias in TYPE_ALIASES if alias.casefold() in raw.casefold())]))


def records(catalogue: dict) -> tuple[list[dict], set[str]]:
    output, mapped_sources = [], set()
    for category in catalogue["categories"]:
        for subcategory in category["subcategories"]:
            mapped_sources.update(subcategory["sources"])
            for variant in subcategory["variants"]:
                output.append({
                    "id": variant["id"],
                    "label": variant["label"],
                    "family": f"{category['id']}/{subcategory['id']}",
                    "status": support_status(variant["id"]),
                    "catalogue_status": variant.get("status", "catalogued"),
                    "direct_terms": direct_terms(variant),
                    "family_terms": FAMILY_TERMS[category["id"]],
                })
    return output, mapped_sources


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate corpus coverage without writing the index.")
    args = parser.parse_args()
    catalogue = yaml.safe_load(CATALOGUE.read_text(encoding="utf-8"))
    rows, mapped = records(catalogue)
    source_dir = (CATALOGUE.parent / catalogue["source_corpus"]["directory"]).resolve()
    actual = {path.name for path in source_dir.glob("*.png")}
    unmapped, missing = sorted(actual - mapped), sorted(mapped - actual)
    report = {"specific_types": len(rows), "source_screenshots": len(actual), "unmapped_screenshots": unmapped, "missing_screenshots": missing}
    if unmapped or missing:
        raise SystemExit(json.dumps(report, ensure_ascii=False))
    if not args.check:
        INDEX.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")
        report["index"] = str(INDEX)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
