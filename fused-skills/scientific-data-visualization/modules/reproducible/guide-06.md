## Tool contract

```powershell
python scripts/inspect_data.py data/measurements.xlsx --sheet Sheet1 --output artifacts/data-profile.json
python scripts/render_figure.py specs/pareto.yaml --output-dir artifacts/pareto
```

Use `--validate-only` to check a specification without rendering. Keep the specification, its source data reference, the renderer version, and exported images in the same artifact directory.
