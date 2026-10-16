# Read and Extract

## Reading order

1. metadata, abstract, introduction, and conclusion
2. the problem setup and the prior approach the paper is reacting to
3. related work and citation contexts around focal papers
4. method, assumptions, and the function of each major component
5. experiments, tables, figures, ablations, and comparison baselines
6. limitations and appendices
7. repository and supplementary material

## Reader model

Write for a person who works in or near the field but has not read the paper. The explanation should not assume knowledge of the paper's terminology, architecture diagram, benchmark setup, or claimed contribution.

## Focused paper card

Extract:

- one-sentence role in the lineage
- background before the paper and why the problem arose
- problem addressed and scope
- prerequisite or paper-specific concepts, each briefly defined
- focus-relevant contribution
- inherited components and their origin papers
- changed components and why those changes are expected to help
- a step-by-step or component-by-component explanation of the method/argument
- evaluation setup, named baselines, metrics, and data regime
- strongest result with enough comparison context to interpret it
- why the result matters
- key limitations, assumptions, and applicability boundaries
- explicit criticism or disagreement
- code/data links
- preprint/publication state, formal venue, peer-review state, and version-family links
- venue-tier basis when a top-venue label is present
- confidence and access level

Store the compact focal relation in `summary`, and the self-contained explanation in `reader_summary` using the structure defined in `schemas/graph.schema.json`.

## Language and clarity rules

- Explain a concept before using it as part of another explanation.
- Expand paper-specific acronyms on first use.
- Replace vague comparison phrases with named baselines and conditions.
- Avoid unexplained strings of architecture names, benchmark names, or noun phrases.
- Prefer direct sentences that state who does what and why.
- Do not merely rewrite the abstract; synthesize information from methods, experiments, limitations, and related work.
- Do not over-explain general undergraduate-level facts that the declared audience can reasonably know.

## Evidence record

Each record should contain:

- evidence_id
- paper_id or repository_id
- source URL/file
- section/page/file path
- exact or closely paraphrased content
- evidence type
- supported node/edge/claim IDs
- access date

Avoid long copyrighted quotations. Use short snippets and paraphrase.

## Select an optional featured figure

For a paper that is central, visually distinctive, or difficult to understand from prose alone, select at most one `featured_figure`. Do not add one merely to fill space. Prefer, in order:

1. method overview or end-to-end pipeline;
2. architecture or conceptual diagram;
3. qualitative result that directly demonstrates the paper's main contribution;
4. compact benchmark summary only when it is central and remains legible.

Avoid decorative figures, generic dataset examples, dense tables, tiny multi-panel plots, and figures whose meaning depends on several pages of unexplained context. Save a local web-friendly asset under `assets/figures/<node-id>/` when permitted. Record the exact paper version, figure number/page, source URL, citation, rights status or usage basis, caption, accessible alt text, and a short reader note explaining what to look at. If the original cannot be responsibly displayed, use no figure or provide a clearly labeled analyst reconstruction; never present a reconstruction as the paper's original figure.
