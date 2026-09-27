---
name: scientific-data-visualization
description: Create reproducible, publication-ready scientific and engineering data-analysis figures from CSV or XLSX data. Use for data profiling, chart recommendation, statistical plots and fits, time-series, Pareto and control charts, bilingual typography, detailed palette and layout configuration, or PNG/SVG/PDF export with auditable quality checks.
---

# Scientific Data Visualization

Create defensible figures through **inspect -> choose -> specify -> render -> verify**. Preserve the data, figure specification, render report, and output files together. Do not claim statistical or visual validity until the quality report has been checked.

## Progressive loading

Read only the reference needed for the user request. Never load the whole reference library.

| Need | Read |
| --- | --- |
| Any new dataset or unclear columns | `references/data-contract.md` |
| Theme, color, typography, labels, legends, tables | `references/style-schema.md` |
| Choosing a plot or applying a statistical method | `references/chart-catalog.md` |
| AI multi-dimensional chart/statistics recommendation | `references/ai-recommendation-protocol.md` |
| Render errors, review, or publication export | `references/quality-gates.md` |
| Full end-to-end workflow or CLI usage | `references/workflow.md` |
| Browse the collected Origin-style references | `references/gallery-routing.md` |

## Required workflow

1. Run `scripts/inspect_data.py` before choosing a plot when data semantics are not already documented.
2. Read `references/ai-recommendation-protocol.md` before any chart or statistics recommendation. Ask “是否需要统计方法？” unless the user has explicitly opted in or out. Profile data first, collect research goal, outcome type, independent/paired/repeated design, named outcome/group columns, experimental unit, independence/missingness/outlier reviews, and—when continuous inference is requested—the smallest meaningful standardized effect size plus target power. Run `scripts/recommend_statistics.py`; pass its compact decision packet to AI, not raw data. Use the required three-tier output: `首选`, `待确认候选`, and `不适用`. Only a local `status: eligible` packet may be described as verified; conditional methods must name their missing assumption and may not produce inferred results.
3. State the analytical question and recommend up to three appropriate renderable chart families with their trade-offs. Use the route packet plus distribution, sample-size, outlier, zero-mass, correlation, time, pairing, and category-cardinality facts. Treat router output as a visual candidate list until units, experimental unit, grouping, pairing, and ordering are confirmed; never treat it as a statistical recommendation. Respect an explicitly requested chart type, but surface material risks.
4. Query the math method catalogue by name/role/data shape without formulas. Full formulas are not needed for recommendation and must remain out of context. Load formula context only when both the user has confirmed one `method_id` and explicitly needs explanation, derivation, or custom computation (`--confirmed --include-formula`); current source images provide no formula sidecars, so never invent them.
5. Create a versioned YAML/JSON figure specification. Use a named theme; record every local style override in the specification. Add `statistics.confirmed: true` only after method confirmation and include the verified result to annotate the figure.
6. Run `scripts/render_figure.py`. It creates image files plus `render-report.json` containing data and visual QA results.
7. Inspect the report and rendered output before declaring the figure complete. Report failed gates as bugs or unfinished work.

## Reference-gallery routing

Treat `figures/` as a visual reference corpus, not as generated examples. Never load the complete catalogue into context. Route in three stages:

1. Read `references/gallery-routing.md` only to select a **major family**.
2. Run `scripts/query_gallery.py --category <major-family>` or `--search <phrase>` to list only **minor families** or short candidate records.
3. Run `scripts/query_gallery.py --type-id <id>` for the compact exact record. Add `--detail` only for final selection, ambiguous recognition, or implementation.
4. For ambiguous visual matches, resolve a returned evidence ID with `--source-id src-XX` and inspect that one original screenshot before deciding.

## Prompt-and-table routing

When the runtime input is only a table plus a human prompt, do not inspect the reference screenshots. Build the local index once with `scripts/build_gallery_index.py`, then run:

```powershell
python scripts/route_from_prompt.py data.xlsx --sheet Sheet1 --prompt "比较不同处理组的分布，优先显示离群值" 
```

The router uses local `rg` retrieval over a line-oriented index, then rejects chart types incompatible with the actual column profile. It returns at most three compact candidates. Rebuild the index after catalogue edits. If a new PNG appears in `figures/` without a catalogue mapping, `build_gallery_index.py --check` must fail; classify it before using it as evidence.

If the desired type is absent, report it as absent instead of pretending that a visually similar type is an exact reference match.

## Tool contract

```powershell
python scripts/inspect_data.py data/measurements.xlsx --sheet Sheet1 --output artifacts/data-profile.json
python scripts/render_figure.py specs/pareto.yaml --output-dir artifacts/pareto
```

Use `--validate-only` to check a specification without rendering. Keep the specification, its source data reference, the renderer version, and exported images in the same artifact directory.

## Boundaries

- Default to high-information displays: distributions, paired observations, regression diagnostics, ECDFs, stratified views, and uncertainty-aware summaries where they answer the question better than aggregate bars.
- Do not infer causality, significance, or model adequacy from a figure alone. State assumptions and sample-size limitations.
- Do not use a rainbow palette, truncated quantitative axes, or a dual y-axis unless the specification gives a defensible reason.
- Do not silently substitute fonts or change a named theme. Emit a warning in the render report.
