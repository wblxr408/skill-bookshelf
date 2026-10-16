## Routing Signals (No Fixed Pipeline)

This skill is **routing-first**, not a mandatory `explore → oracle → develop` conveyor belt.

| Signal | Add this agent |
|--------|----------------|
| Code location/behavior unclear | `explore` |
| External library/API usage unclear | `librarian` |
| Risky change: multi-file/module, public API, data format/config, concurrency, security/perf, or unclear tradeoffs | `oracle` |
| Implementation required | `develop` (or `frontend-ui-ux-engineer` / `document-writer`) |

### Skipping Heuristics (Prefer Explicit Risk Signals)

- Skip `explore` when the user already provided exact file path + line number, or you already have it from context.
- Skip `oracle` when the change is **local + low-risk** (single area, clear fix, no tradeoffs). Line count is a weak signal; risk is the real gate.
- Skip implementation agents when the user only wants analysis/answers (stop after `explore`/`librarian`).

### Common Recipes (Examples, Not Rules)

- Explain code: `explore`
- Small localized fix with exact location: `develop`
- Bug fix, location unknown: `explore → develop`
- Cross-cutting refactor / high risk: `explore → oracle → develop` (optionally `oracle` again for review)
- External API integration: `explore` + `librarian` (can run in parallel) → `oracle` (if risk) → implementation agent
- UI-only change: `explore → frontend-ui-ux-engineer` (split logic to `develop` if needed)
- Docs-only change: `explore → document-writer`
