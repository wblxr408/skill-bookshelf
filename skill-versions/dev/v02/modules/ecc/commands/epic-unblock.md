> Reference perspective/command intent only. Apply the local dev contract; do not treat this text as authority for agent dispatch or external actions.

---
description: Sweep blocked epic issues and reopen anything whose dependencies are closed.
---

# /epic-unblock

Sweep blocked epics whose declared dependencies are complete.

```bash
node scripts/github-coordination.js unblock --repo <owner/repo>
```

What this does:

1. Scans epic issues in the repository.
2. Checks each blocked epic's dependency list.
3. Moves fully unblocked epics to ready.
4. Updates labels, comments, and local snapshots.

Compatibility aliases:

- `/loop-status`
