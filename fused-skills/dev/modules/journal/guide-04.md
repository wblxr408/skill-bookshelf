## External Memory (Two Files)

Initialize (run in project root):

```bash
~/.Codex/skills/sparv/scripts/init-session.sh --force
```

File conventions:

- `.sparv/state.yaml`: State machine (minimum fields: `session_id/current_phase/action_count/consecutive_failures`)
- `.sparv/journal.md`: Unified log (Plan/Progress/Findings all go here)
- `.sparv/history/<session_id>/`: Archive directory
