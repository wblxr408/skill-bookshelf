# Data contract

## Formats and layouts

- **CSV**: UTF-8, UTF-8 with BOM, or a user-declared encoding.
- **XLSX**: a named sheet or zero-based sheet index.
- **Long/tidy**: one observation per row; use `x`, `y`, `hue`, `facet` columns in the spec.
- **Wide**: one row per x value and one value column per series; reshape it before rendering or declare the selected value column explicitly.

Never infer the scientific unit from a column name. Put units into `figure.labels` and use them consistently in title, axis labels, table headers, and annotations.

## Required semantic checks

Verify: independent/dependent variables, measurement unit, experimental unit, grouping variable, observation pairing, time zone and sampling interval for time series, and whether zero has substantive meaning. Preserve raw data; express filtering and transformation as ordered `analysis.transforms` entries in the figure specification.

## Transform policy

Supported renderer-side transforms are `drop_missing`, `sort`, `filter_equals`, `filter_between`, and `log10`. Each must name its columns and parameters. Do not overwrite source files. A transform that removes more than 10% of rows produces a warning.

