## Agent Invocation Format

```bash
codeagent-wrapper --agent <agent_name> - <workdir> <<'EOF'
## Original User Request
<original request>

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: <...>
- Librarian output: <...>
- Oracle output: <...>
- Known constraints: <tests to run, time budget, repo conventions, etc.>

## Current Task
<specific task description>

## Acceptance Criteria
<clear completion conditions>
EOF
```

Execute in shell tool, timeout 2h.
