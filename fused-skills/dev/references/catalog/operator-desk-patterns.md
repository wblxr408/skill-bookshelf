# operator-desk-patterns

Read only relevant technical detail. The local contract governs source mandates, test style, tool/agent usage and user authorization.

| Capability | Existing owner / integration | Use when |
|---|---|---|
| [counterparty-channel-discipline](../../modules/ecc/library/counterparty-channel-discipline/GUIDE.md) | dev / engineering-toolbox; technical-reference | Per-channel strict prompts, mention gating, silent observation, and a communication autonomy policy for agents that sit in shared channels with external counterparties. Use when an agent joins group chats, shared channel |
| [esign-field-placement](../../modules/ecc/library/esign-field-placement/GUIDE.md) | dev / engineering-toolbox; technical-reference | Deterministic method for placing signature, date, and text fields in a web e-signature composer through a browser automation session, using a fixed signature page, numeric Location panel coordinates instead of drag, and  |
| [master-agreement-generator](../../modules/ecc/library/master-agreement-generator/GUIDE.md) | dev / engineering-toolbox; technical-reference | Generate review drafts of counterparty master agreements from one template plus a JSON spec, with role-selected clauses and a Schedule A workflow limited to the executed agreement's notice authority. Use when you need re |
| [operator-approval-loop](../../modules/ecc/library/operator-approval-loop/GUIDE.md) | dev / engineering-toolbox; technical-reference | Operator approval contract with internal filing notices for agent-drafted outbound messages, hashed drafts, epoch-keyed decisions, durable delivery claims and receipts, and a pre-draft baseline gate. Use when an agent dr |
