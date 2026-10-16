## Enhanced Rules (v1.1)

### Uncertainty Declaration (G3)

When any Specify dimension scores < 2:
- Declare: `UNCERTAIN: <what> | ASSUMPTION: <fallback>`
- List all assumptions in journal before Plan
- Offer 2-3 options for ambiguous requirements

Example:
```
UNCERTAIN: deployment target | ASSUMPTION: Docker container
UNCERTAIN: auth method | OPTIONS: JWT / OAuth2 / Session
```

### Requirement Routing

| Mode | Condition | Flow |
|------|-----------|------|
| **Quick** | score >= 9 AND <= 3 files AND no EHRB | Specify → Act → Review |
| **Full** | otherwise | Specify → Plan → Act → Review → Vault |

Quick mode skips formal Plan phase but still requires:
- Completion promise written to journal
- 2-action save rule applies
- Review phase mandatory

### Context Acquisition (Optional)

Before Specify scoring:
1. Check `.sparv/kb.md` for existing patterns/decisions
2. If insufficient, scan codebase for relevant files
3. Document findings in journal under `## Context`

Skip if user explicitly provides full context.

### Knowledge Base Maintenance

During Vault phase, update `.sparv/kb.md`:
- **Patterns**: Reusable code patterns discovered
- **Decisions**: Architectural choices + rationale
- **Gotchas**: Common pitfalls + solutions

### CHANGELOG Update

Use during Review or Vault phase for non-trivial changes:
```bash
~/.Codex/skills/sparv/scripts/changelog-update.sh --type <Added|Changed|Fixed|Removed> --desc "..."
```
