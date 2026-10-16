## Agents

| Agent | Purpose | Needs --worktree |
|-------|---------|------------------|
| `code-explorer` | Trace code, map architecture, find patterns | No (read-only) |
| `code-architect` | Design approaches, file plans, build sequences | No (read-only) |
| `code-reviewer` | Review for bugs, simplicity, conventions | No (read-only) |
| `develop` | Implement code, run tests | **Yes** — use `DO_WORKTREE_DIR` env prefix |
