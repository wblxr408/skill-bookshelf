# Collected reference gallery: tier-1 routing

The corpus contains 21 inspected screenshots from Origin's graph gallery and resource-template pages. Use it as a controlled visual vocabulary. A source marked `template` is an example package, not evidence that the renderer natively supports that plot.

| Tier-1 family | Select when the question is about | Query category |
| --- | --- | --- |
| Exploratory 2D | points, trajectories, error, paired observations | `exploratory-2d` |
| Distribution and quality | spread, histogram, violin, probability, QC | `distribution-quality` |
| Comparison and composition | bars, parts-of-whole, area, waterfall | `comparison-composition` |
| Multivariate and coordinated views | groups, parallel sets, networks, multi-axis/panel | `multivariate-coordinated` |
| Matrix, contour and density | gridded values, correlation, spatial density | `matrix-contour-density` |
| Geospatial | map-based magnitude or composition | `geospatial` |
| Polar, ternary and finance | circular coordinates, composition simplex, market series | `polar-ternary-finance` |
| 3D and functions | 3D observations, surfaces, volumes, parametric functions | `three-d-functions` |
| Domain templates | XRD, XPS, time-series browser, specialized packages | `domain-templates` |

Use the query script rather than opening `assets/reference-catalogue.yaml` directly. The script returns only the requested tier, preserving progressive loading.

## Token-efficient recognition protocol

1. Search a user phrase or a vision-derived clue: `--search "小提琴"`. This returns only short candidate records.
2. Resolve one candidate by `type_id`; the default result is ID, label, family, status, and short evidence IDs.
3. Add `--detail` only after choosing the candidate. It expands to the inherited visual grammar and data shape.
4. If candidates are visually confusable, resolve exactly one `src-XX` via `--source-id` and inspect the unmodified source screenshot. This is a delayed evidence check, not a lossy summary, so it preserves identification accuracy.

Do not send the 237-entry catalogue or all 21 screenshots into model context. The source corpus remains on disk and is loaded only for a contested final match.

## Table plus human prompt

For normal use, the input is a data table and a manually written analytical request. Use the generated JSONL keyword index with local `rg`; it returns candidate IDs without sending the catalogue to the model. Then use the table profile as a hard compatibility gate. `rg` performs candidate recall only: never let a keyword match override incompatible columns, absent geographic fields, missing OHLC fields, or a `reference-only` status.
