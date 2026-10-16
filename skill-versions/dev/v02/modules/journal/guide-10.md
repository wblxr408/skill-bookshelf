## Script Tools

| Script | Purpose |
|--------|---------|
| `scripts/init-session.sh` | Initialize `.sparv/`, generate `state.yaml` + `journal.md` |
| `scripts/save-progress.sh` | Maintain `action_count`, append to `journal.md` every 2 actions |
| `scripts/check-ehrb.sh` | Scan diff/text, output (optionally write) `ehrb_flags` |
| `scripts/failure-tracker.sh` | Maintain `consecutive_failures`, exit code 3 when reaching 3 |
| `scripts/reboot-test.sh` | 3-question self-check (optional strict mode) |
| `scripts/archive-session.sh` | Archive `journal.md` + `state.yaml` to `history/` |
