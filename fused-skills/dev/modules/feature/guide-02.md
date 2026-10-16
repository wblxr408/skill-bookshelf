## Loop Initialization (REQUIRED)

When triggered via `/do <task>`, initialize the task directory immediately without asking about worktree:

```bash
python3 "$HOME/.Codex/skills/do/scripts/setup-do.py" "<task description>"
```

This creates a task directory under `.Codex/do-tasks/` with:
- `task.md`: Single file containing YAML frontmatter (metadata) + Markdown body (requirements/context)

**Worktree decision is deferred until Phase 4 (Implement).** Phases 1-3 are read-only and do not require worktree isolation.
