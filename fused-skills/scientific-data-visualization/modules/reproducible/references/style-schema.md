# Theme and typography schema

Use one named theme per project. A theme is the sole source of defaults; `style.overrides` is reserved for documented figure-specific needs.

```yaml
name: journal-bilingual
canvas: {width_in: 6.5, height_in: 4.2, dpi: 300, background: "#FFFFFF", panel_background: "#FFFFFF", foreground: "#202124"}
fonts:
  cjk_family: Microsoft YaHei
  latin_family: Arial
  fallback: [Noto Sans CJK SC, DejaVu Sans]
  sizes: {title: 12, axis_label: 10, tick: 8, legend: 8, annotation: 8, table: 7}
palette:
  categorical: ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
  sequential: viridis
  diverging: RdBu_r
  reference: "#4B5563"
  alert: "#B42318"
axis: {spine_width: 0.8, spine_color: "#475569", grid: y-major-light, grid_color: "#D9E0E8", grid_alpha: 0.8, grid_width: 0.5, tick_direction: out, tick_color: "#334155", label_color: "#1F2937", title_color: "#111827"}
legend: {frame: false, location: best}
marks: {marker: o, marker_size: 3.5, marker_alpha: 0.85, scatter_size: 24, line_width: 1.5, fit_line_width: 1.2}
annotation: {background: "#FFFFFF", edge_color: "#B0B0B0", text_color: "#202124", alpha: 0.9}
table: {header: true, font_size: 7, header_background: "#F3F4F6", cell_background: "#FFFFFF", edge_color: "#B0B0B0", edge_width: 0.5, text_color: "#202124"}
```

Specify `labels.locale` as `zh`, `en`, or `bilingual`. Supply the label text yourself; locale selects typography and QA rules rather than performing unreliable translation.

At render time, `render-report.json.font_resolution` records the requested and actually available font families, plus the families verified to contain the Chinese probe glyphs `中文`. If `cjk_capable` is empty, treat bilingual output as unfinished even if the image file was generated.

### Palette rules

Use categorical colors for unordered groups, sequential palettes for ordered magnitude, diverging palettes only around a meaningful center, and a neutral color for reference or non-selected series. Keep semantic colors stable across all figures in one project. Never encode more categories than the configured palette can distinguish without an explicit override.

### Token rules

`canvas` controls the figure and axes surfaces; `axis` controls visible axes,
ticks, spines and grids; `palette.reference` and `palette.alert` control fitted,
baseline and warning marks; and `marks`, `annotation`, and `table` control the
geometry, foreground, background and borders of their matching chart elements.
The renderer must use these tokens rather than literal presentation colors.

### Text rules

Define title, x label, y label, legend title, units, and optional table headers in `figure.labels`. Use sentence case for English labels unless the target venue requires otherwise. Use an axis title with units in parentheses, for example `Mean latency (ms)` or `平均延迟（ms）`.
