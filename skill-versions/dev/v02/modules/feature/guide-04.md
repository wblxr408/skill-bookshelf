## Worktree Mode

The worktree is created **only when needed** (right before Phase 4: Implement). If the user chooses worktree mode:

1. Run setup with `--worktree` flag to create the worktree:
   ```bash
   python3 "$HOME/.Codex/skills/do/scripts/setup-do.py" --worktree "<task description>"
   ```

2. Use the `DO_WORKTREE_DIR` environment variable to direct `codeagent-wrapper` develop agent into the worktree. **Do NOT pass `--worktree` to subsequent calls** — that creates a new worktree each time.

```bash
# Save the worktree path from setup output, then prefix all develop calls:
DO_WORKTREE_DIR=<worktree_dir> codeagent-wrapper --agent develop - . <<'EOF'
...
EOF
```

Read-only agents (code-explorer, code-architect, code-reviewer) do NOT need `DO_WORKTREE_DIR`.
