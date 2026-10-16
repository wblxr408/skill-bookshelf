# Mandatory TDD and functional acceptance

Use for features, bug fixes, changed executable configuration, integrations and behavioral refactoring. Prose, copied knowledge and visual instruction updates have no invented code tests; check their actual routing and consistency instead.

Regression tests are prohibited unless the user explicitly requests the specific checks and scope. This includes creating, modifying or running local, full, cross-module and capability/security regression evaluations. Do not disguise them as functional verification, integration, diagnostics, acceptance or TDD. General verification requests, completion criteria, CI and upstream workflows do not authorize them.

Before code, map the current change's acceptance criteria to observable outputs or states and the smallest focused behavior cases. Discover the repository runner and fixture lifecycle from project files. Do not select existing suites or checks of unchanged functionality for automatic regression. A missing tool or syntax/import failure is an infrastructure problem, not RED behavior evidence.

1. Write the failing behavior test first. For a bug, reproduce the exact input and assert the intended result. For a new behavior, express the consumer-facing contract. Run it and record the failed assertion and cause.
2. Implement the smallest complete behavior, including required error handling and boundary cases. Run the new test to GREEN.
3. Verify the same current-change behavior to GREEN and run relevant build/type/lint/schema checks. Do not broaden into regression suites or invoke bundled test commands that include regression. Fix failures at the current target and retain unrelated evidence separately.

For an unchanged-behavior refactor, inspect code, contracts and existing evidence rather than automatically creating or rerunning regression tests. Do not alter production to manufacture RED. Any regression check requires the user's explicit request for that check; explain verification gaps without treating them as permission or inventing a generic approval gate.

Choose test layers by the boundary: unit tests for decisions and algorithms; integration tests for schema, persistence, transactions, queues and external adapters; user-flow E2E tests for browser/native journeys. Do not require every layer for an isolated pure function. A UI journey must verify the resulting action and state, including loading, empty, error, keyboard and accessibility behavior where affected, rather than checking that a page opened.

Cover representative success and rejection, empty/min/max boundaries, duplicate and retry behavior, stale state and cancellation. For async/stateful work add ordering, races and failure recovery where they affect the contract. For a migration verify existing data interpretation, transitional read/write compatibility, backfill restart behavior and the actual rollback/forward-recovery strategy.

Use real implementations for the boundary being tested. Fakes are acceptable for unavailable outside systems if the test also states the adapter contract and remaining integration evidence. Do not mock away the defect, let both sides share the same faulty assumption, accept all requests, or treat an invented response as live-service proof. Use deterministic fixtures and explicit lifecycle cleanup; assert meaningful effects rather than sleep or brittle selectors.

**Do not create, modify or execute regression tests unless explicitly requested.** Also do not create or run smoke tests, hash/checksum comparisons, file-presence/import/startup probes, shallow health checks, wording/regex checks or tests mirroring code internals without an explicit request for the specific check. These prohibitions apply even to auxiliary diagnostics and omitted completion evidence. General verification requests and upstream/CI instructions do not authorize them. Omit prohibited checks from bundled commands and report the gap. Authorization covers only the requested check and scope. Relevant build, type, lint, schema and format checks complement the current behavior's focused acceptance.

Keep an evidence map: current requirement -> tested input/state -> expected effect -> RED failure -> GREEN result -> remaining gap. Coverage requirements do not authorize regression; report unmet checks rather than running prohibited suites. Never present a percentage as proof. No forced checkpoint commits or repeated unchanged suites.

Language and framework fixtures live in the catalog: python-testing, golang-testing, rust-testing, cpp-testing, csharp-testing, fsharp-testing, kotlin-testing, perl-testing, react-testing, swift-protocol-di-testing, django-tdd, laravel-tdd, quarkus-tdd, springboot-tdd, e2e-testing and windows-desktop-e2e. Apply this contract to their examples.

For production prompt/model/tool-policy changes use evaluation-optimization.md as focused TDD: freeze the current change's functional/evaluation target before edits, observe the baseline failure, then require the improved target. Capability/security regression evaluations need an explicit user request for the specific checks. Treat repeated transport calls separately from repeated business effects; verify the latter at the current behavior's actual state/side-effect boundary.
