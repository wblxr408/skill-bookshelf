# Reader-Oriented Paper Summary Extraction Prompt

Given the focal research question and a paper, produce a structured paper card for a reader who is familiar with the broad field but has **not read this paper**.

## Reader model

Assume the reader:

- understands the general discipline and common foundational ideas;
- does not know this paper's setup, terminology, architecture, argument, experiments, or results;
- should be able to understand why the paper exists, what it does, and why it matters without opening the PDF;
- may not know a paper-specific acronym, benchmark protocol, component name, or historical baseline.

## Exposition rules

- Begin with the background situation and the unresolved problem. Do not begin with a dense list of components.
- Define every paper-specific or non-obvious term before relying on it.
- Expand acronyms on first use unless they are truly universal in the focal field.
- Explain what each major component does and why it is needed; naming a component is not an explanation.
- When saying "improves", "outperforms", "more efficient", or "deeper", identify the baseline, metric, data regime, or constraint.
- Separate the paper authors' claims from the analyst's interpretation.
- Explain experimental conditions needed to interpret the result.
- State limitations, assumptions, failure cases, and applicability boundaries in accessible language.
- Use equations only when they materially improve understanding; introduce every symbol.
- Analogies may assist understanding but must not replace the actual mechanism.
- Summarize only content relevant to the focal question, while including enough background to make that content intelligible.
- Cite evidence IDs for every non-obvious statement.

## Required output

Produce both:

1. `summary`: a compact focus-relevant lineage statement.
2. `reader_summary`: a structured explanation with `audience: field_familiar_unread` and localized content under `zh-CN` and/or `en`.

Each localized `reader_summary` must contain:

- `background`: what the field did before this paper and why the issue matters;
- `problem`: the exact problem, constraint, or disputed question;
- `approach`: a plain but technically faithful walkthrough of the core idea and major components;
- `key_findings`: contextualized findings, each identifying the comparison or evaluation condition;
- `why_it_matters`: how the paper changes the focal lineage or the reader's understanding;
- `limitations`: assumptions, missing evidence, failure cases, or scope boundaries;
- `concepts`: optional term/explanation pairs for concepts that cannot be assumed.

Also output:

- role_in_lineage
- contribution
- inherited_from
- changed_vs_predecessor
- experiments
- results
- code_and_data
- relevant_claims
- evidence_ids
- publication_status
- publication_type
- primary_venue
- peer_reviewed
- version_family
- venue_tier and venue_tier_basis when applicable
- confidence

## Quality test

Before finalizing, ask:

> Could a colleague in this field who has never opened the paper explain the problem, the mechanism, the main evidence, and the limitations after reading this card?

If not, add the missing background or explanation. Do not write as though the reader merely needs a memory refresh.

## Localization

- Accept `output_language` as `zh-CN`, `en`, or `bilingual`.
- Write all analyst-authored fields in that language.
- Preserve the canonical original paper title and identifiers.
- In bilingual mode, return both localized reader-summary payloads.
- In Chinese mode, use clear, complete sentences; introduce `中文译名（Original Term）` on first mention when helpful.
- Retain exact original claim wording when its modality or scope matters, followed by a Chinese explanation.

## Optional featured figure decision

Decide explicitly whether this paper benefits from one representative figure for a reader who has not read it. Return no figure when prose is sufficient or no responsible, legible asset is available. When selecting one, output `featured_figure` with:

- `kind` and `display_kind`;
- localized caption and alt text;
- a short reader note explaining what the figure shows and how it connects to the core contribution;
- selection reason;
- exact source citation, paper version, figure number/page, URL, license or usage basis, and rights status;
- a local asset path under `assets/figures/<node-id>/` when available.

Prefer method overviews, architecture/pipeline diagrams, conceptual diagrams, or decisive qualitative results. Never choose a figure only because it is visually attractive. Never imply that an analyst reconstruction is an original paper figure.
