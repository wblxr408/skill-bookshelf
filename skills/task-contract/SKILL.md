---
name: task-contract
description: Turn an AI task into a concise goal, scope, constraints, and completion contract. Use before coding, research, refactoring, or delegation when the request could be interpreted in several ways.
---

# Task contract

Before substantial work, formulate a compact contract from the user's request:

- **Goal:** the user-visible outcome.
- **Scope:** the files, systems, questions, or decisions in bounds.
- **Constraints:** things that must remain true, such as API compatibility, performance, style, security boundaries, or a no-install/no-deploy limit.
- **Evidence of completion:** the checks, output, or review condition that demonstrates success.

Use information already supplied by the user and repository before asking a question. Ask only when the unresolved choice would materially change the outcome or risk.

Keep the contract proportional: one or two sentences for ordinary work; bullets only when the boundaries are complex. Revisit it if new evidence shows it was wrong. Do not silently expand the scope.
