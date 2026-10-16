## v3.6.2 Sprint Contract Hard Gate

- **Reviewer hard gate.** All reviewer modes that ship with contracts (`reviewer_full`, `reviewer_methodology_focus`) now run two-call Phase 1 (paper-content-blind) + Phase 2 (paper-visible) orchestration. See `references/sprint_contract_protocol.md`.
- **Schema 13.2 sprint contract.** Each dimension carries `eligible_roles` and `owner_role`; reviewer Phase 1 commits only eligible scoring plans, while Phase 2 marks ineligible dimensions `not_assessed`. Mandatory dimensions pre-commit `what_triggers_fatal`; fatality is never synthesized post hoc. Validator: `scripts/check_sprint_contract.py`. Schema: `shared/sprint_contract.schema.json`.
- **Executable conformance + panel checkers.** Before synthesis, `scripts/check_phase_conformance.py` verifies role binding, plan grammar, manuscript blindness, trigger binding, dissent cap, and evidence anchors. After synthesis, `scripts/check_panel_synthesis.py` recomputes role-scoped two-stage arithmetic, verifies `dimension_verdicts`, and enforces the DA-CRITICAL terminal gate.
- **Synthesizer three-step mechanical protocol.** Build per-dimension eligible-seat matrix → apply each condition's quantifier per dimension, then its dimension quantifier → resolve precedence by severity. Majority with one assessed eligible seat means that seat decides. Forbidden operations are explicit in `agents/editorial_synthesizer_agent.md`.
- **methodology_focus reduced panel.** `reviewer_methodology_focus` mode runs a 2-reviewer panel (EIC + methodology only) instead of the default 5.
- **Templates:** `shared/contracts/reviewer/full.json` (panel 5) and `shared/contracts/reviewer/methodology_focus.json` (panel 2). Reserved modes (`reviewer_calibration`, `reviewer_guided`) keep pre-v3.6.2 behaviour until follow-up patch templates land; `reviewer_re_review` left the Schema 13 enum with #576 Spec B and is governed by the dedicated contract family `shared/contracts/re_review/`.

---
