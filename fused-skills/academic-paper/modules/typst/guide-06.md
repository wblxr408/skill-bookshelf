## Routing Rules

- Infer the module from the user request first. Ask for the module only if the request still maps equally well to multiple incompatible modules.
- If the user requests 2-3 compatible checks, run them in sequence rather than collapsing everything into one generic review.
- Use this execution order when multiple modules are needed: `compile` -> `bibliography` -> `format` -> `pseudocode` / `tables` -> `grammar` / `sentences` / `deai` -> `logic` / `literature` / `experiment` -> `title` / `expression` / `translation` / `adapt`.
- For bibliography requests, decide BibTeX vs Hayagriva before running the script; do not guess the format after the fact.
- Prefer `logic` for abstract-introduction-conclusion alignment, introduction funnel breaks, or contribution drift; prefer `literature` only when the user is specifically asking for Related Work synthesis, comparison, or gap derivation.
- Keep `pseudocode` for `algorithm-figure`, `algorithmic`, `lovelace`, caption, wrapper, and IEEE-like style-hook issues even when the user phrases them as formatting problems.
- If a command fails, report the exact command and exit code before suggesting the next fallback; do not silently replace a failed script run with a generic prose review.
