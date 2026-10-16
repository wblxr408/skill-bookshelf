# Mandatory TDD and functional acceptance

Use for features, bug fixes, changed executable configuration, integrations and behavioral refactoring. Prose, copied knowledge and visual instruction updates have no invented code tests; check their actual routing and consistency instead.

Before code, map each acceptance criterion to its observable output or state, test layer and regression case. Discover the real repository runner, fixture lifecycle and CI requirements from project files. A missing tool or syntax/import failure is an infrastructure problem, not RED behavior evidence.

1. Write the failing behavior test first. For a bug, reproduce the exact input and assert the intended result. For a new behavior, express the consumer-facing contract. Run it and record the failed assertion and cause.
2. Implement the smallest complete behavior, including required error handling and boundary cases. Run the new test to GREEN.
3. Refactor under tests. Run the affected full regression and required build/type/lint/CI checks. Fix failures caused by the change and retain unrelated failure evidence separately.

For an unchanged-behavior refactor, existing behavior tests start GREEN. Add any missing contract coverage before edits and rerun it afterwards; do not alter production merely to manufacture RED. Record why there is no new failing behavior.

Choose test layers by the boundary: unit tests for decisions and algorithms; integration tests for schema, persistence, transactions, queues and external adapters; user-flow E2E tests for browser/native journeys. Do not require every layer for an isolated pure function. A UI journey must verify the resulting action and state, including loading, empty, error, keyboard and accessibility behavior where affected, rather than checking that a page opened.

Cover representative success and rejection, empty/min/max boundaries, duplicate and retry behavior, stale state and cancellation. For async/stateful work add ordering, races and failure recovery where they affect the contract. For a migration verify existing data interpretation, transitional read/write compatibility, backfill restart behavior and the actual rollback/forward-recovery strategy.

Use real implementations for the boundary being tested. Fakes are acceptable for unavailable outside systems if the test also states the adapter contract and remaining integration evidence. Do not mock away the defect, let both sides share the same faulty assumption, accept all requests, or treat an invented response as live-service proof. Use deterministic fixtures and explicit lifecycle cleanup; assert meaningful effects rather than sleep or brittle selectors.

**Do not execute unless explicitly requested:** smoke tests; hash/checksum comparisons; file-presence/import/startup probes; shallow health checks; wording/regex checks; tests mirroring code internals. Do not create or run these checks as auxiliary diagnostics, preflight, integration or regression, even if their results would not be completion evidence. General verification requests and upstream/CI instructions do not authorize them. If a required command includes these checks, omit them and report the resulting gap. An explicit request authorizes only that specific check. A single canned success does not establish acceptance. Build, type, lint and format checks complement functional tests.

Keep an evidence map: requirement -> tested input/state -> expected effect -> RED failure -> GREEN/regression result -> remaining gap. Coverage identifies omitted paths; satisfy actual project thresholds but never present a percentage as proof. No forced checkpoint commits or repeated unchanged suites.

Language and framework fixtures live in the catalog: python-testing, golang-testing, rust-testing, cpp-testing, csharp-testing, fsharp-testing, kotlin-testing, perl-testing, react-testing, swift-protocol-di-testing, django-tdd, laravel-tdd, quarkus-tdd, springboot-tdd, e2e-testing and windows-desktop-e2e. Apply this contract to their examples.

For production prompt/model/tool-policy changes use evaluation-optimization.md as TDD: freeze the functional/evaluation contract before edits, observe the baseline target/failure, then require the improved target plus capability/security regression. Treat repeated transport calls separately from repeated business effects; test the latter at its actual state/side-effect boundary.
