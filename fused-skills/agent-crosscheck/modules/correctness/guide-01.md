# Agent cross-check

Treat the primary output as a candidate, then perform a narrowly scoped review against the task contract.

Check only what adds value:

- whether the result achieves the stated goal;
- scope drift or unapproved external effects;
- violated constraints or invariants;
- missing validation, edge cases, or unsupported claims;
- the smallest practical correction.

Use a lightweight reviewer for routine work. Escalate to deeper analysis only when the task is high-impact, security-sensitive, irreversible, or evidence reveals a real concern.

Report findings by severity and evidence. If there are no material issues, say so plainly instead of inventing nits. Keep the final human decision focused on purpose, tradeoffs, and authorization rather than mechanical details.
