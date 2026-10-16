## Phase 3: Act

- **TDD Rule**: No failing test → no production code.
- Auto-write journal every 2 actions (PostToolUse hook).
- Failure counting (3-Failure Protocol):

```bash
~/.Codex/skills/sparv/scripts/failure-tracker.sh fail --note "short blocker"
~/.Codex/skills/sparv/scripts/failure-tracker.sh reset
```
