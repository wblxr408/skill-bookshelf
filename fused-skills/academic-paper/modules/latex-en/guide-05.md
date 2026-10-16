## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `compile` | Build fails or the user wants a fresh compile | `uv run python -B $SKILL_DIR/scripts/compile.py main.tex` | `references/modules/COMPILE.md` |
| `format` | User asks for LaTeX or venue formatting review | `uv run python -B $SKILL_DIR/scripts/check_format.py main.tex` | `references/modules/FORMAT.md` (load `templates/<venue>.md` instead of the full `references/VENUES.md` when a venue is named) |
| `bibliography` | Missing citations, unused entries, BibTeX validation | `uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --tex main.tex` | `references/modules/BIBLIOGRAPHY.md` |
| `grammar` | Grammar and surface-level language fixes | `uv run python -B $SKILL_DIR/scripts/analyze_grammar.py main.tex --section introduction` | `references/modules/GRAMMAR.md` |
| `sentences` | Long, dense, or hard-to-read sentences | `uv run python -B $SKILL_DIR/scripts/analyze_sentences.py main.tex --section introduction` | `references/modules/SENTENCES.md` |
| `logic` | Weak argument flow, unclear transitions, introduction funnel problems, or abstract/conclusion misalignment | `uv run python -B $SKILL_DIR/scripts/analyze_logic.py main.tex --section methods` | `references/modules/LOGIC.md` |
| `literature` | Related Work is list-like, under-compared, or missing an evidence-backed research gap | `uv run python -B $SKILL_DIR/scripts/analyze_literature.py main.tex --section related` | `references/modules/LITERATURE.md` |
| `expression` | Academic tone polish without changing claims | `uv run python -B $SKILL_DIR/scripts/improve_expression.py main.tex --section related` | `references/modules/EXPRESSION.md` |
| `translation` | Chinese-to-English academic translation or bilingual polishing | `uv run python -B $SKILL_DIR/scripts/translate_academic.py input.txt --domain deep-learning` | `references/modules/TRANSLATION.md` |
| `title` | Generate, compare, or optimize paper titles | `uv run python -B $SKILL_DIR/scripts/optimize_title.py main.tex --check` | `references/modules/TITLE.md` |
| `figures` | Figure existence, extension, DPI, or caption review | `uv run python -B $SKILL_DIR/scripts/check_figures.py main.tex` | `references/REVIEWER_PERSPECTIVE.md` |
| `pseudocode` | IEEE-safe pseudocode review, `algorithm2e` cleanup, caption/label/reference checks, and comment-length review | `uv run python -B $SKILL_DIR/scripts/check_pseudocode.py main.tex --venue ieee` | `references/modules/PSEUDOCODE.md` |
| `deai` | Reduce AI-writing traces while preserving LaTeX syntax | `uv run python -B $SKILL_DIR/scripts/deai_check.py main.tex --section introduction` | `references/modules/DEAI.md` |
| `experiment` | Inspect experiment design/write-up quality, discussion depth, discussion layering, and conclusion completeness | `uv run python -B $SKILL_DIR/scripts/analyze_experiment.py main.tex --section experiments` | `references/modules/EXPERIMENT.md` |
| `tables` | Table structure validation, three-line table generation, or booktabs review | `uv run python -B $SKILL_DIR/scripts/check_tables.py main.tex` | `references/modules/TABLES.md` |
| `abstract` | Abstract five-element structure diagnosis and word count validation | `uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.tex` | `references/modules/ABSTRACT.md` |
| `adapt` | Journal adaptation: reformat paper for a different venue | (LLM-driven workflow) | references/modules/ADAPT.md |
