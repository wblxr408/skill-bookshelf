## Routing Rules

- Infer the module from the user request before asking follow-up questions. Ask for the module only when two or more modules are equally plausible after keyword routing.
- If the user asks for 2-3 compatible checks in one turn, run them sequentially instead of forcing a single-module reply.
- Use this execution order when multiple modules are needed: `compile` -> `bibliography` -> `format` -> `figures` / `tables` / `pseudocode` -> `grammar` / `sentences` / `deai` -> `logic` / `literature` / `experiment` -> `title` / `expression` / `translation` / `adapt`.
- Prefer `logic` for cross-section alignment requests (abstract vs introduction vs conclusion), introduction funnel issues, or contribution drift; prefer `literature` only when the problem is specifically about Related Work organization, comparison, or gap derivation.
- Keep `experiment` for results, discussion, baseline, ablation, significance, limitation, and conclusion-completeness concerns even if the user phrases them as "logic" problems.
- When a script fails, stop the current module, report the exact command plus exit code, and recommend the next smallest useful fallback instead of silently switching modules.
