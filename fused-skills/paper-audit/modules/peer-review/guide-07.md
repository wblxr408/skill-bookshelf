## Operational Modes (6 Modes)

| Mode | Trigger | Agents | Output |
|------|---------|--------|--------|
| `full` | Default / "full review" | All 7 agents | 5 review reports + Editorial Decision + Revision Roadmap |
| **`re-review`** | **Pipeline Stage 3' / "verification review"** | **Per-item routed seat verifiers (personas from the frozen Round-1 cards, §10 competence routing — Phase 1/2A) + eic/editorial_synthesizer (integration + Phase 2B + decision derivation; field_analyst NOT re-run — `re_review_mode_protocol.md` § Yardstick Continuity). Dispatched under the #576 three-gate contract (`shared/contracts/re_review/` + `scripts/check_re_review_synthesis.py`) — legacy single-pass only behind `ARS_RE_REVIEW_LEGACY=1`** | **Revision response checklist + residual issues + new Decision (or deferral/abort per contract)** |
| `quick` | "quick review" | field_analyst + eic | EIC quick assessment + key issues list (15-minute version) |
| `methodology-focus` | "check methodology" | field_analyst + eic + methodology_reviewer | In-depth methodology review report (panel 2 under v3.6.2 sprint contract: EIC + methodology) |
| `guided` | "guide me" | All + Socratic dialogue | Socratic issue-by-issue guided review |
| **`calibration`** (v3.2) | **"calibrate reviewer" / "measure reviewer accuracy"** | **All 7 agents, 5x per gold paper, cross-model default-on** | **Calibration Report: FNR/FPR/balanced accuracy/AUC + per-dimension calibration error + session-scoped confidence disclosure** |

### Mode Selection Logic

```
"Review this paper"                      -> full
"Give me a quick look at this paper"     -> quick
"Help me check the methodology"          -> methodology-focus
"Does this paper have methodology issues"-> methodology-focus
"Guide me to improve this paper"         -> guided
"Walk me through the issues in my paper" -> guided
"Verification review" / "Check revisions"-> re-review
"How accurate is your review scoring?"   -> calibration
"Calibrate against these 10 papers"      -> calibration
```

---
