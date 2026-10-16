## Revision Mode Patch Protocol (#390)

In revision mode, `draft_writer_agent` does NOT re-emit the complete paper. The round runs **anchorize → patch → deterministic apply → finalizer**, confining the regeneration surface to the blocks the revision explicitly touches (DELEGATE-52 blast-radius containment; spec `docs/design/2026-06-10-390-diff-patch-revision-mode-spec.md`):

1. **Anchorize** the draft (`scripts/ars_anchorize_draft.py` — idempotent, content-neutral): every block gets a stable `<!--block:BNNNN-->` marker; a block manifest (`base_draft_hash` + per-block `old_hash`) is regenerated. Nothing may rewrite the draft between this step and apply.
2. **The writer emits a patch document** (`shared/contracts/patch/revision_patch.schema.json`) as a sidecar file in its `phase6_*/` fence — block ops with hash preconditions copied from the manifest, each op tracing to `roadmap_item_ids`. See `agents/draft_writer_agent.md` § Patch-Document Revision Emission.
3. **Deterministic apply** (`scripts/ars_apply_revision_patch.py`): two-phase fail-closed — one stale hash rejects the whole patch with the base byte-untouched; untouched blocks are preserved byte-identical by construction. Structural shapes (heading rewrites/deletes, section-count change, touched-ratio > 0.6) refuse without an explicit acknowledge that only the §3.6 escalation checkpoint may grant. The apply report (`preserved_ratio`, ops, fresh block IDs, structural flags) is a **required input to re-review** alongside the revised draft.
4. **Escalation, never silent fallback:** restructure-demanding rounds go to a MANDATORY user checkpoint; a confirmed full re-emission round is provenance-stamped `mode: full_reemission_escalated` and the draft is re-anchorized afterwards (new ID generation).

Orchestrated runs follow `pipeline_orchestrator_agent.md` § Revision-Round Patch Sequencing; Mode B (phase-by-phase manual) users run the same scripts by hand — exact commands in `references/revision_patch_protocol.md`. Honest boundary, stated once: patch mode removes the silent-distortion channel for text the revision does not touch; it does not make the revision itself better. The `academic-paper full` in-pair Phase 6→4 loop is NOT patch-adopted (its Phase 4b lint requires a full `## Draft Body`; Item 9 boundary, spec §5.2/§7).

---
