# Implementation

Read the actual callers, data flow and project contract before editing. Identify the user-visible behavior and material invariants. Search the repository for reuse; use research-contracts for a dependency or integration gap. Follow testing.md before changing executable behavior: write and run the minimal failing case for the current change, implement complete required states, and verify that same target plus relevant build/type/lint/schema checks. Regression testing is prohibited unless the user explicitly requests the specific check; do not expand to existing suites or unchanged functionality.

Match project structure and dependency injection, error boundaries, state ownership and package manager. Make direct bounded edits; a wrapper or external coding backend is optional. Avoid new abstractions without a concrete repeated boundary. Finish the full requested result, fix affected failures in one substantive pass and stop once acceptance and required checks pass.
