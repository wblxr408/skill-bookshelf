# Expand from an Existing Node

## Goal

Continue research from one reviewed node without discarding or silently rebuilding the existing graph. Produce an evidence-backed patch, merge it into a new graph revision, and preserve a clear delta.

## Inputs

- existing `graph.json` and, when available, its run directory
- `start_node_id`
- local expansion focus
- direction: backward, forward, both, related, conflicts, benchmark_use, or repository
- branch depth and budgets
- output language

## Procedure

1. Verify graph ID, revision, and selected node.
2. Read the selected node, incident edges, cited evidence, and related candidate-ledger entries.
3. Treat the selected node as a local seed while preserving the original global seed and roles.
4. Search only the uncovered neighborhood unless the request explicitly refreshes prior searches.
5. Rank by local relevance and marginal value to the existing graph.
6. Deep-read the selected branch using the normal evidence rules.
7. Reuse canonical IDs for records already present.
8. Write `graph_patch.json`; do not mutate the base graph during research.
9. Include evidence for all new or changed semantic relationships.
10. Run `merge_expansion.py`, then validate and re-render the complete graph.


## Reader-summary continuity

Every newly added paper node must include a complete `reader_summary` for the graph's declared output language. When an existing paper node is updated because new evidence changes its interpretation, revise the relevant reader-summary sections rather than only changing the compact lineage `summary`.

The expansion must preserve the base graph's `meta.summary_policy` unless the request explicitly supplies a compatible policy. A local branch is not allowed to regress into abstract-like shorthand or assume the reader has read either the selected node or the newly discovered papers.

## Merge rules

- append by default; no deletion unless a separately reviewed correction workflow authorizes it
- preserve old fields that the patch does not mention
- union evidence IDs, links, notes, and expansion provenance
- archive the old graph revision
- mark added and updated revision numbers
- append an expansion-history record
- explain any main-path or conflict reinterpretation in the delta report

## Required outputs

- `expansion_request.json`
- `graph_patch.json`
- updated `graph.json`
- `expansion_manifest.json`
- `delta_report.json` and a human-readable `delta_report.md`
- updated `index.html` with latest-increment highlighting

## Language

All analyst-authored patch content must follow `output_language`. Preserve canonical original titles and identifiers. In Chinese mode, provide Chinese summaries and relationship explanations while retaining original titles and key claim wording where needed.

If an expansion adds or updates a `featured_figure`, place the asset under the expansion directory using a path such as `assets/figures/<node-id>/<filename>`. `merge_expansion.py` copies safe local assets into the base run and rewrites collision paths when necessary. Do not reference arbitrary absolute paths or paths outside the expansion directory.
