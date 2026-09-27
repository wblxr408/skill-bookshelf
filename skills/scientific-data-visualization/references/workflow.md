# Workflow and CLI

## 1. Profile data

Run `inspect_data.py` for every new source. It reports dimensions, inferred field roles, missingness, duplicate rows, distribution flags, IQR outliers, zero mass, group sizes, correlation summary, semantic hints, and candidate plot families. Review the report; inference is advisory, not a semantic guarantee. For AI recommendations, also read `ai-recommendation-protocol.md` and preserve its `首选 / 待确认候选 / 不适用` boundary.

Inputs are CSV or XLSX. For Excel, pass `--sheet` by name or zero-based index. The reader preserves the first row as column names unless the figure specification overrides it.

Before a new-machine run, verify the declared runtime locally and without changing the environment:

```powershell
python scripts/check_environment.py
python -m pip install -r scripts/requirements.txt
```

For the complete reproducible preflight, use the orchestration entry point:

```powershell
python scripts/run_workflow.py data/measurements.xlsx --sheet Measurements --prompt "比较不同处理组的分布并显示异常值" --output-dir artifacts/session
```

It writes `data-profile.json`, `visual-route.json`, `recommendation.json`, and a
`workflow-manifest.json`. It will not create a renderable starter until
`--confirm-semantics` is supplied. Add `--render` only after that confirmation;
the rendered directory then contains the normal render report and image QA.

## 2. Author a figure specification

Start from `assets/example-specs/`. Use YAML for hand-authored specifications or JSON for generated ones. Point `theme.path` to a versioned theme file and keep local overrides under `style.overrides`. Named theme options are `general-bilingual` (default), `nature`, `ieee`, `zh-core`, `morandi`, `tech-dark`, and `tech-light`; the legacy `journal-bilingual` remains compatible.

Before recommending a statistical method, ask whether it is wanted. When the answer is yes, use `recommend_statistics.py` to generate zero or more compatible method IDs. The method catalogue is explanatory only: `query_math_methods.py` labels entries that do not yet have a strict automatic adapter. It exposes no formulas unless `--confirmed` is explicitly supplied. To display an eligible, externally validated inferential result in a graph, use:

```yaml
statistics:
  confirmed: true
  method_id: two-sample-t
  eligibility: {status: eligible, method_id: two-sample-t}
  analysis_reference: artifacts/analysis/treatment-v-control.json
  results: {p: 0.031, mean_difference: 1.24}
  annotation: {enabled: true, location: title-subtitle}
```

The renderer rejects any `statistics` block without `confirmed: true`. Inferential methods additionally require matching eligible evidence and an `analysis_reference`. Results must come from a validated calculation; the renderer does not compute or invent p-values.

For a machine-readable three-tier hand-off, combine the saved visual and statistical packets:

```powershell
python scripts/build_recommendation_packet.py --statistics-packet artifacts/statistics.json --visual-packet artifacts/visual.json --conditional-method pca --output artifacts/recommendation.json
```

For qualified model work, `execute_models.py` performs tuning only inside the training partition and reports an untouched held-out evaluation for `logistic`, `ordinal`, `pls`, or `discriminant`. `execute_factorial_anova.py` executes qualified two-/three-factor ANOVA. Both commands require the matching eligibility packet and produce a traceable analysis artifact; they are not substitutes for an external validation plan.

For three or more independent groups with unequal variances, use the qualified
Welch path and retain Holm-adjusted pairwise contrasts:

```powershell
python scripts/execute_oneway_anova.py data/measurements.csv --outcome response --group treatment --variance unequal --eligibility artifacts/oneway-eligibility.json --output artifacts/oneway-welch.json
```

## 3. Render

```powershell
python scripts/render_figure.py specs/figure.yaml --output-dir artifacts/figure-01
```

The renderer exports every format in `output.formats`, the resolved spec, and `render-report.json`. It exits nonzero on invalid columns, invalid chart contracts, or unrenderable data; warnings do not conceal errors. The report also fingerprints the raw specification, theme, input file, and renderer using SHA-256, so same-path content changes remain auditable.

## 4. Review

Open the PNG for visual review and inspect `render-report.json`. Resolve errors first, then decide whether warnings are acceptable for the intended audience. Re-run from the same spec after any change.

## Supported plot types

`line`, `scatter`, `hexbin`, `regression-diagnostics`, `qq`, `leverage`, `bar`,
`stacked-bar`, `dot`, `paired`, `box`, `violin`, `ecdf`, `histogram`, `kde`,
`heatmap`, `correlation`, `pca`, `roc`, `pr`, `confusion`, `geo-scatter`,
`candlestick`, `waterfall`, `waterfall-lines`, `xrd-waterfall`,
`xps-waterfall`, `color-waterfall`, `bubble`, `surface3d`, `floating-bar3d`,
`polar-heatmap`, `radial-bubble`, `population-pyramid`, `connected-bar`,
`chord`, `pareto`, `control`, and `multi-panel`.
