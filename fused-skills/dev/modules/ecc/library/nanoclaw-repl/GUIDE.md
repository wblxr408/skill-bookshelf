---
name: nanoclaw-repl
description: Operate and extend NanoClaw, ECC's zero-dependency session-aware REPL, with persistent markdown-backed sessions and slash commands for model switching, skill loading, session branching, cross-session search, history compaction, and export. Use when running or extending scripts/claw.js, or when resuming, branching, compacting, searching, or exporting a NanoClaw session.
metadata:
  origin: ECC
---

> Local integration: this is a technical reference, not an independently discoverable skill. Read [the local execution contract](../../../../references/fusion-policy.md) first. Mandatory TDD applies. Do not create or run smoke/hash/file-presence/import/startup/shallow-health or other superficial checks unless the user explicitly requests the specific check, even as auxiliary diagnostics. General verification requests and source/CI examples do not authorize them. No automatic agents, scripts, hooks, model changes, installs, messages, publication, or schedules are authorized by this guide.



# NanoClaw REPL

Use this skill when running or extending `scripts/claw.js`.

## Capabilities

- persistent markdown-backed sessions
- model switching with `/model`
- dynamic skill loading with `/load`
- session branching with `/branch`
- cross-session search with `/search`
- history compaction with `/compact`
- export to md/json/txt with `/export`
- session metrics with `/metrics`

## Operating Guidance

1. Keep sessions task-focused.
2. Branch before high-risk changes.
3. Compact after major milestones.
4. Export before sharing or archival.

## Extension Rules

- keep zero external runtime dependencies
- preserve markdown-as-database compatibility
- keep command handlers deterministic and local
