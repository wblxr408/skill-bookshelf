## Mode Selection

| Requested intent | Mode |
|---|---|
| "check my paper", "quick audit", "submission readiness", "pre-submission review", "投稿前检查" | `quick-audit` |
| "review my paper", "simulate peer review", "harsh review", "deep review" | `deep-review` |
| "is this ready to submit", "gate this submission", "blockers only" | `gate` |
| "did I fix these issues", "re-audit", "compare against old review" | `re-audit` |
| "polish the writing, but only if safe" | `polish` |

Legacy aliases still work for one compatibility cycle:

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

For per-mode workflow steps, input resolution rules, presentation surface
rules, and committee focus routing, see `references/MODE_GUIDE.md`.
