## Auto Hooks

`hooks/hooks.json`:

- PostToolUse: `save-progress.sh` (2-Action save)
- PreToolUse: `check-ehrb.sh --diff --dry-run` (prompt only, no state write)
- Stop: `reboot-test.sh --strict` (3-question self-check)

---

*Quality over speed—iterate until truly complete.*
