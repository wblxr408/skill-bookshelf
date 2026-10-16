## v3.6.6 Generator-Evaluator Contract Protocol

> Authoritative orchestration block for the v3.6.6 contract-gated phase splits inside `academic-paper full` mode. Schema 13.1 since v3.6.6 (`shared/sprint_contract.schema.json`). Templates: `shared/contracts/writer/full.json` + `shared/contracts/evaluator/full.json`. Design spec: `docs/design/2026-04-27-ars-v3.6.6-generator-evaluator-contract-design.md` §5.
>
> **Applies to `academic-paper full` mode only.** Nine non-full modes (`plan`, `outline-only`, `revision`, `revision-coach`, `abstract-only`, `lit-review`, `format-convert`, `citation-check`, `disclosure`) are byte-equivalent across v3.6.5 → v3.6.6 and do not invoke this protocol. (The later-added `rebuttal-audit` mode is likewise non-full and does not invoke this protocol.) Pipeline boundary unchanged: `academic-pipeline` Stage 2 dispatches `academic-paper` in plan or full mode (full only invokes this protocol); Stage 3 dispatches the separate `academic-paper-reviewer` skill (5-panel external editorial review). The in-pair Phase 6 evaluator under this protocol and the Stage 3 reviewer are different review layers — see design doc §5.1 audit conclusion 2.

### Overview

v3.6.6 splits Phase 4 (writer drafting) and Phase 6 (in-pair evaluator review) into paper-blind / paper-visible call pairs gated by the `writer_full` and `evaluator_full` contracts. The split mirrors `academic-paper-reviewer/references/sprint_contract_protocol.md` (the v3.6.2 reviewer pattern) but adapts it for single-agent generator modes that have no panel and (for the writer) no scoring_plan.

The load-bearing mechanism is the **physical separation of calls**: writer Phase 4a never sees the runtime drafting artefacts; evaluator Phase 6a never sees the writer Phase 4b draft. This destroys the "read the paper, then rationalise the standard" drift path on the in-pair self-quality gate.

### Four-call structure

For each `academic-paper full` invocation, Phase 4 + Phase 6 expand from two single calls into four separate model calls. Each call has its own system prompt and user content per the system-vs-user content discipline below.

1. **Phase 4a — writer paper-blind pre-commitment.**
   - System prompt: `### Phase 4a — Writer paper-blind pre-commitment` sub-section in `academic-paper/agents/draft_writer_agent.md` § "v3.6.6 Generator-Evaluator Contract Protocol".
   - User content: `writer_full` contract JSON + paper metadata only (`title`, `field`, `word_count`).
   - Output: `## Acceptance Criteria Paraphrase` section + terminal `[PRE-COMMITMENT-ACKNOWLEDGED]` tag.
   - Lint: 3 structural checks (see § "Phase 4a / 6a output lint" below).
2. **Phase 4b — writer paper-visible drafting + self-scoring.**
   - System prompt: `### Phase 4b — Writer paper-visible drafting + self-scoring` sub-section in the same agent file.
   - User content: `writer_full` contract JSON (re-injected) + Phase 4a output wrapped in `<phase4a_output>...</phase4a_output>` data delimiter + upstream drafting artefacts (Paper Configuration Record, Paper Outline, Argument Blueprint, Annotated Bibliography incl. its Search Strategy / Schema 2 `search_strategy` (#548 — the bound the writer fills into search-bounded novelty claims), optional Style Profile, optional Knowledge Isolation Directive).
   - Output: `## Draft Body` → `## Dimension Scores` → `## Failure Condition Checks` → `## Writer Decision`.
   - Lint: 4 structural checks (see § "Phase 4b / 6b output lint" below).
3. **Phase 6a — evaluator paper-blind pre-commitment.**
   - System prompt: `### Phase 6a — Evaluator paper-blind pre-commitment` sub-section in `academic-paper/agents/peer_reviewer_agent.md` § "v3.6.6 Generator-Evaluator Contract Protocol".
   - User content: `evaluator_full` contract JSON + paper metadata + the writer's most recent `<phase4a_output>` (the writer artefact the evaluator must verify per `disagreement_handling.pre_commitment_check_protocol.check_writer_artifact`).
   - Output: `## Contract Paraphrase` + `## Scoring Plan` (per-dimension `dimension_id` / `what_to_look_for` / `what_triggers_block` / `what_triggers_warn`) + terminal `[PRE-COMMITMENT-ACKNOWLEDGED]` tag.
   - Lint: 5 structural checks.
4. **Phase 6b — evaluator paper-visible scoring + decision.**
   - System prompt: `### Phase 6b — Evaluator paper-visible scoring + decision` sub-section in the same agent file.
   - User content: `evaluator_full` contract JSON (re-injected) + Phase 6a output wrapped in `<phase6a_output>...</phase6a_output>` + the writer's `<phase4a_output>` (unconditional per `pre_commitment_check_protocol.check_writer_artifact`) + the writer Phase 4b draft (the artefact under review).
   - Output: `## Dimension Scores` → `## Failure Condition Checks` → `## Review Body` → `## Evaluator Decision`.
   - Lint: 5 structural checks.

### System prompt vs user content discipline

Mirrors `sprint_contract_protocol.md` §2 reviewer pattern verbatim:

- **System prompt carries invariant policy text only**: the phase sub-section instructions from the agent file's `## v3.6.6 Generator-Evaluator Contract Protocol` block, the lint description, and the phase-boundary tag conventions.
- **User content carries the contract JSON (re-injected per call) plus the runtime inputs allowed at that phase**: paper metadata, `<phase4a_output>` / `<phase6a_output>` delimiter blocks, upstream drafting artefacts, the paper draft.
