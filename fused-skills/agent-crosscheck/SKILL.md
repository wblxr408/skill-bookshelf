---
name: agent-crosscheck
description: Review a plan, code change, or answer for user purpose, scope, correctness, evidence, and meaningful tradeoffs in one focused pass.
metadata:
  version: "fusion-2026-10-05"
---

# Agent Crosscheck — unified outcome review

Review the result against the actual user goal and the task contract. Match depth to material risk and available evidence; ordinary work needs a focused pass.

| Review need | Read next |
|---|---|
| Purpose, scope, boundaries, tradeoffs, decision to proceed | [purpose](references/purpose.md) |
| Correctness, constraints, edge cases, claims, validation gaps | [correctness](references/correctness.md) |
| Both, or an ordinary change review | [combined review](references/combined-review.md) |

Combine the two perspectives into one deduplicated finding set. Use severity, exact evidence/location, impact, and the smallest useful correction. Automated formatting/syntax checks need no manual restatement. Do not invent nits or require another review after meaningful checks pass unless a change, failure, or unresolved concern warrants it.

Use an independent reviewer when authorized and valuable; otherwise disclose the bounds of a self-review. Keep the user's decision focused on goal, tradeoff, material uncertainty, or authorization. A clean review says there are no material findings and names the actual evidence. `$intent-review` intent is handled by the purpose route.

For development results, apply ../dev/references/testing.md. Review the requirement-to-RED/GREEN/regression evidence and actual effects; do not accept smoke/hash/startup evidence or a self-rating as proof. Use dev's ECC catalog for a specialist perspective only when it fits the changed boundary.
