# Changelog

## 0.2.4 — 2026-08-15

- Added a native DeepSeek Harness plugin bundle that exposes the existing Skill without additional runtime code.
- Added profile-scoped DeepSeek Harness installation, verification, update, invocation, and removal guidance.
- Moved the Skill version into portable `metadata.version` frontmatter.
- Removed tracked Python bytecode caches from release and plugin packages.

## 0.2.3 — 2026-08-05

- Added optional, selective `featured_figure` metadata for paper nodes.
- Added source, rights, caption, alt-text, selection-reason, and local/remote asset contracts.
- Added local figure embedding to standalone HTML, figure display cards, and missing/unsafe-asset validation.
- Added expansion-merge support for copying figure assets from a branch into the base run.
- Added figure-selection guidance that prioritizes explanatory value over decoration.

## 0.2.2 — 2026-08-05

- Changed the default paper-summary audience to field-relevant readers who have not read the paper.
- Added structured `reader_summary` content covering background, problem, approach, findings, significance, limitations, and optional concept definitions.
- Added summary-policy configuration, input/schema validation, page-side structured paper guides, and clarity audits.
- Updated sample graphs and pages to demonstrate explanatory Chinese paper summaries.

## 0.2.1 — 2026-08-05

- Added structured preprint, publication-type, formal venue, peer-review, and version-family metadata.
- Added a distinct top-venue badge that requires an explicit tier basis and as-of date.
- Changed latest-increment highlighting so revision-1 baseline graphs are never marked wholesale as newly added/updated.
- Added `meta.latest_increment`, baseline-safe rendering, validation rules, and initial/expanded HTML examples.

## 0.2.0 — 2026-08-05

- Added node-centered incremental research from any reviewed graph node.
- Added revisioned graph patches, safe merge, expansion history, and delta reporting.
- Added page-side export of editable expansion requests and latest-increment filtering.
- Added first-class `zh-CN`, `en`, and `bilingual` output contracts.
- Added localized graph fields and terminology-glossary guidance.
- Added expansion request and graph patch schemas, task documentation, scripts, and examples.
