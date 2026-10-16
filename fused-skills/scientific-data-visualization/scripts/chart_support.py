"""Single lightweight registry for chart forms implemented by the renderer.

The reference catalogue is intentionally broader than the current renderer.
Consumers must use this module rather than infer support from a visual match or
duplicate a local set of chart IDs.
"""
from __future__ import annotations


SUPPORTED = frozenset({
    "line", "scatter", "hexbin", "regression-diagnostics", "qq", "leverage",
    "bar", "stacked-bar", "dot", "paired", "box", "violin", "ecdf",
    "histogram", "kde", "heatmap", "correlation", "pca", "roc", "pr",
    "confusion", "geo-scatter", "candlestick", "waterfall", "waterfall-lines",
    "xrd-waterfall", "xps-waterfall", "color-waterfall", "bubble", "surface3d",
    "floating-bar3d", "polar-heatmap", "radial-bubble", "population-pyramid",
    "connected-bar", "chord", "pareto", "control", "multi-panel",
})


def support_status(chart_id: str) -> str:
    """Return a public boundary label suitable for compact retrieval packets."""
    return "renderable" if chart_id in SUPPORTED else "reference-only"
