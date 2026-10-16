# Paper Audit Skill v5.1

`paper-audit` is **deep-review-first**. Its core job is to behave like a
serious reviewer: find technical, methodological, claim-level, and
cross-section issues; keep script-backed findings separate from reviewer
judgment; and return a structured issue bundle plus a revision roadmap.

This version ships a script-backed `PRESUBMISSION` layer for final-week
mechanical checks (em dashes, AI-tone term frequency, abstract completeness,
LaTeX citation/label/equation hygiene, paragraph-shape weak signals, concrete
captions). It plugs into existing modes; it is not a separate public mode.
See `references/PRESUBMISSION_GUIDE.md` for mode integration.

Use it for audit and review. Do not use it as the first tool for source
editing, sentence rewriting, or build fixing.
