---
name: lean-agent-harness
description: Keep AI task instructions, repository guidance, and automation interfaces compact and durable across model upgrades. Use when creating or simplifying prompts, agent rules, or workflow scaffolding.
---

# Lean agent harness

Preserve only durable information that a capable model cannot reliably infer: project commands, architecture boundaries, data contracts, required checks, approval limits, and user-specific conventions.

Prefer direct tool interfaces, short Markdown guidance, and task-local context over elaborate multi-stage prompt chains. Remove rules that duplicate tool-enforced policy, describe obvious general behavior, or compensate for a past model weakness without a current need.

When simplifying an existing harness, make small reversible changes. Keep a rule only when it prevents a known, material failure; record the failure and the intended invariant near the rule when helpful. Validate that the simpler harness still completes a representative task.
