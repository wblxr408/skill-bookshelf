---
name: dev
description: Implement features, fix defects, and refactor with mandatory behavior-driven TDD, research and contract reuse, domain guidance, focused review, and full functional regression.
metadata:
  version: "fusion-ecc-2026-10-12"
---

# Unified development

Read [the execution contract](references/fusion-policy.md). Derive the goal, scope, constraints, and observable acceptance criteria from the request and repository. Inspect the smallest relevant index and real callers; reuse applicable Basic Memory evidence. Complete already-authorized work and ask only for a material missing choice.

**TDD is required for executable behavior changes:** write behavior tests before implementation, run and observe their intended failure, implement, then run the affected regression and required project checks. Read [testing and acceptance](references/testing.md). Unless the user explicitly requests the specific check, do not create or run smoke tests, hash/checksum comparisons, file-presence/import/startup probes, shallow health checks, wording/regex checks or tests that restate implementation. This is a prohibition on execution, not merely on using their results as evidence. A general request to verify, an upstream guide or a CI requirement does not authorize these checks. Do not relabel them as diagnostics, preflight, integration or regression. Pure prose changes do not create invented code tests.

| Need | Read next |
|---|---|
| Ordinary implementation or defect | [implementation](references/implementation.md), [testing](references/testing.md) |
| Existing solution, dependency or integration | [research and contracts](references/research-contracts.md) |
| Multi-component feature or architecture decision | [feature workflow](references/feature-workflow.md), then only the relevant preserved feature module |
| API, backend, persistence or asynchronous work | [backend and data](references/backend-data.md) |
| Frontend behavior, accessibility, interaction or performance | [frontend engineering](references/frontend-engineering.md); use the local design owner for art direction |
| Language/framework, mobile, database, network, ML or other domain gap | [domain catalog](references/ecc-catalog.md); select one matching guide, not the whole library |
| Build failure, delivery, migrations or rollout | [delivery and operations](references/delivery-operations.md) |
| Security-sensitive changes or MCP/tool boundary | [security and tool integration](references/security-tools.md) |
| Agent reliability, latency, throughput or cost optimization | [evaluation and optimization](references/evaluation-optimization.md) |
| Agent/backend routing | [agent routing](references/agent-routing.md); obey current authorization |
| Persistent state, resumable work or reusable lesson | [state and recovery](references/state-and-recovery.md), [learning](references/learning.md) |
| `/dev`, `/do`, `/omo`, `/sparv`, `/harness` or an ECC command intent | Interpret its purpose through these routes; [compatibility](references/compatibility.md) resolves old names |

Use direct supported tools. codeagent-wrapper and upstream specialist roles are optional adapters and review perspectives; they never require a fixed backend, role count, sequence of approvals, or compulsory agent dispatch. Give an authorized collaborator a bounded task and collect its result before finishing. Project documentation, ownership, and current environment control imported examples.

Review correctness and purpose through `agent-crosscheck` when it adds evidence. `context-bridge` owns continuity and `engineering-memory` owns durable knowledge; ECC adds methods to these owners rather than creating a second default store or listener. The source library contains reference material, not independent policy. The execution contract and current user instructions govern every imported guide, script, command and role.

Production prompt/model/tool-policy changes use evaluation TDD: baseline failure against a frozen functional/optimization contract, followed by target and capability/security regression. Idempotency tests assert one business effect; legitimate retried transport calls may occur. Read the relevant domain guide before selecting those assertions.
