## What This Skill Produces

- `quick-audit`: fast submission-readiness screen with script-backed findings,
  including `PRESUBMISSION`
- `deep-review`: reviewer-style structured issue bundle with major/moderate/
  minor findings
- `gate`: PASS/FAIL decision calibrated for submission blockers;
  `PRESUBMISSION` Major/Minor findings remain advisory
- `re-audit`: compare current issue bundle against a previous audit, including
  mechanical regression findings
- `polish`: precheck-only handoff into a polishing workflow

The primary product is no longer just a score. For `deep-review`, the
workspace root contains exactly four files for the reader:

- `review_report.md` — the primary deep-review report
- `revision_suggestions.md` — concrete fix recommendations for each
  Major/Moderate issue, including suggested rewrites (when applicable)
- `review_report.html` — HTML twin of the primary report
- `revision_suggestions.html` — HTML twin of the suggestions

Everything else lives under `artifacts/` for verification and tooling:

- `artifacts/summary/` — `paper_summary.md`, `overall_assessment.txt`,
  `peer_review_report.md`
- `artifacts/data/` — `final_issues.json`, `all_comments.json`,
  `claim_map.json`, `section_index.json`, `revision_suggestions.json`,
  `revision_trajectory.md`
- `artifacts/meta/` — `metadata.json`, `checkpoint.json`,
  `phase0_context.md`, `full_text.md`
- `artifacts/sections/`, `artifacts/comments/`, `artifacts/committee/`,
  `artifacts/references/`

The report language is controlled by `--lang en|zh` (default: auto-detect
from `metadata.json`, fallback `en`). The language switch only affects
report headings, labels, and table headers — issue quotes, source tags
(`[Script]`, `[LLM]`), and structured field values stay in their original
form.
