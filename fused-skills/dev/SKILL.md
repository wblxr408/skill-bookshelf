---
name: dev
description: Implement features, fix defects, and refactor with focused behavior-driven TDD, research and contract reuse, domain guidance, and review; regression tests require an explicit user request.
metadata:
  version: "fusion-ecc-2026-10-14"
---

## Technology selection

When the task leaves a consequential language, runtime, framework, database or key dependency undecided, read [tech-stack-evaluator](../tech-stack-evaluator/SKILL.md) before choosing the design or implementation. Reuse the project's approved decision and explicit technology constraints; ordinary edits within an established stack do not reopen stack selection. Record the actual constraints, feasible alternatives, current sources and accepted tradeoffs in the existing OpenSpec design or project decision. For new libraries follow [research and contracts](references/research-contracts.md).


# Unified development

Read [the execution contract](references/fusion-policy.md). Derive the goal, scope, constraints, and observable acceptance criteria from the request and repository. Inspect the smallest relevant index and real callers; reuse applicable Basic Memory evidence. Complete already-authorized work and ask only for a material missing choice.

**禁止回归测试。** 未经用户另行明确要求具体回归检查，不得新增、修改或执行回归测试，包括局部回归、完整回归、跨模块回归及能力/安全回归评估。不得通过改名为功能验证、集成测试、诊断、验收或 TDD 绕过禁止项。一般性的“验证一下”、任务完成要求、CI 和上游 skill/流程都不构成授权；明确授权仅适用于用户点名的检查和范围。

**TDD is required for executable behavior changes, limited to the current change's minimal behavior contract:** write and run the focused failing case, implement, then verify that same requested behavior to GREEN. Do not broaden into existing suites or checks of unchanged functionality. Relevant build/type/lint/schema checks remain available; commands that bundle regression tests must omit them. Read [testing and acceptance](references/testing.md). Unless the user explicitly requests the specific check, do not create or run smoke tests, hash/checksum comparisons, file-presence/import/startup probes, shallow health checks, wording/regex checks or tests that restate implementation. These prohibitions apply to execution itself, even if results are omitted from completion evidence. Pure prose changes use actual consistency review, without invented code tests.

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

Production prompt/model/tool-policy changes use evaluation TDD only for the current change's frozen functional/optimization target. Capability/security regression evaluations are prohibited unless the user explicitly requests the specific checks. Idempotency tests assert one business effect; legitimate retried transport calls may occur. Read the relevant domain guide before selecting those assertions.
