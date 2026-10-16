## Workflow

1. Parse `$ARGUMENTS`, infer the active module, and keep that inference unless the user explicitly changes the target.
2. If the request combines multiple compatible concerns, run them in the routing order above and group the output by module.
3. Read only the reference file needed for that module.
4. Run the module script with `uv run python ...`.
5. Return Typst-ready comments and next actions.
6. For bibliography requests, decide BibTeX vs Hayagriva first, then run `bibliography`.
