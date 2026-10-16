## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `compile` | Thesis build fails or toolchain is unclear | `uv run python $SKILL_DIR/scripts/compile.py main.tex` | `references/modules/COMPILE.md` |
| `format` | User asks about thesis formatting or GB/T 7714 layout | `uv run python $SKILL_DIR/scripts/check_format.py main.tex` | `references/modules/FORMAT.md`（已知模板时改读 `templates/<template>.md`，如 thuthesis、pkuthss、generic） |
| `structure` | Need chapter/section map or thesis skeleton overview | `uv run python $SKILL_DIR/scripts/map_structure.py main.tex` | `references/STRUCTURE_GUIDE.md` |
| `consistency` | Terms, abbreviations, or naming drift across chapters | `uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --terms` | `references/modules/CONSISTENCY.md` |
| `template` | Need to identify or validate thesis class/template | `uv run python $SKILL_DIR/scripts/detect_template.py main.tex` | `references/modules/TEMPLATE.md` |
| `bibliography` | GB/T 7714 or BibTeX validation | `uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --standard gb7714` | `references/modules/BIBLIOGRAPHY.md` |
| `title` | Optimize Chinese thesis titles and chapter titles | `uv run python $SKILL_DIR/scripts/optimize_title.py main.tex --check` | `references/modules/TITLE.md` |
| `deai` | Reduce AI-writing traces in visible Chinese prose | `uv run python $SKILL_DIR/scripts/deai_check.py main.tex --section introduction` | `references/modules/DEAI.md` |
| `logic` | Check logical coherence, introduction funnel, heading lead-ins, lit review quality, chapter mainline, and cross-section closure | `uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex --section related` | `references/modules/LOGIC.md` |
| `literature` | 文献综述像流水账、缺少比较分析、研究空白没有被自然推出 | `uv run python $SKILL_DIR/scripts/analyze_literature.py main.tex --section related` | `references/modules/LITERATURE.md` |
| `experiment` | Review experiment chapter language, discussion layering, and conclusion completeness | `uv run python $SKILL_DIR/scripts/analyze_experiment.py main.tex --section experiments` | `references/modules/EXPERIMENT.md` |
| `tables` | 表格结构校验、三线表生成、booktabs 检查 | `uv run python $SKILL_DIR/scripts/check_tables.py main.tex` | `references/modules/TABLES.md` |
| `abstract` | 摘要五要素结构诊断与字数校验 | `uv run python $SKILL_DIR/scripts/analyze_abstract.py main.tex --lang zh` | `references/modules/ABSTRACT.md` |
