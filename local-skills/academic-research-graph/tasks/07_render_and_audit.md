# Render and Audit

## Required views

- complete reviewed graph
- main lineage only
- conflict edges
- benchmark adoption branch
- latest frontier
- repository/code relationships
- latest incremental expansion only, but only after a genuine expansion revision exists

## Visual conventions

- thick edge: main path
- dashed red edge: conflict/criticism
- blue edge: benchmark or dataset use
- purple edge: repository/code relationship
- seed node: emphasized border
- frontier node: recent marker
- latest-expansion node/edge: separate outline or dash pattern; never apply it to a revision-1 baseline
- paper detail: a structured guide for an informed non-reader, followed by the compact relation to the focal question
- paper detail: preprint-only vs formally published, exact conference/journal, peer-review status, and version family
- justified top venue: visually distinct badge plus visible tier basis

Do not encode meaning by color alone; also use labels, dash patterns, widths, and legends.

## Audit

Before delivery verify:

- every edge endpoint exists
- every substantive edge has evidence
- every conflict has an adjudication record
- every benchmark-use edge has direct evidence
- every repository claim has a commit and code location when possible
- all links are normalized
- duplicate versions are documented
- coverage numbers reconcile with the candidate ledger
- search cutoff date is explicit
- graph and report use the same IDs

## Node-centered continuation

The node detail panel must expose a “continue research from this node” action. In a standalone static page, this action exports an editable `expansion_request.json` containing graph ID, base revision, node ID, local focus, direction, depth, budgets, and output language. It must clearly state that the host agent performs retrieval and merge.

## Language audit

- UI labels follow `meta.output_language`.
- In Chinese mode, analyst-authored summaries and edge explanations are Chinese.
- Original titles and identifiers remain searchable.
- Bilingual fields display deterministically and do not overwrite canonical text.
- Every paper detail panel explains background, problem, approach, findings, significance, and limitations without assuming the paper has been read.
- Acronyms and paper-specific terms are expanded or defined before use.

## Baseline-versus-increment rule

A fresh graph (`revision == 1`, no expansion history, no `meta.latest_increment`) is a baseline. The renderer must omit the latest-increment filter and legend row, suppress incremental node/edge styling, and hide revision-added/updated fields. Enable them only when the current revision was created by an expansion merge.

## Featured-figure rendering audit

When a paper node contains `featured_figure`:

- render it near the top of the node detail panel, before the long reader guide;
- preserve aspect ratio and allow click-to-open when a source URL exists;
- show a localized caption, reader note, and compact attribution;
- expose alt text to assistive technology;
- label analyst reconstructions explicitly;
- embed local assets into the standalone HTML when under the configured size limit;
- do not silently hotlink remote images unless the run policy allows it;
- show a graceful metadata-only fallback if the image asset cannot be loaded.

Audit that every displayed figure has attribution, an alt description, a documented rights/usage status, and enough resolution to be legible without dominating the entire detail panel.
