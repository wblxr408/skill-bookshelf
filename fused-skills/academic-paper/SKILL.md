---
name: academic-paper
description: Write and revise academic papers or theses in prose, LaTeX, and Typst; handle language, citations, formatting, compilation, and reviewer responses.
metadata:
  version: "fusion-2026-10-05"
---

# Academic Paper — unified writing and revision

Read [the execution contract](references/fusion-policy.md). Use the supplied manuscript, venue, language, and requested change to choose a route. Preserve claims and evidence, citation keys, math, labels, macros, and formatting outside scope. Research new evidence only when the request needs it; never invent sources or results.

| Need | Read next |
|---|---|
| Full draft, plan, outline, abstract, title, literature review, revision coaching, reviewer-response revision, disclosure, authorship, funding, or format conversion | [writing modes](references/writing-modes.md), then the relevant section in [writing module](modules/writing/PLAYBOOK.md) |
| Existing English LaTeX conference/journal paper | [LaTeX English router](modules/latex-en/PLAYBOOK.md); select its Module Router and requested module |
| Existing Chinese thesis, university template, GB/T 7714, terminology consistency, or chapter structure | [Chinese thesis router](modules/latex-zh/PLAYBOOK.md) |
| Existing English/Chinese Typst manuscript, BibTeX/Hayagriva, export, fonts, watch, venue layout | [Typst router](modules/typst/PLAYBOOK.md) |
| Match comments to a revised manuscript or audit a rebuttal | `$paper-audit` revision verification; perform requested source edits here |

For a single requested module, load only that module's guide. For compatible requested checks, run dependency prerequisites once, then only the affected checks. Existing source-specific scripts and venue templates remain available in the selected module; `SKILL_DIR` means that module's directory.

Create/edit a standalone `.tex` in the built-in Codex editor by default, open it, compile with `compile_latex_document`, and fix errors within its repair limits. Multi-file TeX projects use the preserved compile module and project toolchain. Preserve the file and report compiler limitations rather than installing a new toolchain unasked. Ordinary prose improvements do not trigger full paper generation, all review roles, or compilation of unrelated formats.

Use `$bib-search-citation` for a local library search and `$cover-letter` for a submission letter. Full research-to-publication orchestration remains `$academic-pipeline`, with review routed to `$paper-audit`. [Runtime adapters](references/runtime-adapters.md) cover missing upstream tool/protocol dependencies.
