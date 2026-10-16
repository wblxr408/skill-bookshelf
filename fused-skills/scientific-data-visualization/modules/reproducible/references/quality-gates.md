# Quality gates

The renderer reports the following gates:

1. **Contract**: file exists, columns exist, chart fields have compatible types, and required mappings are present.
2. **Data semantics**: missing values, duplicate rows, empty groups, excessive filtering, time ordering, and category count are reported.
3. **Analytical appropriateness**: impossible or misleading configurations are errors: fewer than three observations in a distribution group; mean-only bars with fewer than ten observations per group; OLS with fewer than eight usable observations, fewer than three distinct x values, or zero y variance; and control charts with fewer than twenty observations or zero variance. Small samples, zero variance, insufficient regression points, and control-chart sample size are also surfaced in the data profile before specification.
4. **Visual quality**: configured font availability, palette capacity, label length, output size, table/header settings, and export completion are checked.
5. **Image-level QA**: PNG outputs are checked for existence, blank output, requested DPI, tonal variation and grayscale distinguishability by `scripts/visual_qa.py`; SVG/PDF geometry still requires human inspection.

Warnings require human judgement. Errors block output and are bugs in the job specification or source data that must be resolved before delivery. Chart routing and rendering do not validate statistical significance: inferential annotations additionally require a matching eligible decision record and an `analysis_reference` to the validated calculation. Use vector SVG/PDF for manuscript assembly and 300 dpi or higher PNG only when raster output is requested.
