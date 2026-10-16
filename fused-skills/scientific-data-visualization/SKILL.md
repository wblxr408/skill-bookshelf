---
name: scientific-data-visualization
description: Analyze data and create reproducible publication figures with appropriate chart choice, statistical evidence, journal sizing, and visual QA.
metadata:
  version: "fusion-2026-10-05"
---

# Scientific Data Visualization — unified scientific figures

Read [the execution contract](references/fusion-policy.md). Establish the analytical question from supplied context; profile unknown data once before choosing a chart. Reuse documented units, groups, pairing, experimental unit, missingness, and sample sizes. Do not treat a numeric ID as a measurement or a plot as causal/significance evidence.

| Need | Read next |
|---|---|
| Reproducible specification, gallery routing, chart catalogue, machine render report, or statistical eligibility | [reproducible figures](references/reproducible-figures.md), then [reproducible module](modules/reproducible/PLAYBOOK.md) |
| Journal sizing, Chinese fonts, publication recipes, multipanel layout, gray-scale preview, or custom Matplotlib construction | [publication figures](references/publication-figures.md), then [publication module](modules/publication/PLAYBOOK.md) |

Select one profiling route and one rendering route. Add the other module only for a concrete capability gap; do not independently profile or redraw the same data twice. Both modules' scripts, gallery, themes, statistical decision packets, journal guidance, and visual QA remain available.

Infer a pure descriptive task when no inferential statistics are requested. When inference is needed, establish design and method assumptions; use the statistical eligibility packet and confirmed method before annotating inferred results. Ask only for material missing assumptions, not a routine statistics opt-in for every chart.

Use final display dimensions, readable fonts with CJK fallback, colorblind-safe colors plus redundant encoding, truthful scales, and explicit uncertainty type/sample size. Prefer individual observations for small samples. Materially misleading requested charts require a concise explanation and appropriate alternative. Use existing uncertainty only as labeled; do not invent a test or significance.

Inspect the render report and a batched visual preview, correct actual defects, then export the requested vector/raster formats. Keep data reference, code/specification, renderer version, and QA evidence together. Interactive explanatory visuals remain `$visualize`.
