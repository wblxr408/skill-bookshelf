## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `compile` | Typst build, export, font, or watch issues | `uv run python $SKILL_DIR/scripts/compile.py main.typ` | `references/modules/COMPILE.md` |
| `format` | Venue/layout review for a Typst paper | `uv run python $SKILL_DIR/scripts/check_format.py main.typ` | `references/modules/FORMAT.md` (load `templates/<venue>.md` instead of the full `references/VENUES.md` when a venue is named) |
| `bibliography` | BibTeX or Hayagriva validation | `uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --typ main.typ` | `references/modules/BIBLIOGRAPHY.md` |
| `grammar` | Grammar cleanup on Typst prose | `uv run python $SKILL_DIR/scripts/analyze_grammar.py main.typ --section introduction` | `references/modules/GRAMMAR.md` |
| `sentences` | Long or dense sentence diagnostics | `uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --section introduction` | `references/modules/SENTENCES.md` |
| `logic` | Argument flow, introduction funnel, cross-section closure, and abstract/conclusion alignment review | `uv run python $SKILL_DIR/scripts/analyze_logic.py main.typ --section methods` | `references/modules/LOGIC.md` |
| `literature` | Related Work is list-like, under-compared, or missing a literature-backed gap | `uv run python $SKILL_DIR/scripts/analyze_literature.py main.typ --section related` | `references/modules/LITERATURE.md` |
| `expression` | Tone and expression polishing | `uv run python $SKILL_DIR/scripts/improve_expression.py main.typ --section methods` | `references/modules/EXPRESSION.md` |
| `translation` | Chinese/English academic translation in Typst context | `uv run python $SKILL_DIR/scripts/translate_academic.py input_zh.txt --domain deep-learning` | `references/modules/TRANSLATION.md` |
| `title` | Generate, compare, or optimize Typst paper titles | `uv run python $SKILL_DIR/scripts/optimize_title.py main.typ --check` | `references/modules/TITLE.md` |
| `pseudocode` | Review `algorithmic` / `algorithm-figure` / `lovelace` output for IEEE-like safety, captions, and comment length | `uv run python $SKILL_DIR/scripts/check_pseudocode.py main.typ --venue ieee` | `references/modules/PSEUDOCODE.md` |
| `deai` | Reduce English or Chinese AI-writing traces while preserving Typst syntax | `uv run python $SKILL_DIR/scripts/deai_check.py main.typ --section introduction` | `references/modules/DEAI.md` |
| `experiment` | Inspect experiment-section clarity, discussion layering, and reporting quality | `uv run python $SKILL_DIR/scripts/analyze_experiment.py main.typ --section experiment` | `references/modules/EXPERIMENT.md` |
| `tables` | Table structure validation, three-line table generation | `uv run python $SKILL_DIR/scripts/check_tables.py main.typ` | `references/modules/TABLES.md` |
| `abstract` | Abstract five-element structure diagnosis and word count validation | `uv run python $SKILL_DIR/scripts/analyze_abstract.py main.typ` | `references/modules/ABSTRACT.md` |
| `adapt` | Journal adaptation: reformat paper for a different venue | (LLM-driven workflow) | references/modules/ADAPT.md |
