# Chart selection and analysis guide

| Question | Prefer | Avoid by default |
| --- | --- | --- |
| Trajectory over ordered time | `line`; annotate events | connecting unordered categories |
| Relationship between two numeric variables | `scatter`; `hexbin` for large n; `regression-diagnostics` after fitting | binned bars hiding spread |
| Distribution across groups | `dot` for small n; `box`/`violin`/`ecdf` when support is adequate | mean-only bars for small samples |
| Before/after or matched samples | `paired`; retain a complete subject ID | independent-group bar chart |
| Ordered contribution to a total | `pareto` | unsorted categorical bars |
| Process stability | `control` | trend line without limits |
| Matrix relationship or condition grid | `correlation` or `heatmap` | rainbow heatmap |

For `scatter`, an OLS line describes association only; inspect residuals before relying on it. `paired` rejects missing or duplicated subject-condition cells. For `bar`, set `analysis.statistic` to `mean`, `sum`, or `count` and include uncertainty only when its calculation is appropriate; use `stacked-bar` only for additive parts of a shared whole. Control limits in the initial renderer use mean plus/minus three sample standard deviations; they are screening limits, not a substitute for process-specific control-chart rules.
