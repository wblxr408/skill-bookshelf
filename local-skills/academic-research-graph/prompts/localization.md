# Output Localization

Requested output language: {{output_language}}

Rules:

1. Preserve canonical paper titles, author names, venue names, identifiers, repository paths, code symbols, benchmark names, and metrics.
2. Write all analyst-authored summaries, relationship explanations, conflict assessments, report headings, and UI labels in the requested language.
3. For `zh-CN`, use consistent Simplified Chinese terminology. On first mention, add the original English term in parentheses when useful.
4. For `bilingual`, populate language maps rather than mixing languages unpredictably.
5. Preserve exact original claim wording when wording itself matters, followed by a faithful localized explanation.
6. Do not make translations sound more certain than the source. Preserve modality, scope, and negation.
7. Maintain `meta.terminology_glossary` for ambiguous or repeatedly used technical terms.


## Reader-oriented Chinese explanations

For paper `reader_summary` fields, assume the Chinese reader understands the broad field but has not read the paper. Do not translate an abstract sentence by sentence. Reconstruct the explanation in a pedagogical order: background, problem, concept definitions, approach, findings, significance, and limitations.

Avoid unexplained acronym chains and long stacks of untranslated component names. On first mention, explain what a component does. Preserve original technical terms in parentheses when they help lookup. Comparative claims must name the baseline, metric, or data condition.
