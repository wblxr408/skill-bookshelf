## 5-Phase Workflow

### Phase 1: Understand (Parallel, No Interaction)

**Goal:** Understand requirements and map codebase simultaneously.

**Actions:** Run `code-architect` and 2-3 `code-explorer` tasks in parallel.

```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p1_requirements
agent: code-architect
workdir: .
---CONTENT---
Analyze requirements completeness (score 1-10):
1. Extract explicit requirements, constraints, acceptance criteria
2. Identify blocking questions (issues that prevent implementation)
3. Identify minor clarifications (nice-to-have but can proceed without)

Output format:
- Completeness score: X/10
- Requirements: [list]
- Non-goals: [list]
- Blocking questions: [list, if any]

---TASK---
id: p1_similar_features
agent: code-explorer
workdir: .
---CONTENT---
Find 1-3 similar features, trace end-to-end. Return: key files with line numbers, call flow, extension points.

---TASK---
id: p1_architecture
agent: code-explorer
workdir: .
---CONTENT---
Map architecture for relevant subsystem. Return: module map + 5-10 key files.

---TASK---
id: p1_conventions
agent: code-explorer
workdir: .
---CONTENT---
Identify testing patterns, conventions, config. Return: test commands + file locations.
EOF
```

### Phase 2: Clarify (Conditional)

**Goal:** Resolve blocking ambiguities only.

**Actions:**
1. Review `p1_requirements` output for blocking questions
2. **IF blocking questions exist** → Use AskUserQuestion
3. **IF no blocking questions (completeness >= 8)** → Skip to Phase 3

### Phase 3: Design (No Interaction)

**Goal:** Produce minimal-change implementation plan.

```bash
codeagent-wrapper --agent code-architect - . <<'EOF'
Design minimal-change implementation:
- Reuse existing abstractions
- Minimize new files
- Follow established patterns from Phase 1 exploration

Output:
- File touch list with specific changes
- Build sequence
- Test plan
- Risks and mitigations
EOF
```

### Phase 4: Implement + Review

**Goal:** Build feature and review in one phase.

**Step 1: Decide on worktree mode (ONLY NOW)**

Use AskUserQuestion to ask:

```
Develop in a separate worktree? (Isolates changes from main branch)
- Yes (Recommended for larger changes)
- No (Work directly in current directory)
```

If user chooses worktree:
```bash
python3 "$HOME/.Codex/skills/do/scripts/setup-do.py" --worktree "<task description>"
# Save the worktree path from output for DO_WORKTREE_DIR
```

**Step 2: Invoke develop agent**

For full-stack projects, split into backend/frontend tasks with per-task `skills:` injection. Use `--parallel` when tasks can be split; use single agent when the change is small or single-domain.

**Single-domain example** (prefix with `DO_WORKTREE_DIR` if worktree enabled):

```bash
# With worktree:
DO_WORKTREE_DIR=<worktree_dir> codeagent-wrapper --agent develop --skills golang-base-practices - . <<'EOF'
Implement with minimal change set following the Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
- Run narrowest relevant tests
EOF

# Without worktree:
codeagent-wrapper --agent develop --skills golang-base-practices - . <<'EOF'
Implement with minimal change set following the Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
- Run narrowest relevant tests
EOF
```

**Full-stack parallel example** (adapt task IDs, skills, and content based on Phase 3 design):

```bash
# With worktree:
DO_WORKTREE_DIR=<worktree_dir> codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p4_backend
agent: develop
workdir: .
skills: golang-base-practices
---CONTENT---
Implement backend changes following Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan

---TASK---
id: p4_frontend
agent: develop
workdir: .
skills: frontend-design,vercel-react-best-practices
dependencies: p4_backend
---CONTENT---
Implement frontend changes following Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
EOF

# Without worktree: remove DO_WORKTREE_DIR prefix
```

Note: Choose which skills to inject based on Phase 3 design output. Only inject skills relevant to each task's domain.

**Step 3: Review**

**Step 3: Review**

Run parallel reviews:

```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p4_correctness
agent: code-reviewer
workdir: .
---CONTENT---
Review for correctness, edge cases, failure modes.
Classify each issue as BLOCKING or MINOR.

---TASK---
id: p4_simplicity
agent: code-reviewer
workdir: .
---CONTENT---
Review for KISS: remove bloat, collapse needless abstractions.
Classify each issue as BLOCKING or MINOR.
EOF
```

**Step 4: Handle review results**

- **MINOR issues only** → Auto-fix via `develop`, no user interaction
- **BLOCKING issues** → Use AskUserQuestion: "Fix now / Proceed as-is"

### Phase 5: Complete (No Interaction)

**Goal:** Document what was built.

```bash
codeagent-wrapper --agent code-reviewer - . <<'EOF'
Write completion summary:
- What was built
- Key decisions/tradeoffs
- Files modified (paths)
- How to verify (commands)
- Follow-ups (optional)
EOF
```

Output the completion signal:
```
<promise>DO_COMPLETE</promise>
```
