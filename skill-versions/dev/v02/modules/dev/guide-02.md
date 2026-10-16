## CRITICAL CONSTRAINTS (NEVER VIOLATE)

These rules have HIGHEST PRIORITY and override all other instructions:

1. **NEVER use Edit, Write, or MultiEdit tools directly** - ALL code changes MUST go through codeagent-wrapper
2. **MUST use AskUserQuestion in Step 0** - Backend selection MUST be the FIRST action (before requirement clarification)
3. **MUST use AskUserQuestion in Step 1** - Do NOT skip requirement clarification
4. **MUST use TodoWrite after Step 1** - Create task tracking list before any analysis
5. **MUST use codeagent-wrapper for Step 2 analysis** - Do NOT use Read/Glob/Grep directly for deep analysis
6. **MUST wait for user confirmation in Step 3** - Do NOT proceed to Step 4 without explicit approval
7. **MUST invoke codeagent-wrapper --parallel for Step 4 execution** - Use Bash tool, NOT Edit/Write or Task tool

**Violation of any constraint above invalidates the entire workflow. Stop and restart if violated.**

---

**Core Responsibilities**
- Orchestrate a streamlined 7-step development workflow (Step 0 + Step 1–6):
  0. Backend selection (user constrained)
  1. Requirement clarification through targeted questioning
  2. Technical analysis using codeagent-wrapper
  3. Development documentation generation
  4. Parallel development execution (backend routing per task type)
  5. Coverage validation (≥90% requirement)
  6. Completion summary

**Workflow Execution**
- **Step 0: Backend Selection [MANDATORY - FIRST ACTION]**
  - MUST use AskUserQuestion tool as the FIRST action with multiSelect enabled
  - Ask which backends are allowed for this /dev run
  - Options (user can select multiple):
    - `codex` - Stable, high quality, best cost-performance (default for most tasks)
    - `Codex` - Fast, lightweight (for quick fixes and config changes)
    - `gemini` - UI/UX specialist (for frontend styling and components)
  - Store the selected backends as `allowed_backends` set for routing in Step 4
  - Special rule: if user selects ONLY `codex`, then ALL subsequent tasks (including UI/quick-fix) MUST use `codex` (no exceptions)

- **Step 1: Requirement Clarification [MANDATORY - DO NOT SKIP]**
  - MUST use AskUserQuestion tool
  - Focus questions on functional boundaries, inputs/outputs, constraints, testing, and required unit-test coverage levels
  - Iterate 2-3 rounds until clear; rely on judgment; keep questions concise
  - After clarification complete: MUST use TodoWrite to create task tracking list with workflow steps

- **Step 2: codeagent-wrapper Deep Analysis (Plan Mode Style) [USE CODEAGENT-WRAPPER ONLY]**

  MUST use Bash tool to invoke `codeagent-wrapper` for deep analysis. Do NOT use Read/Glob/Grep tools directly - delegate all exploration to codeagent-wrapper.

  **How to invoke for analysis**:
  ```bash
  # analysis_backend selection:
  # - prefer codex if it is in allowed_backends
  # - otherwise pick the first backend in allowed_backends
  codeagent-wrapper --backend {analysis_backend} - <<'EOF'
  Analyze the codebase for implementing [feature name].

  Requirements:
  - [requirement 1]
  - [requirement 2]

  Deliverables:
  1. Explore codebase structure and existing patterns
  2. Evaluate implementation options with trade-offs
  3. Make architectural decisions
  4. Break down into 2-5 parallelizable tasks with dependencies and file scope
  5. Classify each task with a single `type`: `default` / `ui` / `quick-fix`
  6. Determine if UI work is needed (check for .css/.tsx/.vue files)

  Output the analysis following the structure below.
  EOF
  ```

  **When Deep Analysis is Needed** (any condition triggers):
  - Multiple valid approaches exist (e.g., Redis vs in-memory vs file-based caching)
  - Significant architectural decisions required (e.g., WebSockets vs SSE vs polling)
  - Large-scale changes touching many files or systems
  - Unclear scope requiring exploration first

  **UI Detection Requirements**:
  - During analysis, output whether the task needs UI work (yes/no) and the evidence
  - UI criteria: presence of style assets (.css, .scss, styled-components, CSS modules, tailwindcss) OR frontend component files (.tsx, .jsx, .vue)

  **What the AI backend does in Analysis Mode** (when invoked via codeagent-wrapper):
  1. **Explore Codebase**: Use Glob, Grep, Read to understand structure, patterns, architecture
  2. **Identify Existing Patterns**: Find how similar features are implemented, reuse conventions
  3. **Evaluate Options**: When multiple approaches exist, list trade-offs (complexity, performance, security, maintainability)
  4. **Make Architectural Decisions**: Choose patterns, APIs, data models with justification
  5. **Design Task Breakdown**: Produce parallelizable tasks based on natural functional boundaries with file scope and dependencies

  **Analysis Output Structure**:
  ```
  ## Context & Constraints
  [Tech stack, existing patterns, constraints discovered]

  ## Codebase Exploration
  [Key files, modules, patterns found via Glob/Grep/Read]

  ## Implementation Options (if multiple approaches)
  | Option | Pros | Cons | Recommendation |

  ## Technical Decisions
  [API design, data models, architecture choices made]

  ## Task Breakdown
  [2-5 tasks with: ID, description, file scope, dependencies, test command, type(default|ui|quick-fix)]

  ## UI Determination
  needs_ui: [true/false]
  evidence: [files and reasoning tied to style + component criteria]
  ```
