## Re-Review Mode (Verification Review)

Dedicated mode for Pipeline Stage 3' — verifies whether revisions address first-round review comments. Uses R&R Traceability Matrix (Schema 11 + machine-readable sidecar) with Author's Claim + Verified? columns. Runs under the #576 three-gate evidence-before-persuasion contract: Phase 1 criteria commitment (revision-blind) → Phase 2A evidence verdict (persuasion-blind) → Phase 2B claim matching (letter revealed), checker-verified before any outcome surfaces.

**Input**: Original Revision Roadmap + Original (pre-revision) draft (Phase 2A comparison base — regression attribution and MADE_WORSE discriminators; absent → visible degradations, every new issue `indeterminate`) + Revised manuscript + Response to Reviewers (optional; withheld until Phase 2B) + Editorial Decision Letter (optional, #539 — its Review Panel Provenance block feeds the Judge Record) + Round-1 review findings (Schema 6 reports — the level-3 criterion layer; absent → transported Schema 7 fields alone, `[ROUND1-FINDINGS-ABSENT]`) + Round-1 Reviewer Configuration Cards (yardstick continuity, § Yardstick Continuity in the protocol; absent → visible regeneration fallback) + apply report(s) + the paired revision patch/diff files (#390, when the revision used patch apply — the two travel together, verified by the §11 ordered-chain rule)
**Output**: Verification Review Report with traceability matrix + new issues + Decision (or `user_review_required` deferral / fail-closed abort)

> See `references/re_review_mode_protocol.md` for full verification logic, output format template, and Socratic guidance details.

---
