# Backend, data and asynchronous contracts

Use api-design, backend-patterns and the project's framework guide for endpoint semantics, pagination and typed errors. Enforce validation at the boundary, authorization for the affected resource, and stable client errors. For retriable operations define idempotency, replay, timeout, cancellation and side-effect boundaries before implementation; test duplicate requests and partial failure, not just one successful call.

Choose transaction and state ownership from the actual consistency requirement. For queues/jobs define delivery semantics, retry/backoff, deduplication, poison-message handling and acknowledgement behavior. Verify persistence and external side effects across crashes and retries. Avoid unbounded retry loops or assuming that network success equals committed business state.

Use postgres-patterns, mysql-patterns, prisma-patterns, redis-patterns, jpa-patterns, mybatis-patterns and clickhouse-io only for the actual database. Inspect query plans and representative data before changing indexes/caching. Cache invalidation, stale data and tenant boundaries are part of the behavior contract, with tests.

Use database-migrations for expand-contract compatibility, separate resumable backfills, concurrent-index limitations and immutable deployed migrations. Verify real data transformations and transitional application behavior; a schema command returning zero is insufficient.

Use error-handling for typed failures and retries; cost-aware-llm-pipeline and prompt-caching-strategy for LLM latency/cost only when applicable. Keep budget, model/version and provider failure behavior explicit. ML work uses data contracts, leakage checks, training/evaluation separation, reproducible seeds, metric thresholds and deployment monitoring from mle-workflow, pytorch-patterns and recsys-pipeline-architect.

Idempotency asserts the business effect, not the transport attempt count. After an ambiguous timeout it can be correct to send another request with the same stable operation key; verify one committed refund/payment effect and a reconciled persistent result across retries, concurrent workers and partial failure. Define operation identity and request-parameter binding: a changed payload with the same key is rejected; a new client key does not authorize another refund for the same business operation or exceed the refundable amount. Do not mock a gateway into always returning success or reject legitimate retry attempts to satisfy a call-count assertion.

For structured-data migrations, establish the actual semantic transformation contract before choosing a parser. Preserve original display/raw data and represent ambiguous or missing information explicitly rather than guessing a person's name components. Verify information preservation and legacy/new interpretation under transitional writes, interrupt/restart and rollback or forward recovery.
