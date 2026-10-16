## Workflow

1. Parse `$ARGUMENTS`, infer the smallest matching module, and keep that inference unless the user explicitly redirects you.
2. Read only the reference file needed for that module.
3. If the request contains multiple compatible concerns, run them in the routing order above and keep the output grouped by module.
4. Run the module script with `uv run python -B ...`.
5. Summarize issues, suggested fixes, and blockers in LaTeX-friendly comments.
6. If the user asks for a different concern, switch modules instead of overloading one run.
