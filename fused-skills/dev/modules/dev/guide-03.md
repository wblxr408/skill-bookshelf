
  **Skip Deep Analysis When**:
  - Simple, straightforward implementation with obvious approach
  - Small changes confined to 1-2 files
  - Clear requirements with single implementation path

- **Step 3: Generate Development Documentation**
  - invoke agent dev-plan-generator
  - When creating `dev-plan.md`, ensure every task has `type: default|ui|quick-fix`
  - Append a dedicated UI task if Step 2 marked `needs_ui: true` but no UI task exists
  - Output a brief summary of dev-plan.md:
    - Number of tasks and their IDs
    - Task type for each task
    - File scope for each task
    - Dependencies between tasks
    - Test commands
  - Use AskUserQuestion to confirm with user:
    - Question: "Proceed with this development plan?" (state backend routing rules and any forced fallback due to allowed_backends)
    - Options: "Confirm and execute" / "Need adjustments"
  - If user chooses "Need adjustments", return to Step 1 or Step 2 based on feedback

- **Step 4: Parallel Development Execution [CODEAGENT-WRAPPER ONLY - NO DIRECT EDITS]**
  - MUST use Bash tool to invoke `codeagent-wrapper --parallel` for ALL code changes
  - NEVER use Edit, Write, MultiEdit, or Task tools to modify code directly
  - Backend routing (must be deterministic and enforceable):
    - Task field: `type: default|ui|quick-fix` (missing → treat as `default`)
    - Preferred backend by type:
      - `default` → `codex`
      - `ui` → `gemini` (enforced when allowed)
      - `quick-fix` → `Codex`
    - If user selected `仅 codex`: all tasks MUST use `codex`
    - Otherwise, if preferred backend is not in `allowed_backends`, fallback to the first available backend by priority: `codex` → `Codex` → `gemini`
  - Build ONE `--parallel` config that includes all tasks in `dev-plan.md` and submit it once via Bash tool:
    ```bash
    # One shot submission - wrapper handles topology + concurrency
    codeagent-wrapper --parallel <<'EOF'
    ---TASK---
    id: [task-id-1]
    backend: [routed-backend-from-type-and-allowed_backends]
    workdir: .
    dependencies: [optional, comma-separated ids]
    ---CONTENT---
    Task: [task-id-1]
    Reference: @.Codex/specs/{feature_name}/dev-plan.md
    Scope: [task file scope]
    Test: [test command]
    Deliverables: code + unit tests + coverage ≥90% + coverage summary

    ---TASK---
    id: [task-id-2]
    backend: [routed-backend-from-type-and-allowed_backends]
    workdir: .
    dependencies: [optional, comma-separated ids]
    ---CONTENT---
    Task: [task-id-2]
    Reference: @.Codex/specs/{feature_name}/dev-plan.md
    Scope: [task file scope]
    Test: [test command]
    Deliverables: code + unit tests + coverage ≥90% + coverage summary
    EOF
    ```
  - **Note**: Use `workdir: .` (current directory) for all tasks unless specific subdirectory is required
  - Execute independent tasks concurrently; serialize conflicting ones; track coverage reports
  - Backend is routed deterministically based on task `type`, no manual intervention needed

- **Step 5: Coverage Validation**
  - Validate each task’s coverage:
    - All ≥90% → pass
    - Any <90% → request more tests (max 2 rounds)

- **Step 6: Completion Summary**
  - Provide completed task list, coverage per task, key file changes

**Error Handling**
- **codeagent-wrapper failure**: Retry once with same input; if still fails, log error and ask user for guidance
- **Insufficient coverage (<90%)**: Request more tests from the failed task (max 2 rounds); if still fails, report to user
- **Dependency conflicts**:
  - Circular dependencies: codeagent-wrapper will detect and fail with error; revise task breakdown to remove cycles
  - Missing dependencies: Ensure all task IDs referenced in `dependencies` field exist
- **Parallel execution timeout**: Individual tasks timeout after 2 hours (configurable via CODEX_TIMEOUT); failed tasks can be retried individually
- **Backend unavailable**: If a routed backend is unavailable, fallback to another backend in `allowed_backends` (priority: codex → Codex → gemini); if none works, fail with a clear error message

**Quality Standards**
- Code coverage ≥90%
- Tasks based on natural functional boundaries (typically 2-5)
- Each task has exactly one `type: default|ui|quick-fix`
- Backend routed by `type`: `default`→codex, `ui`→gemini, `quick-fix`→Codex (with allowed_backends fallback)
- Documentation must be minimal yet actionable
- No verbose implementations; only essential code

**Communication Style**
- Be direct and concise
- Report progress at each workflow step
- Highlight blockers immediately
- Provide actionable next steps when coverage fails
- Prioritize speed via parallelization while enforcing coverage validation
