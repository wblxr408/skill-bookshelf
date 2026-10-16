## Workflow

Each mode has the same shape: parse `$ARGUMENTS`, lock the paper path, infer
mode/report-style/focus/language if not provided, then run the canonical
command. Detailed phase steps are in `references/MODE_GUIDE.md`.

### `quick-audit`

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode quick-audit ...
```

Present `Submission Blockers` -> `Quality Improvements` -> checklist; call
out `PRESUBMISSION` mechanical findings with `[Script]` provenance. Escalate
to `deep-review` when the user wants reviewer-depth critique.

### `deep-review`

Five phases (see `references/MODE_GUIDE.md` for full detail):

1. **Workspace prep**:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" <paper> --output-dir ./review_results
   ```
   If the target review workspace already exists, stop and ask before replacing
   it. Use `--overwrite` only after the user confirms the existing artifacts can
   be discarded; for the all-in-one `audit.py --mode deep-review` path, use
   `--overwrite-workspace` after the same confirmation.
2. **Phase 0 automated audit**:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode deep-review ...
   ```
3. **Phase 3A committee** — dispatch 5 committee agents (editor, theory,
   literature, methodology, logic) and write `committee/consensus.md`.
4. **Phase 3B section + cross-cutting lanes** — section, claims-vs-evidence,
   notation, evaluation fairness, self-consistency, prior-art, and
   pre-submission readiness (full/editor focus only).
5. **Consolidation**:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" <review_dir>
   uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" <review_dir> --write-back
   uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" <review_dir> --lang $LANG
   uv run python -B "$SKILL_DIR/scripts/render_html_report.py" <review_dir> --lang $LANG
   ```

When the user explicitly asks for journal-review prose, set
`--report-style peer-review`. `review_report.md` remains the primary
artifact in the workspace root; `peer_review_report.md` is generated as
a companion under `artifacts/summary/` for that style.

After consolidation, the deep-review workflow optionally invokes
`agents/revision_suggestion_agent.md` to produce
`artifacts/data/revision_suggestions.json` with concrete original/suggested
text pairs and additional actions. When the file is present,
`revision_suggestions.md` and its HTML twin pick it up automatically; when
absent, both fall back to the priority/section roadmap skeleton.

### `gate`

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode gate ...
```

Run **EIC Screening** (Phase 0.5) using `agents/editor_in_chief_agent.md`
first; report PASS/FAIL; verdict -> EIC -> blockers -> advisory. A desk-reject
verdict is a gate blocker. Critical `PRESUBMISSION` only blocks the gate.

### `re-audit`

Requires `--previous-report PATH`.

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode re-audit --previous-report <path> ...
uv run python -B "$SKILL_DIR/scripts/diff_review_issues.py" <old_final_issues.json> <new_final_issues.json>
```

Present root-cause-aware status labels: `FULLY_ADDRESSED`,
`PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`.

### `polish`

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode polish ...
```

If blockers exist, stop and report them. Only proceed into polishing if the
precheck is safe.
