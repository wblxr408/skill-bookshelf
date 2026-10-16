---
name: paper-audit
description: Review academic manuscripts, evidence, methods, and submission readiness; support peer panels, calibration, and revision verification.
metadata:
  version: "fusion-2026-10-05"
---

# Paper Audit — unified manuscript review

Read [the execution contract](references/fusion-policy.md). Review the supplied manuscript and requested scope before selecting a mode. Preserve `.tex`, `.typ`, or PDF source; do not silently rewrite it during a review.

| Need | Read next |
|---|---|
| Quick screen, deep technical critique, PASS/FAIL submission gate, or re-audit | [audit modes](references/audit-modes.md) then [audit module](modules/audit/PLAYBOOK.md) |
| Five-perspective peer panel, editorial letter, guided review, methodology focus, reviewer calibration, or cross-model review | [peer review](references/peer-review.md) then the relevant section in [peer module](modules/peer-review/PLAYBOOK.md) |
| Verify citations, literature novelty, methodology, bias, statistics, ethics, or conflicting evidence | [evidence review](references/evidence-review.md) then relevant [evidence module](modules/evidence-review/PLAYBOOK.md) resources |
| Compare revisions with earlier comments, or audit a rebuttal | [revision verification](references/revision-verification.md) |

Combine requested perspectives into one issue register, deduplicating by the underlying defect while preserving independent evidence. Include severity, exact location, evidence, consequence, smallest correction, and verification state. Keep script-backed findings separate from expert judgment. A gate fails for actual blockers; style suggestions remain advisory. Use the user's requested format; comprehensive reviews can use the retained Markdown/HTML report scripts and reviewer templates.

Writing and source edits route to `$academic-paper`; topic research remains `$deep-research`. `academic-paper-reviewer` and `deep-research paper-review` are compatibility intents handled here. Missing upstream shared protocols are handled by [runtime adapters](references/runtime-adapters.md), without inventing evidence or weakening review criteria.
