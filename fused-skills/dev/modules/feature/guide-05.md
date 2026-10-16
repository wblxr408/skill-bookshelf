## Hard Constraints

1. **Never write code directly.** Delegate all code changes to `codeagent-wrapper` agents.
2. **Parallel-first.** Run independent tasks via `codeagent-wrapper --parallel`.
3. **Update phase after each phase.** Use `task.py update-phase <N>`.
4. **Expect long-running `codeagent-wrapper` calls.** High-reasoning modes can take a long time.
5. **Timeouts are not an escape hatch.** If a call times out, retry with narrower scope.
6. **Defer worktree decision until Phase 4.** Only ask about worktree mode right before implementation. If enabled, prefix develop agent calls with `DO_WORKTREE_DIR=<path>`. Never pass `--worktree` after initialization.
