# Implementation

Read the actual callers, data flow and project contract before editing. Identify the user-visible behavior and material invariants. Search the repository for reuse; use research-contracts for a dependency or integration gap. Follow testing.md before changing executable behavior: write and run the failing behavior test, implement complete required states, then perform affected regression and required checks.

Match project structure and dependency injection, error boundaries, state ownership and package manager. Make direct bounded edits; a wrapper or external coding backend is optional. Avoid new abstractions without a concrete repeated boundary. Finish the full requested result, fix affected failures in one substantive pass and stop once acceptance and required checks pass.
