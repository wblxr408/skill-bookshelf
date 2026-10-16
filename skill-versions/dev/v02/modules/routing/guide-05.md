## Examples (Routing by Task)

<example>
User: /omo fix this type error at src/foo.ts:123

Sisyphus executes:

**Single step: develop** (location known; low-risk change)
```bash
codeagent-wrapper --agent develop - /path/to/project <<'EOF'
## Original User Request
fix this type error at src/foo.ts:123

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: None
- Librarian output: None
- Oracle output: None

## Current Task
Fix the type error at src/foo.ts:123 with the minimal targeted change.

## Acceptance Criteria
Typecheck passes; no unrelated refactors.
EOF
```
</example>

<example>
User: /omo analyze this bug and fix it (location unknown)

Sisyphus executes:

**Step 1: explore**
```bash
codeagent-wrapper --agent explore - /path/to/project <<'EOF'
## Original User Request
analyze this bug and fix it

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: None
- Librarian output: None
- Oracle output: None

## Current Task
Locate bug position, analyze root cause, collect relevant code context (thoroughness: medium).

## Acceptance Criteria
Output: problem file path, line numbers, root cause analysis, relevant code snippets.
EOF
```

**Step 2: develop** (use explore output as input)
```bash
codeagent-wrapper --agent develop - /path/to/project <<'EOF'
## Original User Request
analyze this bug and fix it

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: [paste complete explore output]
- Librarian output: None
- Oracle output: None

## Current Task
Implement the minimal fix; run the narrowest relevant tests.

## Acceptance Criteria
Fix is implemented; tests pass; no regressions introduced.
EOF
```

Note: If explore shows a multi-file or high-risk change, consult `oracle` before `develop`.
</example>

<example>
User: /omo add feature X using library Y (need internal context + external docs)

Sisyphus executes:

**Step 1a: explore** (internal codebase)
```bash
codeagent-wrapper --agent explore - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: None
- Librarian output: None
- Oracle output: None

## Current Task
Find where feature X should hook in; identify existing patterns and extension points.

## Acceptance Criteria
Output: file paths/lines for hook points; current flow summary; constraints/edge cases.
EOF
```

**Step 1b: librarian** (external docs/usage) — can run in parallel with explore
```bash
codeagent-wrapper --agent librarian - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: None
- Librarian output: None
- Oracle output: None

## Current Task
Find library Y’s recommended API usage for feature X; provide evidence/links.

## Acceptance Criteria
Output: minimal usage pattern; API pitfalls; version constraints; links to authoritative sources.
EOF
```

**Step 2: oracle** (optional but recommended if multi-file/risky)
```bash
codeagent-wrapper --agent oracle - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: [paste explore output]
- Librarian output: [paste librarian output]
- Oracle output: None

## Current Task
Propose the minimal implementation plan and file touch list; call out risks.

## Acceptance Criteria
Output: concrete plan; files to change; risk/edge cases; effort estimate.
EOF
```

**Step 3: develop** (implement)
```bash
codeagent-wrapper --agent develop - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: [paste explore output]
- Librarian output: [paste librarian output]
- Oracle output: [paste oracle output, or "None" if skipped]

## Current Task
Implement feature X using the established internal patterns and library Y guidance.

## Acceptance Criteria
Feature works end-to-end; tests pass; no unrelated refactors.
EOF
```
</example>

<example>
User: /omo how does this function work?

Sisyphus executes:

**Only explore needed** (analysis task, no code changes)
```bash
codeagent-wrapper --agent explore - /path/to/project <<'EOF'
## Original User Request
how does this function work?

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: None
- Librarian output: None
- Oracle output: None

## Current Task
Analyze function implementation and call chain

## Acceptance Criteria
Output: function signature, core logic, call relationship diagram
EOF
```
</example>

<anti_example>
User: /omo fix this type error

Wrong approach:
- Always run `explore → oracle → develop` mechanically
- Use grep to find files yourself
- Modify code yourself
- Invoke develop without passing context

Correct approach:
- Route based on signals: if location is known and low-risk, invoke `develop` directly
- Otherwise invoke `explore` to locate the problem (or to confirm scope), then delegate implementation
- Invoke the implementation agent with a complete Context Pack
</anti_example>
