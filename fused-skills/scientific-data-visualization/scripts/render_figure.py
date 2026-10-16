#!/usr/bin/env python3
"""Render a versioned YAML/JSON figure specification with QA and vector export."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
import yaml
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.metrics import auc, confusion_matrix, precision_recall_curve, roc_curve
from chart_support import SUPPORTED
try:
    from visual_qa import audit_paths
except ImportError:  # direct import through an external test harness
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from visual_qa import audit_paths

INFERENTIAL_METHODS = {
    "two-sample-t", "one-way-anova", "one-way-repeated-anova", "two-way-anova", "three-way-anova", "mann-whitney", "kruskal-wallis", "paired-t", "paired-wilcoxon",
    "friedman", "two-sample-proportion", "logistic-regression", "ordinal-regression", "pearson-correlation", "partial-correlation", "kaplan-meier", "cox-model", "multiple-linear-regression",
}
MIN_REGRESSION_POINTS = 8
MIN_CONTROL_POINTS = 20


class SpecificationError(ValueError):
    pass


def read_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SpecificationError(f"Configuration file does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    result = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(result, dict):
        raise SpecificationError(f"Configuration root must be a mapping: {path}")
    return result


def sha256_file(path: Path) -> str:
    """Fingerprint the exact bytes consumed by a reproducible render."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deep_merge(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def resolve(path_text: str, relative_to: Path) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else (relative_to / path).resolve()


def load_data(data: dict[str, Any], spec_dir: Path) -> tuple[pd.DataFrame, Path]:
    source = resolve(str(data.get("path", "")), spec_dir)
    if not source.exists():
        raise SpecificationError(f"Data source does not exist: {source}")
    suffix = source.suffix.lower()
    if suffix == ".csv":
        frame = pd.read_csv(source, encoding=data.get("encoding", "utf-8-sig"))
    elif suffix in {".xlsx", ".xls"}:
        sheet = data.get("sheet", 0)
        frame = pd.read_excel(source, sheet_name=sheet)
    else:
        raise SpecificationError("Only CSV, XLSX, and XLS sources are supported.")
    return frame, source


def apply_transforms(frame: pd.DataFrame, transforms: list[dict[str, Any]], warnings: list[str]) -> pd.DataFrame:
    result = frame.copy()
    original = len(result)
    for step in transforms:
        action = step.get("type")
        column = step.get("column")
        if action == "drop_missing":
            cols = step.get("columns") or ([column] if column else list(result.columns))
            result = result.dropna(subset=cols)
        elif action == "sort":
            result = result.sort_values(column, ascending=bool(step.get("ascending", True)))
        elif action == "filter_equals":
            result = result.loc[result[column] == step.get("value")]
        elif action == "filter_between":
            result = result.loc[result[column].between(step.get("min"), step.get("max"), inclusive="both")]
        elif action == "log10":
            if (result[column] <= 0).any():
                raise SpecificationError(f"log10 requires positive values in '{column}'.")
            target = step.get("output_column", f"log10_{column}")
            result[target] = np.log10(result[column])
        else:
            raise SpecificationError(f"Unsupported transform: {action}")
    if original and (original - len(result)) / original > 0.1:
        warnings.append(f"Transforms removed {(original-len(result))/original:.1%} of rows.")
    return result


def is_ordered_axis(frame: pd.DataFrame, field: str, figure: dict[str, Any]) -> bool:
    return bool(figure.get("x_ordered")) or pd.api.types.is_numeric_dtype(frame[field]) or pd.api.types.is_datetime64_any_dtype(frame[field])


def validate_statistics(statistics: dict[str, Any] | None, base_dir: Path | None = None) -> list[str]:
    if not statistics:
        return []
    errors = []
    if statistics.get("confirmed") is not True:
        errors.append("statistics requires confirmed: true before it may appear in a figure.")
    method_id = statistics.get("method_id")
    if method_id in INFERENTIAL_METHODS:
        eligibility = statistics.get("eligibility", {})
        if eligibility.get("status") != "eligible" or eligibility.get("method_id") != method_id:
            errors.append("Inferential statistics require matching statistics.eligibility with status: eligible and method_id.")
        reference = statistics.get("analysis_reference")
        if not reference:
            errors.append("Inferential statistics require analysis_reference pointing to the validated analysis record.")
        elif base_dir is not None and not resolve(str(reference), base_dir).exists():
            errors.append(f"analysis_reference does not exist: {resolve(str(reference), base_dir)}")
    return errors


def validate(frame: pd.DataFrame, figure: dict[str, Any], theme: dict[str, Any], warnings: list[str], statistics: dict[str, Any] | None = None, base_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    chart = figure.get("type")
    if chart not in SUPPORTED:
        errors.append(f"figure.type must be one of {sorted(SUPPORTED)}.")
        return errors
    if chart == "multi-panel":
        panels = figure.get("panels")
        if not isinstance(panels, list) or not 2 <= len(panels) <= 8:
            return ["multi-panel requires between two and eight figure.panels entries."]
        for index, panel in enumerate(panels, start=1):
            if not isinstance(panel, dict):
                errors.append(f"Panel {index} must be a mapping.")
                continue
            errors.extend([f"panel {index}: {message}" for message in validate(frame, panel, theme, warnings, None, base_dir)])
        return errors
    required = set()
    if chart not in {"correlation", "pca", "roc", "pr", "confusion", "geo-scatter", "candlestick", "surface3d", "floating-bar3d", "polar-heatmap", "radial-bubble", "population-pyramid", "chord"}:
        required.add("x")
    if chart not in {"heatmap", "histogram", "kde", "correlation", "pca", "roc", "pr", "confusion", "geo-scatter", "candlestick", "surface3d", "floating-bar3d", "polar-heatmap", "radial-bubble", "population-pyramid", "chord", "qq"}:
        required.add("y")
    if chart == "heatmap":
        required.update({"x", "y", "value"})
    for key in required:
        field = figure.get(key)
        if not field:
            errors.append(f"{chart} requires figure.{key}.")
        elif field not in frame.columns:
            errors.append(f"Column '{field}' configured as figure.{key} does not exist.")
    hue = figure.get("hue")
    if hue and hue not in frame.columns:
        errors.append(f"Column '{hue}' configured as figure.hue does not exist.")
    errors.extend(validate_statistics(statistics, base_dir))
    if errors:
        return errors
    if chart == "heatmap":
        numeric_fields = {figure.get("value")}
    elif chart in {"histogram", "kde"}:
        numeric_fields = {figure.get("x")}
    elif chart == "correlation":
        numeric_fields = set(figure.get("variables") or [column for column in frame.columns if pd.api.types.is_numeric_dtype(frame[column])])
        if len(numeric_fields) < 3:
            errors.append("correlation requires figure.variables with at least three numeric fields.")
    elif chart == "pca":
        numeric_fields = set(figure.get("variables") or [])
        if len(numeric_fields) < 2:
            errors.append("pca requires figure.variables with at least two numeric feature fields.")
    elif chart in {"roc", "pr"}:
        actual, score = figure.get("actual"), figure.get("score")
        numeric_fields = {score}
        if not actual or actual not in frame.columns:
            errors.append(f"{chart} requires figure.actual containing binary observed outcomes.")
        elif frame[actual].dropna().nunique() != 2:
            errors.append(f"{chart} requires exactly two observed outcome values.")
    elif chart == "confusion":
        numeric_fields = set()
        for name in ("actual", "predicted"):
            value = figure.get(name)
            if not value or value not in frame.columns:
                errors.append(f"confusion requires figure.{name}.")
    elif chart == "geo-scatter":
        numeric_fields = {figure.get("longitude"), figure.get("latitude"), figure.get("value")}
        for key in ("longitude", "latitude"):
            field = figure.get(key)
            if not field or field not in frame.columns:
                errors.append(f"geo-scatter requires figure.{key} with numeric coordinates.")
    elif chart == "candlestick":
        numeric_fields = {figure.get(key) for key in ("open", "high", "low", "close")}
        for key in ("open", "high", "low", "close"):
            field = figure.get(key)
            if not field or field not in frame.columns:
                errors.append(f"candlestick requires figure.{key}.")
    elif chart == "surface3d":
        numeric_fields = {figure.get(key) for key in ("x", "y", "z")}
        for key in ("x", "y", "z"):
            field = figure.get(key)
            if not field or field not in frame.columns:
                errors.append(f"surface3d requires figure.{key}.")
    elif chart == "polar-heatmap":
        numeric_fields = {figure.get(key) for key in ("theta", "radius", "value")}
        for key in ("theta", "radius", "value"):
            if not figure.get(key) or figure[key] not in frame.columns:
                errors.append(f"polar-heatmap requires figure.{key}.")
    elif chart == "radial-bubble":
        numeric_fields = {figure.get(key) for key in ("theta", "radius", "size")}
        for key in ("theta", "radius", "size"):
            if not figure.get(key) or figure[key] not in frame.columns:
                errors.append(f"radial-bubble requires figure.{key}.")
    elif chart == "population-pyramid":
        numeric_fields = {figure.get("left"), figure.get("right")}
        for key in ("category", "left", "right"):
            if not figure.get(key) or figure[key] not in frame.columns:
                errors.append(f"population-pyramid requires figure.{key}.")
    elif chart in {"waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall"}:
        numeric_fields = {figure.get("x"), figure.get("y")}
        if not figure.get("x") or not figure.get("y"):
            errors.append(f"{chart} requires ordered figure.x and numeric figure.y.")
    elif chart == "floating-bar3d":
        numeric_fields = {figure.get(key) for key in ("x", "y", "z")}
        for key in ("x", "y", "z"):
            if not figure.get(key) or figure[key] not in frame.columns:
                errors.append(f"floating-bar3d requires figure.{key}.")
    elif chart == "chord":
        numeric_fields = {figure.get("value")}
        for key in ("source", "target", "value"):
            if not figure.get(key) or figure[key] not in frame.columns:
                errors.append(f"chord requires figure.{key}.")
    else:
        numeric_fields = {figure.get("y")}
    for field in filter(None, numeric_fields):
        if field not in frame.columns:
            errors.append(f"Column '{field}' does not exist.")
        elif not pd.api.types.is_numeric_dtype(frame[field]):
            errors.append(f"'{field}' must be numeric for {chart}.")
        elif frame[field].dropna().empty:
            errors.append(f"'{field}' has no usable numeric values.")
    usable_fields = [field for field in [figure.get("x"), figure.get("y"), figure.get("value"), hue] if field]
    if chart == "correlation":
        usable_fields = list(numeric_fields)
    if chart == "pca":
        usable_fields = list(numeric_fields) + ([hue] if hue else [])
    if chart in {"roc", "pr"}:
        usable_fields = [figure.get("actual"), figure.get("score")]
    if chart == "confusion":
        usable_fields = [figure.get("actual"), figure.get("predicted")]
    if chart == "geo-scatter":
        usable_fields = [figure.get("longitude"), figure.get("latitude"), figure.get("value")]
    if chart == "candlestick":
        usable_fields = [figure.get(key) for key in ("x", "open", "high", "low", "close")]
    if chart == "surface3d":
        usable_fields = [figure.get(key) for key in ("x", "y", "z")]
    if chart == "polar-heatmap":
        usable_fields = [figure.get(key) for key in ("theta", "radius", "value")]
    if chart == "radial-bubble":
        usable_fields = [figure.get(key) for key in ("theta", "radius", "size")]
    if chart == "population-pyramid":
        usable_fields = [figure.get(key) for key in ("category", "left", "right")]
    if chart in {"waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall"}:
        usable_fields = [figure.get(key) for key in ("x", "y", "series") if figure.get(key)]
    if chart == "floating-bar3d":
        usable_fields = [figure.get(key) for key in ("x", "y", "z")]
    if chart == "chord":
        usable_fields = [figure.get(key) for key in ("source", "target", "value")]
    if frame.dropna(subset=usable_fields).empty:
        errors.append("No usable rows remain for the selected figure mappings.")
    if frame.empty:
        errors.append("No rows remain after transforms.")
    if frame.duplicated().any():
        warnings.append(f"Source contains {int(frame.duplicated().sum())} duplicate rows; confirm whether replication is intended.")
    palette = theme.get("palette", {}).get("categorical", [])
    if hue and len(frame[hue].dropna().unique()) > len(palette):
        warnings.append("Hue categories exceed the categorical palette capacity; colors will repeat.")
    if chart in {"line", "control"} and not is_ordered_axis(frame, figure["x"], figure):
        errors.append(f"{chart} requires a numeric/datetime x axis or figure.x_ordered: true with documented ordering.")
    if chart in {"scatter", "hexbin", "regression-diagnostics", "leverage"}:
        if not pd.api.types.is_numeric_dtype(frame[figure["x"]]):
            errors.append(f"{chart} requires a numeric figure.x field.")
        if chart in {"regression-diagnostics", "leverage"} or figure.get("regression"):
            usable = frame.dropna(subset=[figure["x"], figure["y"]])
            if len(usable) < MIN_REGRESSION_POINTS or usable[figure["x"]].nunique() < 3:
                errors.append(f"OLS regression requires at least {MIN_REGRESSION_POINTS} usable observations and three distinct x values.")
            elif usable[figure["y"]].nunique() < 2:
                errors.append("OLS regression requires variation in figure.y.")
            warnings.append("Regression rendering is descriptive only; residual, leverage, and independence diagnostics remain required before model inference.")
    if chart == "line" and len(frame.dropna(subset=[figure["x"], figure["y"]])) < 2:
        errors.append("line requires at least two usable observations.")
    for uncertainty_key in ("y_lower", "y_upper", "y_error"):
        uncertainty = figure.get(uncertainty_key)
        if uncertainty:
            if uncertainty not in frame.columns or not pd.api.types.is_numeric_dtype(frame[uncertainty]):
                errors.append(f"{chart} uncertainty field '{uncertainty}' must be an existing numeric column.")
    if chart in {"box", "violin", "ecdf"}:
        groups = frame.groupby(figure["x"], dropna=False)[figure["y"]].count()
        if (groups < 3).any():
            errors.append("Distribution charts require at least three usable observations in every group; use an individual-point display for smaller groups.")
    if chart == "bar" and figure.get("statistic", "mean") == "mean":
        groups = frame.groupby(figure["x"], dropna=False)[figure["y"]].count()
        if (groups < 10).any():
            errors.append("Mean bars require at least 10 usable observations in every group; use a distribution/individual-point figure instead.")
        warnings.append("Mean bars are descriptive only unless uncertainty, experimental unit, and inference evidence are documented separately.")
    if chart == "stacked-bar" and not hue:
        errors.append("stacked-bar requires figure.hue for the stacked category.")
    if chart == "bubble":
        size_field = figure.get("size")
        if not size_field or size_field not in frame.columns or not pd.api.types.is_numeric_dtype(frame[size_field]):
            errors.append("bubble requires figure.size with an existing numeric size field.")
    if chart in {"histogram", "kde"} and len(frame[figure["x"]].dropna()) < 5:
        errors.append(f"{chart} requires at least five usable observations.")
    if chart == "qq" and len(frame[figure["x"]].dropna()) < 8:
        errors.append("qq requires at least eight usable observations.")
    if chart == "hexbin" and len(frame.dropna(subset=[figure["x"], figure["y"]])) < 30:
        errors.append("hexbin requires at least 30 usable observations; use scatter for smaller samples.")
    if chart in {"geo-scatter", "candlestick", "surface3d"} and len(frame.dropna(subset=usable_fields)) < 5:
        errors.append(f"{chart} requires at least five complete observations.")
    if chart in {"polar-heatmap", "radial-bubble", "population-pyramid"} and len(frame.dropna(subset=usable_fields)) < 5:
        errors.append(f"{chart} requires at least five complete observations.")
    if chart in {"waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall", "floating-bar3d", "chord"} and len(frame.dropna(subset=usable_fields)) < 5:
        errors.append(f"{chart} requires at least five complete observations.")
    if chart == "paired":
        subject = figure.get("subject")
        if not subject or subject not in frame.columns:
            errors.append("paired requires figure.subject identifying matched experimental units.")
        else:
            pair_data = frame.dropna(subset=[subject, figure["x"], figure["y"]])
            conditions = list(pd.unique(pair_data[figure["x"]]))
            cells = pair_data.groupby([subject, figure["x"]], dropna=False).size()
            expected = len(pair_data[subject].unique()) * len(conditions)
            if len(conditions) < 2 or len(pair_data[subject].unique()) < 2 or len(cells) != expected or (cells != 1).any():
                errors.append("paired requires at least two complete, unique observations for every subject-by-condition cell.")
    if chart == "pareto":
        values = frame[figure["y"]].dropna()
        if (values < 0).any() or values.sum() <= 0:
            errors.append("pareto requires non-negative values with a positive total.")
    if chart == "control":
        usable = frame.dropna(subset=[figure["x"], figure["y"]])
        if len(usable) < MIN_CONTROL_POINTS:
            errors.append(f"control requires at least {MIN_CONTROL_POINTS} ordered observations; screening limits would otherwise be unstable.")
        if usable[figure["y"]].nunique() < 2:
            errors.append("control requires variation in figure.y.")
        warnings.append("The rendered three-sigma limits are screening limits, not validated process-control limits.")
    return errors


def resolve_fonts(theme: dict[str, Any], warnings: list[str]) -> dict[str, Any]:
    """Resolve configured fonts and verify that at least one can draw Chinese text."""
    fonts = theme.get("fonts", {})
    requested = [fonts.get("cjk_family"), fonts.get("latin_family"), *fonts.get("fallback", [])]
    available = []
    cjk_capable = []
    for name in filter(None, requested):
        try:
            found = font_manager.findfont(name, fallback_to_default=False)
            if found:
                available.append(name)
                font = font_manager.get_font(found)
                if all(font.get_char_index(ord(character)) for character in "中文"):
                    cjk_capable.append(name)
        except ValueError:
            warnings.append(f"Configured font '{name}' is unavailable; Matplotlib will fall back.")
    if not available:
        warnings.append("No configured fonts are available; Matplotlib default font will be used.")
        available = ["DejaVu Sans"]
    if not cjk_capable:
        warnings.append("No configured available font was verified to contain Chinese glyphs; bilingual labels may be incomplete.")
    return {"requested": [name for name in requested if name], "available": available, "cjk_capable": cjk_capable}


def configure_theme(theme: dict[str, Any], warnings: list[str]) -> dict[str, Any]:
    resolution = resolve_fonts(theme, warnings)
    available = resolution["available"]
    fonts = theme.get("fonts", {})
    sizes = fonts.get("sizes", {})
    plt.rcParams.update({
        "font.family": available,
        "axes.unicode_minus": False,
        "font.size": sizes.get("tick", 8),
        "axes.labelsize": sizes.get("axis_label", 10),
        "axes.titlesize": sizes.get("title", 12),
        "legend.fontsize": sizes.get("legend", 8),
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "text.color": theme.get("canvas", {}).get("foreground", "#202124"),
        "axes.labelcolor": theme.get("axis", {}).get("label_color", theme.get("canvas", {}).get("foreground", "#202124")),
        "axes.titlecolor": theme.get("axis", {}).get("title_color", theme.get("canvas", {}).get("foreground", "#202124")),
        "xtick.color": theme.get("axis", {}).get("tick_color", theme.get("canvas", {}).get("foreground", "#202124")),
        "ytick.color": theme.get("axis", {}).get("tick_color", theme.get("canvas", {}).get("foreground", "#202124")),
    })
    return resolution


def colors(theme: dict[str, Any], count: int) -> list[str]:
    palette = theme.get("palette", {}).get("categorical", ["#0072B2"])
    return [palette[i % len(palette)] for i in range(max(count, 1))]


def style_axis(ax: Any, theme: dict[str, Any]) -> None:
    axis = theme.get("axis", {})
    canvas = theme.get("canvas", {})
    ax.set_facecolor(canvas.get("panel_background", canvas.get("background", "#FFFFFF")))
    for spine in ("top", "right"):
        if spine in ax.spines:
            ax.spines[spine].set_visible(False)
    for spine in ax.spines.values():
        spine.set_linewidth(axis.get("spine_width", 0.8))
        spine.set_color(axis.get("spine_color", canvas.get("foreground", "#202124")))
    if axis.get("grid"):
        ax.grid(axis="both" if axis.get("grid") == "both" else "y", color=axis.get("grid_color", "#D9D9D9"), alpha=float(axis.get("grid_alpha", 1.0)), linewidth=float(axis.get("grid_width", 0.5)), zorder=0)
    ax.tick_params(direction=axis.get("tick_direction", "out"), width=axis.get("spine_width", 0.8), colors=axis.get("tick_color", canvas.get("foreground", "#202124")))


def render_chart(ax: Any, df: pd.DataFrame, figure: dict[str, Any], theme: dict[str, Any], warnings: list[str]) -> None:
    chart, x, y, hue = figure["type"], figure.get("x"), figure.get("y"), figure.get("hue")
    marks = theme.get("marks", {})
    palette = theme.get("palette", {})
    reference_color = palette.get("reference", "#333333")
    alert_color = palette.get("alert", "#D55E00")
    plot_fields = [field for field in [x, y, hue, figure.get("y_lower"), figure.get("y_upper"), figure.get("y_error")] if field]
    plot = df.dropna(subset=plot_fields)
    if chart == "line":
        groups = [("", plot)] if not hue else list(plot.groupby(hue, sort=False))
        for color, (name, group) in zip(colors(theme, len(groups)), groups):
            group = group.sort_values(x)
            ax.plot(group[x], group[y], marker=marks.get("marker", "o"), linewidth=marks.get("line_width", 1.5), markersize=marks.get("marker_size", 3.5), color=color, label=str(name) if hue else None)
            lower, upper = figure.get("y_lower"), figure.get("y_upper")
            if lower and upper:
                ax.fill_between(group[x], group[lower], group[upper], color=color, alpha=float(figure.get("uncertainty_alpha", 0.18)), linewidth=0, label="uncertainty" if not hue else None)
            elif figure.get("y_error"):
                error = pd.to_numeric(group[figure["y_error"]], errors="coerce")
                ax.errorbar(group[x], group[y], yerr=error, fmt="none", ecolor=color, alpha=0.6, capsize=2, linewidth=0.8)
    elif chart == "scatter":
        groups = [("", plot)] if not hue else list(plot.groupby(hue, sort=False))
        for color, (name, group) in zip(colors(theme, len(groups)), groups):
            ax.scatter(group[x], group[y], s=marks.get("scatter_size", 24), alpha=marks.get("marker_alpha", 0.85), color=color, label=str(name) if hue else None, zorder=3)
        if figure.get("regression"):
            coeff = np.polyfit(plot[x], plot[y], deg=1)
            grid = np.linspace(plot[x].min(), plot[x].max(), 100)
            ax.plot(grid, np.polyval(coeff, grid), color=reference_color, linewidth=marks.get("fit_line_width", 1.2), label="OLS fit")
            warnings.append("OLS line shows association only; inspect residuals before model claims.")
    elif chart == "geo-scatter":
        lon, lat, value = figure["longitude"], figure["latitude"], figure.get("value")
        geo = df.dropna(subset=[field for field in (lon, lat, value) if field])
        if value:
            points = ax.scatter(geo[lon], geo[lat], c=geo[value], cmap=palette.get("sequential", "viridis"), s=marks.get("scatter_size", 28), alpha=marks.get("marker_alpha", 0.85), zorder=3)
            ax.figure.colorbar(points, ax=ax, label=figure.get("labels", {}).get("colorbar", value))
        else:
            ax.scatter(geo[lon], geo[lat], color=colors(theme, 1)[0], s=marks.get("scatter_size", 28), alpha=marks.get("marker_alpha", 0.85), zorder=3)
        ax.set_aspect("equal", adjustable="datalim"); ax.set_xlabel(figure.get("labels", {}).get("x", "Longitude")); ax.set_ylabel(figure.get("labels", {}).get("y", "Latitude"))
        warnings.append("This is a coordinate scatter without a basemap or projection transform; do not interpret it as a cartographic map without CRS documentation.")
    elif chart == "hexbin":
        bins = figure.get("gridsize", 28)
        image = ax.hexbin(plot[x], plot[y], gridsize=bins, cmap=palette.get("sequential", "viridis"), mincnt=1, linewidths=0)
        ax.figure.colorbar(image, ax=ax, label=figure.get("labels", {}).get("colorbar", "Count"))
    elif chart == "regression-diagnostics":
        coeff = np.polyfit(plot[x], plot[y], deg=1)
        fitted = np.polyval(coeff, plot[x])
        residuals = plot[y].to_numpy() - fitted
        ax.scatter(fitted, residuals, s=marks.get("scatter_size", 24), alpha=marks.get("marker_alpha", 0.85), color=colors(theme, 1)[0], zorder=3)
        ax.axhline(0, color=reference_color, linewidth=marks.get("fit_line_width", 1.2), linestyle="--")
        ax.set_xlabel(figure.get("labels", {}).get("x", "Fitted value"))
        ax.set_ylabel(figure.get("labels", {}).get("y", "Residual"))
        warnings.append("Residual-versus-fitted display is diagnostic only; review leverage, dependence, scale and model specification before inference.")
    elif chart == "qq":
        values = np.sort(plot[x].to_numpy())
        theoretical = stats.norm.ppf((np.arange(1, len(values) + 1) - 0.5) / len(values))
        slope, intercept, *_ = stats.linregress(theoretical, values)
        ax.scatter(theoretical, values, s=marks.get("scatter_size", 24), alpha=marks.get("marker_alpha", 0.85), color=colors(theme, 1)[0], zorder=3)
        ax.plot(theoretical, intercept + slope * theoretical, color=reference_color, linestyle="--", linewidth=marks.get("fit_line_width", 1.2))
        ax.set_xlabel(figure.get("labels", {}).get("x", "Theoretical normal quantiles")); ax.set_ylabel(figure.get("labels", {}).get("y", "Observed quantiles"))
    elif chart == "leverage":
        coefficients = np.polyfit(plot[x], plot[y], deg=1)
        fitted = np.polyval(coefficients, plot[x])
        residuals = plot[y].to_numpy() - fitted
        centered = plot[x].to_numpy() - plot[x].mean()
        leverage = 1 / len(plot) + centered ** 2 / np.sum(centered ** 2)
        scale = np.sqrt(np.mean(residuals ** 2))
        standardized = residuals / scale if scale > 0 else residuals
        ax.scatter(leverage, standardized, s=marks.get("scatter_size", 24), alpha=marks.get("marker_alpha", 0.85), color=colors(theme, 1)[0], zorder=3)
        ax.axhline(0, color=reference_color, linewidth=marks.get("fit_line_width", 1.2), linestyle="--")
        ax.set_xlabel(figure.get("labels", {}).get("x", "Leverage")); ax.set_ylabel(figure.get("labels", {}).get("y", "Standardized residual"))
        warnings.append("Leverage diagnostic is for a simple one-predictor OLS fit; inspect influence and model specification before inference.")
    elif chart in {"box", "violin", "ecdf"}:
        categories = list(pd.unique(plot[x]))
        grouped = [plot.loc[plot[x] == c, y].to_numpy() for c in categories]
        if chart == "box":
            obj = ax.boxplot(grouped, labels=categories, patch_artist=True, showfliers=True)
            for patch, color in zip(obj["boxes"], colors(theme, len(categories))):
                patch.set_facecolor(color); patch.set_alpha(0.7)
        elif chart == "violin":
            obj = ax.violinplot(grouped, showmedians=True, showextrema=True)
            for body, color in zip(obj["bodies"], colors(theme, len(categories))):
                body.set_facecolor(color); body.set_alpha(0.7)
            ax.set_xticks(range(1, len(categories) + 1), [str(c) for c in categories])
        else:
            for color, category, values in zip(colors(theme, len(categories)), categories, grouped):
                ordered = np.sort(values)
                ax.step(ordered, np.arange(1, len(ordered) + 1) / len(ordered), where="post", color=color, label=str(category))
            ax.set_ylim(0, 1); ax.set_ylabel("Cumulative probability")
    elif chart in {"histogram", "kde"}:
        values = plot[x].to_numpy()
        if chart == "histogram":
            ax.hist(values, bins=figure.get("bins", "auto"), color=colors(theme, 1)[0], alpha=0.8, edgecolor=theme.get("axis", {}).get("spine_color", "#475569"), zorder=3)
            ax.set_ylabel(figure.get("labels", {}).get("y", "Count"))
        else:
            grid = np.linspace(values.min(), values.max(), 200)
            density = stats.gaussian_kde(values, bw_method=figure.get("bandwidth"))(grid)
            ax.plot(grid, density, color=colors(theme, 1)[0], linewidth=marks.get("line_width", 1.5))
            ax.fill_between(grid, density, color=colors(theme, 1)[0], alpha=0.16)
            ax.set_ylabel(figure.get("labels", {}).get("y", "Density"))
    elif chart == "dot":
        categories = list(pd.unique(plot[x]))
        for index, (category, color) in enumerate(zip(categories, colors(theme, len(categories)))):
            values = plot.loc[plot[x] == category, y].to_numpy()
            offsets = np.linspace(-0.11, 0.11, len(values)) if len(values) > 1 else np.array([0.0])
            ax.scatter(np.full(len(values), index) + offsets, values, s=marks.get("scatter_size", 24), alpha=marks.get("marker_alpha", 0.85), color=color, zorder=3)
        ax.set_xticks(range(len(categories)), [str(value) for value in categories])
    elif chart == "paired":
        subject = figure["subject"]
        categories = list(pd.unique(plot[x]))
        positions = {category: index for index, category in enumerate(categories)}
        for _, unit in plot.groupby(subject, sort=False):
            ordered = unit.set_index(x).loc[categories]
            ax.plot(range(len(categories)), ordered[y].to_numpy(), color=theme.get("palette", {}).get("reference", "#6B7280"), alpha=0.42, linewidth=marks.get("line_width", 1.2), zorder=2)
            ax.scatter(range(len(categories)), ordered[y].to_numpy(), s=marks.get("scatter_size", 24), color=colors(theme, 1)[0], alpha=marks.get("marker_alpha", 0.85), zorder=3)
        ax.set_xticks(range(len(categories)), [str(value) for value in categories])
    elif chart == "bar":
        statistic = figure.get("statistic", "mean")
        aggregator = {"mean": "mean", "sum": "sum", "count": "count"}.get(statistic)
        if not aggregator:
            raise SpecificationError("bar statistic must be mean, sum, or count.")
        if hue:
            pivot = plot.pivot_table(index=x, columns=hue, values=y, aggfunc=aggregator, observed=True)
            positions = np.arange(len(pivot)); width = 0.8 / max(1, len(pivot.columns))
            for idx, (name, series) in enumerate(pivot.items()):
                ax.bar(positions + (idx - (len(pivot.columns)-1)/2)*width, series, width, color=colors(theme, len(pivot.columns))[idx], label=str(name), zorder=3)
            ax.set_xticks(positions, [str(v) for v in pivot.index])
        else:
            summary = plot.groupby(x, observed=True)[y].agg(aggregator)
            ax.bar(np.arange(len(summary)), summary.values, color=colors(theme, len(summary)), zorder=3)
            ax.set_xticks(np.arange(len(summary)), [str(v) for v in summary.index])
    elif chart == "stacked-bar":
        statistic = figure.get("statistic", "sum")
        aggregator = {"mean": "mean", "sum": "sum", "count": "count"}.get(statistic)
        if not aggregator:
            raise SpecificationError("stacked-bar statistic must be mean, sum, or count.")
        pivot = plot.pivot_table(index=x, columns=hue, values=y, aggfunc=aggregator, observed=True).fillna(0)
        positions = np.arange(len(pivot))
        bottom = np.zeros(len(pivot))
        for color, (name, series) in zip(colors(theme, len(pivot.columns)), pivot.items()):
            ax.bar(positions, series.to_numpy(), bottom=bottom, color=color, label=str(name), zorder=3)
            bottom += series.to_numpy()
        ax.set_xticks(positions, [str(value) for value in pivot.index])
    elif chart == "heatmap":
        value = figure["value"]
        matrix = plot.pivot_table(index=y, columns=x, values=value, aggfunc=figure.get("statistic", "mean"), observed=True)
        image = ax.imshow(matrix.to_numpy(), cmap=theme.get("palette", {}).get("sequential", "viridis"), aspect="auto")
        ax.set_xticks(range(len(matrix.columns)), [str(v) for v in matrix.columns], rotation=45, ha="right")
        ax.set_yticks(range(len(matrix.index)), [str(v) for v in matrix.index])
        ax.figure.colorbar(image, ax=ax, label=figure.get("labels", {}).get("colorbar", value))
    elif chart == "correlation":
        variables = figure.get("variables") or [column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])]
        matrix = df[variables].corr()
        image = ax.imshow(matrix.to_numpy(), cmap=palette.get("diverging", "RdBu_r"), vmin=-1, vmax=1, aspect="equal")
        ax.set_xticks(range(len(variables)), variables, rotation=45, ha="right")
        ax.set_yticks(range(len(variables)), variables)
        if figure.get("annotate", len(variables) <= 12):
            for row in range(len(variables)):
                for column in range(len(variables)):
                    value = matrix.iloc[row, column]
                    ax.text(column, row, f"{value:.2f}", ha="center", va="center", fontsize=theme.get("fonts", {}).get("sizes", {}).get("table", 7), color=theme.get("canvas", {}).get("foreground", "#202124"))
        ax.figure.colorbar(image, ax=ax, label=figure.get("labels", {}).get("colorbar", "Pearson r"))
    elif chart == "pca":
        variables = figure["variables"]
        pca_frame = df[variables + ([hue] if hue else [])].dropna()
        matrix = pca_frame[variables].to_numpy()
        standardized = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0, ddof=0)
        if np.any(~np.isfinite(standardized)):
            raise SpecificationError("pca requires feature variables with nonzero variance.")
        scores = PCA(n_components=2).fit_transform(standardized)
        if hue:
            labels = pca_frame[hue].reset_index(drop=True)
            for color, name in zip(colors(theme, labels.nunique()), pd.unique(labels)):
                indices = np.flatnonzero(labels.to_numpy() == name)
                ax.scatter(scores[indices, 0], scores[indices, 1], s=marks.get("scatter_size", 24), alpha=marks.get("marker_alpha", 0.85), color=color, label=str(name), zorder=3)
        else:
            ax.scatter(scores[:, 0], scores[:, 1], s=marks.get("scatter_size", 24), alpha=marks.get("marker_alpha", 0.85), color=colors(theme, 1)[0], zorder=3)
        ax.set_xlabel(figure.get("labels", {}).get("x", "PC1")); ax.set_ylabel(figure.get("labels", {}).get("y", "PC2"))
        if hue: ax.legend(frameon=bool(theme.get("legend", {}).get("frame", False)), loc=theme.get("legend", {}).get("location", "best"))
        warnings.append("PCA is exploratory; report feature scaling, stability and loading interpretation separately.")
    elif chart in {"roc", "pr"}:
        actual, score = figure["actual"], figure["score"]
        subset = df[[actual, score]].dropna()
        positive = figure.get("positive_value", sorted(pd.unique(subset[actual]))[-1])
        truth = (subset[actual] == positive).astype(int)
        if chart == "roc":
            first, second, _ = roc_curve(truth, subset[score])
            ax.plot(first, second, color=colors(theme, 1)[0], linewidth=marks.get("line_width", 1.8), label=f"AUC = {auc(first, second):.3f}")
            ax.plot([0, 1], [0, 1], color=reference_color, linestyle="--", linewidth=1)
            ax.set_xlabel(figure.get("labels", {}).get("x", "False positive rate")); ax.set_ylabel(figure.get("labels", {}).get("y", "True positive rate"))
        else:
            precision, recall, _ = precision_recall_curve(truth, subset[score])
            ax.plot(recall, precision, color=colors(theme, 1)[0], linewidth=marks.get("line_width", 1.8), label=f"AP area = {auc(recall, precision):.3f}")
            ax.set_xlabel(figure.get("labels", {}).get("x", "Recall")); ax.set_ylabel(figure.get("labels", {}).get("y", "Precision"))
        ax.legend(frameon=bool(theme.get("legend", {}).get("frame", False)), loc=theme.get("legend", {}).get("location", "best"))
    elif chart == "confusion":
        actual, predicted = figure["actual"], figure["predicted"]
        subset = df[[actual, predicted]].dropna(); classes = list(pd.unique(pd.concat([subset[actual], subset[predicted]])))
        matrix = confusion_matrix(subset[actual], subset[predicted], labels=classes)
        image = ax.imshow(matrix, cmap=palette.get("sequential", "viridis"), aspect="equal")
        ax.set_xticks(range(len(classes)), [str(value) for value in classes], rotation=45, ha="right"); ax.set_yticks(range(len(classes)), [str(value) for value in classes])
        ax.set_xlabel(figure.get("labels", {}).get("x", "Predicted class")); ax.set_ylabel(figure.get("labels", {}).get("y", "Observed class"))
        for row in range(len(classes)):
            for column in range(len(classes)):
                ax.text(column, row, str(matrix[row, column]), ha="center", va="center", color=theme.get("canvas", {}).get("foreground", "#202124"))
        ax.figure.colorbar(image, ax=ax, label="Count")
    elif chart == "candlestick":
        subset = df.dropna(subset=[figure[key] for key in ("x", "open", "high", "low", "close")]).sort_values(figure["x"])
        positions = np.arange(len(subset)); width = float(figure.get("body_width", 0.62))
        for position, (_, row) in zip(positions, subset.iterrows()):
            opened, high, low, closed = [float(row[figure[key]]) for key in ("open", "high", "low", "close")]
            rising = closed >= opened; color = colors(theme, 1)[0] if rising else palette.get("alert", "#B42318")
            ax.vlines(position, low, high, color=color, linewidth=0.9, zorder=2)
            ax.add_patch(plt.Rectangle((position - width / 2, min(opened, closed)), width, max(abs(closed - opened), 1e-12), facecolor=color, edgecolor=color, alpha=0.82, zorder=3))
        ax.set_xticks(positions[::max(1, len(positions) // 8)], [str(value) for value in subset[figure["x"]].iloc[::max(1, len(positions) // 8)]], rotation=30, ha="right")
        ax.set_ylabel(figure.get("labels", {}).get("y", "Price")); warnings.append("Candlestick interpretation requires documented time ordering, market session and OHLC provenance.")
    elif chart == "waterfall":
        summary = plot.groupby(x, observed=True)[y].sum()
        positions = np.arange(len(summary)); cumulative = summary.cumsum().shift(fill_value=0)
        bar_colors = [colors(theme, 1)[0] if value >= 0 else alert_color for value in summary.to_numpy()]
        ax.bar(positions, summary.to_numpy(), bottom=cumulative.to_numpy(), color=bar_colors, zorder=3)
        ax.set_xticks(positions, [str(value) for value in summary.index], rotation=30, ha="right")
        ax.set_ylabel(figure.get("labels", {}).get("y", y)); warnings.append("Waterfall assumes additive increments on a common scale; verify no double-counting before interpretation.")
    elif chart == "bubble":
        size_field = figure.get("size")
        bubble = plot.dropna(subset=[x, y, size_field])
        sizes = pd.to_numeric(bubble[size_field], errors="coerce").clip(lower=0)
        sizes = 30 + 220 * sizes / max(float(sizes.max()), 1e-12)
        ax.scatter(bubble[x], bubble[y], s=sizes, c=colors(theme, 1)[0], alpha=marks.get("marker_alpha", 0.7), edgecolors="white", linewidths=0.4, zorder=3)
        warnings.append("Bubble area is a visual encoding; report the size field and its unit explicitly.")
    elif chart == "surface3d":
        surface = df[[figure["x"], figure["y"], figure["z"]]].dropna()
        ax.plot_trisurf(surface[figure["x"]], surface[figure["y"]], surface[figure["z"]], cmap=palette.get("sequential", "viridis"), linewidth=0.15, antialiased=True, alpha=0.88)
        ax.set_xlabel(figure.get("labels", {}).get("x", figure["x"])); ax.set_ylabel(figure.get("labels", {}).get("y", figure["y"])); ax.set_zlabel(figure.get("labels", {}).get("z", figure["z"]))
        warnings.append("3D surfaces can occlude values and exaggerate slopes; use only when the spatial surface semantics and sampling grid are documented.")
    elif chart == "polar-heatmap":
        subset = df[[figure["theta"], figure["radius"], figure["value"]]].dropna()
        theta_values = np.sort(subset[figure["theta"]].unique()); radius_values = np.sort(subset[figure["radius"]].unique())
        matrix = subset.pivot_table(index=figure["radius"], columns=figure["theta"], values=figure["value"], aggfunc="mean").reindex(index=radius_values, columns=theta_values)
        theta_edges = np.linspace(0, 2 * np.pi, len(theta_values) + 1); radius_edges = np.linspace(0, 1, len(radius_values) + 1)
        image = ax.pcolormesh(theta_edges, radius_edges, matrix.to_numpy(), cmap=palette.get("sequential", "viridis"), shading="auto")
        ax.figure.colorbar(image, ax=ax, label=figure.get("labels", {}).get("colorbar", figure["value"]))
        warnings.append("Polar heatmap maps ordered angular bins to equal sectors; document angle units and ordering.")
    elif chart == "radial-bubble":
        subset = df[[figure["theta"], figure["radius"], figure["size"]]].dropna()
        theta = pd.to_numeric(subset[figure["theta"]], errors="coerce").to_numpy(); radius = pd.to_numeric(subset[figure["radius"]], errors="coerce").to_numpy(); size = pd.to_numeric(subset[figure["size"]], errors="coerce").clip(lower=0).to_numpy()
        sizes = 25 + 220 * size / max(float(size.max()), 1e-12)
        ax.scatter(theta, radius, s=sizes, color=colors(theme, 1)[0], alpha=marks.get("marker_alpha", 0.75), edgecolors="white", linewidths=0.4)
        warnings.append("Radial bubble area is an approximate visual encoding; report the size variable and units.")
    elif chart == "population-pyramid":
        subset = df[[figure["category"], figure["left"], figure["right"]]].dropna(); positions = np.arange(len(subset))
        ax.barh(positions, -subset[figure["left"]].to_numpy(), color=colors(theme, 1)[0], alpha=0.85, label=str(figure["left"]))
        ax.barh(positions, subset[figure["right"]].to_numpy(), color=colors(theme, 2)[1], alpha=0.85, label=str(figure["right"]))
        ax.set_yticks(positions, [str(value) for value in subset[figure["category"]]]); ax.axvline(0, color=reference_color, linewidth=0.8)
        ax.legend(frameon=bool(theme.get("legend", {}).get("frame", False)), loc=theme.get("legend", {}).get("location", "best"))
        warnings.append("Population-pyramid sides must share a denominator and category ordering; confirm whether values are counts or rates.")
    elif chart == "connected-bar":
        ordered = plot.sort_values(x); positions = np.arange(len(ordered)); values = ordered[y].to_numpy()
        ax.bar(positions, values, color=colors(theme, 1)[0], alpha=0.75, zorder=2); ax.plot(positions, values, color=reference_color, marker=marks.get("marker", "o"), linewidth=marks.get("line_width", 1.4), zorder=3)
        ax.set_xticks(positions, [str(value) for value in ordered[x]], rotation=30, ha="right")
        warnings.append("Connected bars imply an ordered category sequence; do not use for unordered groups.")
    elif chart in {"waterfall-lines", "xrd-waterfall", "xps-waterfall", "color-waterfall"}:
        series_field = figure.get("series")
        groups = [(None, plot)] if not series_field else list(plot.groupby(series_field, sort=False))
        for color, (name, group) in zip(colors(theme, len(groups)), groups):
            ordered = group.sort_values(x)
            ax.plot(ordered[x], ordered[y], color=color, linewidth=marks.get("line_width", 1.3), label=str(name) if name is not None else None)
        if series_field:
            ax.legend(frameon=bool(theme.get("legend", {}).get("frame", False)), loc=theme.get("legend", {}).get("location", "best"))
        warnings.append("Waterfall-line displays require documented series offsets/baseline and domain-specific x-axis units; no 3D perspective is implied.")
    elif chart == "floating-bar3d":
        subset = df[[figure["x"], figure["y"], figure["z"]]].dropna(); dx = float(figure.get("dx", 0.65)); dy = float(figure.get("dy", 0.65))
        ax.bar3d(subset[figure["x"]], subset[figure["y"]], np.zeros(len(subset)), dx, dy, subset[figure["z"]], color=colors(theme, 1)[0], alpha=0.82, shade=True)
        ax.set_xlabel(figure.get("labels", {}).get("x", figure["x"])); ax.set_ylabel(figure.get("labels", {}).get("y", figure["y"])); ax.set_zlabel(figure.get("labels", {}).get("z", figure["z"]))
        warnings.append("Floating 3D bars can occlude magnitude; document bar base, axis units and viewing angle before interpretation.")
    elif chart == "chord":
        subset = df[[figure["source"], figure["target"], figure["value"]]].dropna(); nodes = list(pd.unique(pd.concat([subset[figure["source"]], subset[figure["target"]]]))); positions = {node: (np.cos(angle), np.sin(angle)) for node, angle in zip(nodes, np.linspace(0, 2 * np.pi, len(nodes), endpoint=False))}
        for _, row in subset.iterrows():
            source, target = positions[row[figure["source"]]], positions[row[figure["target"]]]
            width = 0.5 + 2.5 * float(row[figure["value"]]) / max(float(subset[figure["value"]].max()), 1e-12)
            ax.plot([source[0], target[0]], [source[1], target[1]], color=colors(theme, 1)[0], alpha=0.35, linewidth=width)
        for color, node in zip(colors(theme, len(nodes)), nodes):
            point = positions[node]; ax.scatter([point[0]], [point[1]], s=60, color=color, zorder=3); ax.text(point[0] * 1.1, point[1] * 1.1, str(node), ha="center", va="center")
        ax.set_aspect("equal", adjustable="box"); ax.axis("off")
        warnings.append("Chord links show association only; direction, normalization, self-links and thresholding must be documented.")
    elif chart == "pareto":
        summary = plot.groupby(x, observed=True)[y].sum().sort_values(ascending=False)
        cumulative = summary.cumsum() / summary.sum() * 100
        positions = np.arange(len(summary))
        ax.bar(positions, summary.values, color=colors(theme, len(summary)), zorder=3)
        ax.set_xticks(positions, [str(v) for v in summary.index], rotation=30, ha="right")
        second = ax.twinx()
        second.plot(positions, cumulative.values, color=reference_color, marker=marks.get("marker", "o"), linewidth=marks.get("line_width", 1.4))
        second.set_ylim(0, 105); second.set_ylabel("Cumulative percentage (%)")
        second.tick_params(colors=theme.get("axis", {}).get("tick_color", theme.get("canvas", {}).get("foreground", "#202124")))
        second.yaxis.label.set_color(theme.get("axis", {}).get("label_color", theme.get("canvas", {}).get("foreground", "#202124")))
    elif chart == "control":
        ordered = plot.sort_values(x)
        mean, sigma = ordered[y].mean(), ordered[y].std(ddof=1)
        ax.plot(ordered[x], ordered[y], marker=marks.get("marker", "o"), markersize=marks.get("marker_size", 3.5), linewidth=marks.get("line_width", 1.2), color=colors(theme, 1)[0], zorder=3)
        for value, label, color in [(mean, "Center", reference_color), (mean + 3*sigma, "UCL", alert_color), (mean - 3*sigma, "LCL", alert_color)]:
            ax.axhline(value, color=color, linestyle="--", linewidth=1, label=label)
    style_axis(ax, theme)
    labels = figure.get("labels", {})
    ax.set_title(labels.get("title", ""), pad=10)
    if chart not in {"regression-diagnostics", "correlation", "pca", "roc", "pr", "confusion", "qq", "leverage", "geo-scatter", "candlestick", "surface3d", "floating-bar3d", "polar-heatmap", "radial-bubble", "population-pyramid", "chord"}:
        ax.set_xlabel(labels.get("x", x))
    if chart not in {"ecdf", "histogram", "kde", "regression-diagnostics", "pca", "roc", "pr", "confusion", "qq", "leverage", "geo-scatter", "candlestick", "surface3d", "floating-bar3d", "polar-heatmap", "radial-bubble", "population-pyramid", "chord"}:
        ax.set_ylabel(labels.get("y", y))
    if hue or chart in {"ecdf", "control", "stacked-bar"} or (chart == "scatter" and figure.get("regression")):
        legend = theme.get("legend", {})
        ax.legend(frameon=bool(legend.get("frame", False)), loc=legend.get("location", "best"))


def add_table(ax: Any, df: pd.DataFrame, figure: dict[str, Any], theme: dict[str, Any]) -> None:
    settings = figure.get("table", {})
    if not settings.get("enabled", False):
        return
    columns = settings.get("columns") or [figure.get("x"), figure.get("y")]
    columns = [c for c in columns if c]
    table = ax.table(cellText=df[columns].head(int(settings.get("max_rows", 8))).values,
                     colLabels=columns if settings.get("header", theme.get("table", {}).get("header", True)) else None,
                     loc="bottom", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(settings.get("font_size", theme.get("table", {}).get("font_size", 7)))
    table_style = theme.get("table", {})
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor(table_style.get("edge_color", "#B0B0B0"))
        cell.set_linewidth(float(table_style.get("edge_width", 0.5)))
        cell.set_facecolor(table_style.get("header_background", "#F3F4F6") if row == 0 else table_style.get("cell_background", "#FFFFFF"))
        cell.get_text().set_color(table_style.get("text_color", theme.get("canvas", {}).get("foreground", "#202124")))
    ax.figure.subplots_adjust(bottom=0.26)


def add_statistics_annotation(ax: Any, spec: dict[str, Any], theme: dict[str, Any]) -> None:
    """Render only a user-confirmed method/result; never infer or manufacture a result."""
    statistics = spec.get("statistics")
    if not statistics:
        return
    if statistics.get("confirmed") is not True:
        raise SpecificationError("statistics requires confirmed: true before it may appear in a figure.")
    method_id = statistics.get("method_id")
    catalogue_path = Path(__file__).resolve().parents[1] / "assets" / "math-method-catalogue.yaml"
    catalogue = read_mapping(catalogue_path)
    method = next((item for category in catalogue["categories"] for item in category["methods"] if item["id"] == method_id), None)
    if method is None:
        raise SpecificationError(f"Unknown statistics.method_id: {method_id}")
    annotation = statistics.get("annotation", {})
    if annotation.get("enabled", True) is False:
        return
    text = annotation.get("text")
    if not text:
        results = statistics.get("results", {})
        items = [f"{key}={value}" for key, value in results.items()]
        text = method["label"] + ("; " + ", ".join(items) if items else "")
    location = annotation.get("location", "title-subtitle")
    if location == "title-subtitle":
        ax.set_title(ax.get_title(), pad=30)
        ax.text(0.5, 1.015, text, transform=ax.transAxes, va="bottom", ha="center",
                fontsize=annotation.get("font_size", theme.get("fonts", {}).get("sizes", {}).get("annotation", 8)),
                color=annotation.get("color", theme.get("annotation", {}).get("text_color", theme.get("canvas", {}).get("foreground", "#202124"))), clip_on=False)
        return
    locations = {"top-left": (0.01, 0.98, "left"), "top-right": (0.99, 0.98, "right"), "bottom-left": (0.01, 0.02, "left")}
    x, y, alignment = locations.get(location, locations["top-left"])
    annotation_theme = theme.get("annotation", {})
    ax.text(x, y, text, transform=ax.transAxes, va="top" if y > 0.5 else "bottom", ha=alignment,
            fontsize=annotation.get("font_size", theme.get("fonts", {}).get("sizes", {}).get("annotation", 8)),
            color=annotation.get("color", annotation_theme.get("text_color", theme.get("canvas", {}).get("foreground", "#202124"))),
            bbox={"facecolor": annotation.get("background", annotation_theme.get("background", "#FFFFFF")), "edgecolor": annotation.get("edge_color", annotation_theme.get("edge_color", "#B0B0B0")), "alpha": float(annotation.get("alpha", annotation_theme.get("alpha", 0.9))), "pad": 3})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    warnings: list[str] = []
    report: dict[str, Any] = {"status": "failed", "warnings": warnings, "errors": []}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    try:
        spec_path = args.spec.resolve()
        spec = read_mapping(spec_path)
        if spec.get("version") != 1:
            raise SpecificationError("Only version: 1 figure specifications are supported.")
        theme_cfg = spec.get("theme", {})
        theme_path = resolve(str(theme_cfg.get("path", "")), spec_path.parent)
        theme = read_mapping(theme_path)
        theme = deep_merge(theme, spec.get("style", {}).get("overrides", {}))
        report["theme"] = {"name": theme.get("name", theme_path.stem), "path": str(theme_path), "has_local_overrides": bool(spec.get("style", {}).get("overrides", {}))}
        frame, source = load_data(spec.get("data", {}), spec_path.parent)
        report["provenance"] = {
            "spec_sha256": sha256_file(spec_path),
            "theme_sha256": sha256_file(theme_path),
            "data_sha256": sha256_file(source),
            "renderer_sha256": sha256_file(Path(__file__).resolve()),
        }
        frame = apply_transforms(frame, spec.get("analysis", {}).get("transforms", []), warnings)
        figure = spec.get("figure", {})
        errors = validate(frame, figure, theme, warnings, spec.get("statistics"), spec_path.parent)
        report.update({"source": str(source), "rows_after_transforms": int(len(frame)), "errors": errors})
        if errors:
            raise SpecificationError("; ".join(errors))
        if args.validate_only:
            report["status"] = "valid"
        else:
            report["font_resolution"] = configure_theme(theme, warnings)
            canvas = theme.get("canvas", {})
            if figure.get("type") == "multi-panel":
                panels = figure["panels"]
                ncols = int(figure.get("columns", min(2, len(panels))))
                nrows = int(np.ceil(len(panels) / ncols))
                fig, axes = plt.subplots(nrows, ncols, figsize=(canvas.get("width_in", 6.5), canvas.get("height_in", 4.2) * nrows / 2), dpi=canvas.get("dpi", 300), squeeze=False)
                axes_flat = list(axes.ravel())
                for panel, panel_ax in zip(panels, axes_flat):
                    render_chart(panel_ax, frame, panel, theme, warnings)
                for panel_ax in axes_flat[len(panels):]:
                    panel_ax.set_visible(False)
                ax = axes_flat[0]
            elif figure.get("type") == "surface3d":
                fig = plt.figure(figsize=(canvas.get("width_in", 6.5), canvas.get("height_in", 4.2)), dpi=canvas.get("dpi", 300))
                ax = fig.add_subplot(111, projection="3d")
            elif figure.get("type") == "floating-bar3d":
                fig = plt.figure(figsize=(canvas.get("width_in", 6.5), canvas.get("height_in", 4.2)), dpi=canvas.get("dpi", 300))
                ax = fig.add_subplot(111, projection="3d")
            elif figure.get("type") in {"polar-heatmap", "radial-bubble"}:
                fig = plt.figure(figsize=(canvas.get("width_in", 6.5), canvas.get("height_in", 4.2)), dpi=canvas.get("dpi", 300))
                ax = fig.add_subplot(111, projection="polar")
            else:
                fig, ax = plt.subplots(figsize=(canvas.get("width_in", 6.5), canvas.get("height_in", 4.2)), dpi=canvas.get("dpi", 300))
            fig.patch.set_facecolor(canvas.get("background", "#FFFFFF"))
            if figure.get("type") != "multi-panel":
                render_chart(ax, frame, figure, theme, warnings)
                add_statistics_annotation(ax, spec, theme)
                add_table(ax, frame, figure, theme)
            fig.tight_layout()
            stem = spec.get("output", {}).get("stem", "figure")
            formats = spec.get("output", {}).get("formats", ["png", "svg", "pdf"])
            rendered = []
            for extension in formats:
                if extension not in {"png", "svg", "pdf"}:
                    raise SpecificationError(f"Unsupported export format: {extension}")
                destination = args.output_dir / f"{stem}.{extension}"
                fig.savefig(destination, dpi=canvas.get("dpi", 300), bbox_inches="tight", facecolor=fig.get_facecolor())
                rendered.append(str(destination))
            plt.close(fig)
            report.update({"status": "rendered", "outputs": rendered, "visual_qa": audit_paths([Path(path) for path in rendered], min_dpi=int(canvas.get("dpi", 300)))})
        (args.output_dir / "resolved-spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
    except Exception as exc:  # report failures for auditability
        report["errors"] = list(dict.fromkeys(report["errors"] + [str(exc)]))
    (args.output_dir / "render-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] == "failed":
        sys.exit(2)


if __name__ == "__main__":
    main()
