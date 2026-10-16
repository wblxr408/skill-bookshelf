# Research, contracts and design evidence

Start with the project's authoritative scope/index, actual implementations and Basic Memory history. For functionality that may already exist, compare repository reuse, maintained packages, existing connectors/MCP and upstream implementations. Check current official documentation for API and version assumptions. Use available search channels and disclose omitted sources; no compulsory global search for a one-line local change.

Evaluate adopt/extend/compose/build by contract fit, maintenance, license, dependency weight, privacy, deployment and failure modes. An exact maintained match favors adoption; a stable partial match favors a thin adapter. Record the selected option and material tradeoff, not a fabricated numeric ranking.

For cross-service/frontend-backend work, establish one authoritative OpenAPI/schema/event contract and its compatibility/version policy. Derive producer and consumer tests from that contract. Do not let both sides independently redefine status codes, nullability, paging, errors, ordering or idempotency. Include migration and rollout compatibility.

For consequential choices, write an ADR only when another session/reviewer needs the decision: context, alternatives, decision, consequences, reversal cost and evidence. Use engineering-memory for personal reusable lessons, project documentation for project truth, and context-bridge for unfinished work. These have different ownership; do not duplicate the same large narrative in all three.

Source methods: search-first, contract-first, documentation-lookup, iterative-retrieval, architecture-decision-records, context-and-decisions, change-impact, codebase-onboarding and code-tour. Use one relevant catalog guide.
