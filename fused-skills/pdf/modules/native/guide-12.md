## Final response

### Final response citations

Place `:codex-file-citation{...}` inline in prose, not in a trailing list. Use `purpose="source"` for Q&amp;A/no-op and `purpose="output"` for create/edit.

- [HARD REQUIREMENT] Create/edit: cite each final PDF exactly once with a plain output citation. Summarize representative changes; do not cite every page or add a separate filename, path, or Markdown link. Example: `Created :codex-file-citation{path="/abs/path/report.pdf" purpose="output"}, with the completed analysis and appendix.`
- Q&amp;A/no-op: do not edit or re-export. Inspect the complete relevant pages, preserve material headings, table/figure labels, footnotes, sources, and sample sizes, and cite each source PDF once with a plain source citation.

PDF citations currently support only plain file citations. Do not add `artifact_kind`, `page_number`, or other locators. Never cite rendered PNGs, scratch files, builders, or QA intermediates unless asked.

### Final response suggested followups

- After successfully creating, editing, or analyzing an artifact, finish your final response with 3 useful next actions tailored to the artifact and the user's goal. Completing the requested work is not a reason to skip these actions: they help the user continue from the result. Do not perform the actions unless the user chooses one.
- Each action must be a distinct, concrete request the user could send next. Do not repeat completed work or invent filler. Omit the list if the user declines suggestions, the requested work fails, or no genuinely useful next action remains.
- Present each action as an unescaped Markdown list item using this exact syntax: `- :codex-followup[Short action]{prompt="Complete request for that action"}`.
