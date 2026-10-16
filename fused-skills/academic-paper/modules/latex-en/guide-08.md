## Output Contract

- Return findings in LaTeX diff-comment style whenever possible: `% MODULE (Line N) [Severity] [Priority]: Issue ...`
- Keep comments surgical and source-aware.
- Report the exact command used and the exit code when a script fails.
- Preserve `\cite{}`, `\ref{}`, `\label{}`, custom macros, and math environments unless the user explicitly asks for source edits.
- For `literature`, default to diagnosis + rewrite blueprint first; only produce paragraph-level rewriting when the user explicitly asks for prose.
