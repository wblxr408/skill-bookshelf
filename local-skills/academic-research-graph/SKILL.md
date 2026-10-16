---
name: academic-research-graph
description: Build and incrementally extend an evidence-backed literature lineage and controversy graph from a paper, academic concept/claim, benchmark, paper-associated GitHub repository, or an existing graph node; analyze citation chains, substantive relationships, conflicts, benchmark adoption, and code; support Chinese, English, or bilingual output; optionally attach source-attributed representative paper figures; then render an interactive node-edge research map.
metadata:
  version: "0.2.4"
---

## 本机已安装的运行环境

本机依赖和调用方式见 [运行环境说明](references/research-runtime.md)。Python 脚本使用 `python`，并从本技能目录解析脚本的绝对路径；R 使用该说明中的 R 与包库路径。

# Academic Research Graph Skill

## Purpose

Use this skill when the user gives one of the following:

1. A specific academic paper: title, DOI, arXiv URL/ID, publisher URL, OpenAlex ID, Semantic Scholar ID, or PDF.
2. A specific academic concept, benchmark, method, claim, or disputed proposition.
3. A GitHub repository associated with an academic paper.
4. A node in a previously generated research graph that the user wants to investigate further and merge back into the same graph.

The output is not merely a citation list. It is a defensible research map that answers:

- Where did the focal idea come from?
- Which papers materially extended, applied, tested, criticized, contradicted, reproduced, or superseded it?
- Which citations are central and which are incidental?
- Which later works genuinely use the method, code, dataset, or benchmark?
- What are the main research lineages, branches, disagreements, and latest frontiers?
- How does the repository implement the paper, and where does the code diverge from the paper?
- What new branch emerges when research continues from a selected node, and how does it change the existing graph?

## Core principles

1. **Separate retrieval from analysis.** Maintain a broad candidate graph and a smaller evidence-reviewed analysis graph.
2. **Never equate citation with contribution.** A citation edge becomes a semantic relationship only after evidence is found in the citing or cited work.
3. **Never infer benchmark use from title, abstract, or bibliography alone.** Confirm use in methods, experiments, tables, configuration, or code.
4. **Treat conflict as claim-level, not paper-level.** Two papers conflict only when they address sufficiently comparable questions under sufficiently comparable assumptions.
5. **Preserve provenance.** Every important summary, relationship, and conflict must point to evidence and a source URL or document location.
6. **Prefer representative structure over exhaustive noise.** For foundational topics, cluster the field and select representative papers while preserving a candidate ledger.
7. **Report uncertainty and coverage limits.** Citation databases disagree and may omit works; never claim completeness without a coverage audit.
8. **Use lawful access paths.** Prefer open APIs, open-access copies, author manuscripts, and user-provided files. Do not bypass paywalls.
9. **Make graph growth incremental and reversible.** A node-centered expansion must preserve stable IDs, previous evidence, revision history, and a machine-readable delta; do not silently rebuild or overwrite the old graph.
10. **Publication-state and venue claims require provenance.** Record whether a paper is preprint-only, accepted, or published; preserve its version family; and mark a venue as top-tier only when the adopted field-specific rule, source, and as-of date are recorded.
11. **Honor the requested output language.** Research may use multilingual sources, but all analyst-authored summaries, relationship explanations, conflict assessments, report headings, and UI labels must be produced in `zh-CN`, `en`, or `bilingual` as requested.
12. **Explain papers for an informed non-reader.** Assume the reader works in or near the field but has never opened the paper. A paper explanation must establish the necessary background, define paper-specific or non-obvious concepts, state the problem before the solution, walk through the core idea in understandable language, and explain results, significance, limitations, and scope without relying on familiarity with the PDF.
13. **Use figures selectively and transparently.** A paper figure is optional. Include at most one only when it materially improves understanding; record exact attribution, rights or usage basis, accessible alt text, and whether it is an original figure, author asset, or analyst reconstruction.

## Inputs

Accept a structured input conforming to `schemas/input.schema.json`, or infer it from natural language.

Minimum natural-language input:

- focal item: paper / concept / claim / benchmark / GitHub repository
- research question or focus

Operation:

- `build`: construct a new graph from a paper, concept, claim, benchmark, or repository.
- `expand`: start from `start_node_id` in an existing `graph.json`, investigate that node locally, and merge the resulting branch into the same graph.

Optional controls:

- depth: `quick`, `standard`, `deep`, or `foundational`
- maximum candidate papers
- maximum deeply analyzed papers
- date range
- disciplines or venues
- source/search languages
- output language: `zh-CN`, `en`, or `bilingual`
- summary audience and exposition depth; default is `field_familiar_unread`, meaning a field-relevant reader who has not read the paper
- for expansion: base graph/run, start node ID, expansion focus, direction, branch depth, and branch budgets
- whether repository analysis is required
- whether selective paper featured figures are enabled, and whether local embedding or remote image loading is allowed
- whether to emphasize benchmark adoption, controversy, applications, or historical origin

If the user gives no explicit focus, infer the paper's central contribution from its title, abstract, introduction, and conclusion, then state the inferred focus.

## Output contract

Create a run directory containing:

- `research_report.md` — human-readable synthesis
- `graph.json` — reviewed node-edge graph
- `candidate_ledger.jsonl` — all discovered candidates with inclusion/exclusion status
- `papers.jsonl` — normalized paper records
- `evidence.jsonl` — evidence spans supporting summaries and relationships
- `run_manifest.json` — query, dates, sources, limits, warnings, and coverage statistics
- `index.html` — interactive research map generated from `graph.json`
- `assets/` — optional local figures or thumbnails; paper figures should normally live under `assets/figures/<node-id>/`
- `history/graph.rev-N.json` — immutable prior reviewed-graph revisions
- for an expansion run: `expansion_request.json`, `graph_patch.json`, `expansion_manifest.json`, and `delta_report.md`

Use `scripts/validate_graph.py` before delivery and `scripts/render_site.py` to produce the page. For node-centered continuation, use `scripts/init_expansion.py` to create a branch request and `scripts/merge_expansion.py` to merge an evidence-reviewed patch.

## Research modes and budgets

### quick

- 1-2 citation hops
- up to 80 candidates
- 15-30 deeply analyzed papers
- suitable for a focused paper or narrow benchmark

### standard

- adaptive 2-3 hops
- up to 300 candidates
- 40-90 deeply analyzed papers
- default mode

### deep

- adaptive 3+ hops where marginal yield remains high
- up to 1,000 candidates
- 80-180 deeply analyzed papers
- includes branch-specific searches and stronger coverage auditing

### foundational

Use for broad roots such as Transformer, diffusion models, or reinforcement learning.

- do not attempt to deeply analyze every citing paper
- construct clusters: origins, architectural variants, scaling, applications, evaluation, criticism, efficiency, safety, and latest frontier
- choose representative and bridge papers per cluster
- preserve aggregate counts and excluded candidate records

## Source strategy

Use multiple sources because no single graph is complete.

### Citation backbone

Preferred order:

1. OpenAlex for broad metadata, references, citing works, related works, topics, and citation counts.
2. Semantic Scholar for citation/reference cross-checking, influential citations, abstracts, and paper matching.
3. Crossref for DOI normalization, publisher metadata, updates, licenses, references, and citation counts where available.
4. arXiv for preprint metadata, version history, categories, and open full text.
5. Publisher or conference pages for authoritative versions and supplements.

Do not merge records solely by title similarity. Use DOI, arXiv ID, PMID, Corpus ID, or high-confidence title-author-year matching.

### Full text

Preferred order:

1. user-provided PDF
2. open-access publisher copy
3. arXiv or institutional manuscript
4. repository paper PDF
5. abstract-only analysis, clearly labeled as limited

When figures, tables, equations, or benchmark results are important, inspect the page image as well as parsed text. For central papers, also decide whether one figure materially improves first-time understanding. Selection is optional and explanatory, not decorative.

### Repository

Use:

- README and documentation
- `CITATION.cff`, `codemeta.json`, badges, DOI/arXiv links
- repository metadata, topics, releases, tags, issues, pull requests, and commit history
- source tree, entry points, configuration files, training/evaluation scripts, dataset loaders, checkpoints, and tests

Prefer cloning the repository at a pinned commit for code analysis. Record the commit SHA and analysis date.

## Workflow

### Phase 0 — Define the focal question

Create a `focus frame`:

- focal item
- exact question
- core contribution or claim
- inclusion criteria
- exclusion criteria
- desired temporal and citation depth
- expected output mode

Examples:

- “How did ViT inherit from Transformer and which later papers changed its data regime, architecture, or efficiency?”
- “Which works truly use the VillagerAgent benchmark, and what do they conclude about it?”
- “Does this repository faithfully implement the method described in the linked paper?”

### Phase 1 — Resolve the input

Follow `tasks/01_resolve_input.md`.

Produce one or more canonical seed records. A concept may need several seeds because origin can mean:

- first use of the term
- first formal definition
- first technical implementation
- first empirical demonstration
- first popularization

A repository may map to several papers; identify the primary paper and related technical reports.

### Phase 2 — Build the candidate graph

Follow `tasks/02_retrieve_candidate_graph.md`.

For each seed, retrieve:

- backward references
- forward citations
- related works
- papers sharing the method, benchmark, dataset, repository, or distinctive phrase
- latest citing works, sorted by publication date
- surveys and review papers that can reveal missing branches

Run adaptive snowballing. Expand a frontier paper when at least one condition holds:

- high relevance to the focal question
- bridge between clusters
- introduces a named variant or benchmark
- contains criticism, failure analysis, or contradictory findings
- is recent and appears to define the current frontier
- is repeatedly cited by already relevant papers

Stop expanding a branch when:

- the last expansion yields less than 10% new relevant candidates
- papers are mostly incidental citations
- the branch falls outside the focus frame
- the configured candidate budget is reached

Always keep discovered but excluded works in `candidate_ledger.jsonl`.

### Phase 3 — Normalize and deduplicate

Follow `tasks/03_normalize_and_rank.md`.

Build a canonical paper identity with:

- DOI
- arXiv ID and version
- OpenAlex ID
- Semantic Scholar Corpus ID
- publisher URL
- title aliases
- authors
- first-public date, publication status, document type, primary venue, and version family
- venue tier plus its explicit basis/as-of date when prestige labels are used

Merge preprint and published versions into a version family when appropriate, but preserve each version link, date, review status, and venue. The reviewed node must expose structured `publication.status`, `publication.type`, `publication.primary_venue`, and `publication.versions` fields. A `top` venue tier is invalid as an unexplained assertion: include `tier_basis` and `tier_as_of`, and prefer a user- or institution-supplied venue policy. Do not merge distinct workshop, conference, journal, and extended versions when their content materially differs.

### Phase 4 — Rank candidates for deep reading

Use `scripts/rank_candidates.py` as a transparent baseline, then adjust using research judgment.

Default priority components:

- 0.30 focus relevance
- 0.15 lineage importance
- 0.12 bridge centrality
- 0.12 methodological novelty
- 0.10 conflict or criticism likelihood
- 0.08 benchmark/repository evidence
- 0.08 recency/frontier value
- 0.05 evidence quality

Do not use raw citation count as the main ranking signal. Age-normalize influence and protect recent papers from being unfairly suppressed.

### Phase 5 — Read and extract evidence

Follow `tasks/04_read_and_extract.md`.

For each analyzed paper, extract only what is relevant to the focus, but make the explanation self-contained for a field-relevant reader who has not read the paper:

- the background situation before this paper and why the problem exists
- the precise problem and scope
- the minimum prerequisite concepts needed to follow the paper
- the contribution, stated after the problem is clear
- an understandable walkthrough of the method or argument, including the role of each major component
- data, benchmark, and experimental setup
- main results, expressed with enough context to understand what improved over what
- why the result matters to the focal research question and to the broader lineage
- limitations, assumptions, failure cases, and applicability boundaries
- relationship to earlier work
- relationship to later work
- code/data availability
- publication status, document type, peer-review status, primary venue, and version notes
- optional `featured_figure` metadata when one representative visual genuinely helps an unread-paper audience
- venue-tier label and its provenance when a top-venue badge is requested

Store two distinct layers:

1. `summary`: a compact statement of the paper's relation to the focal question.
2. `reader_summary`: a structured paper explanation for an informed non-reader, localized under `zh-CN` and/or `en`, with `background`, `problem`, `approach`, `key_findings`, `why_it_matters`, `limitations`, and optional `concepts`.
3. Optional `featured_figure`: at most one representative visual with exact source attribution, rights/usage status, localized caption and alt text, reader note, selection reason, and a safe local or explicitly permitted remote asset.

Do not compress the second layer into insider shorthand. Expand acronyms on first use, define paper-specific terms, identify the baseline or predecessor behind comparative phrases, and explain what a component does rather than merely naming it. Record evidence spans for every non-trivial relationship.

Evidence levels:

- `direct`: explicit statement, experiment, table, or code path
- `strong_indirect`: multiple aligned clues, no explicit sentence
- `inferred`: reasoned interpretation; must be labeled
- `unsupported`: do not place in the reviewed graph

### Phase 6 — Classify relationships

Each reviewed edge may have multiple relationship types:

- `cites_background`
- `introduces_concept`
- `formalizes`
- `extends_method`
- `modifies_architecture`
- `improves_efficiency`
- `improves_data_regime`
- `applies_method`
- `uses_benchmark`
- `introduces_benchmark`
- `uses_dataset`
- `compares_against`
- `reproduces`
- `fails_to_reproduce`
- `criticizes`
- `contradicts`
- `corroborates`
- `supersedes`
- `survey_synthesizes`
- `independent_parallel`
- `repository_of`
- `implements`
- `code_diverges_from_paper`

A raw citation edge without semantic evidence may remain in the candidate graph but must not be promoted to the reviewed graph.

### Phase 7 — Detect and adjudicate conflicts

Follow `tasks/05_conflict_analysis.md`.

Extract comparable claim tuples:

- research question
- claim
- population or domain
- assumptions
- dataset
- metric
- experimental protocol
- model scale and compute
- date/version
- conclusion

Classify apparent disagreements:

- `direct_conflict`: same or closely comparable setup, incompatible result
- `scope_conflict`: different domains or assumptions
- `measurement_conflict`: different metrics or evaluation protocols
- `version_conflict`: later code/data/model version changes the result
- `interpretation_conflict`: same observations, different explanation
- `replication_failure`
- `criticism_without_empirical_conflict`
- `resolved_or_reconciled`

Do not call two papers contradictory merely because one improves a metric or uses a different dataset.

For every conflict, write:

- the exact disputed question
- each side's claim
- comparability analysis
- strongest evidence for each side
- likely reason for divergence
- current status: unresolved, conditional, or largely resolved

### Phase 8 — Verify benchmark adoption

Follow `tasks/06_benchmark_and_repo.md`.

A paper “uses a benchmark” only when at least one is confirmed:

- benchmark appears in experimental setup
- benchmark results appear in a table or figure
- dataset/evaluator is loaded in code
- official benchmark scripts are invoked
- reported metrics are directly comparable to the benchmark protocol

Classify usage:

- `official_protocol`
- `modified_protocol`
- `partial_subset`
- `inspired_only`
- `mentions_only`
- `unclear`

Record benchmark version, split, metric, evaluator, and deviations.

### Phase 9 — Analyze the repository

For repository inputs or when code is important:

1. Identify the paper link from README, `CITATION.cff`, metadata, docs, badges, or title-author matching.
2. Pin a commit SHA.
3. Map paper components to code modules.
4. Identify training, inference, and evaluation entry points.
5. Trace dataset and benchmark loading.
6. Inspect default configs and released checkpoints.
7. Compare equations/pseudocode to implementation.
8. Check whether paper results are reproducible from documented commands.
9. Review releases, major commits, and issues for behavior changes or known failures.
10. Record implementation gaps, undocumented tricks, and post-paper improvements.

Code claims require file paths and line ranges or commit references.

### Phase 10 — Identify the main lineage and frontier

The main lineage is not necessarily the highest-citation path. Select edges that best explain conceptual inheritance and improvement.

Mark:

- `main_path: true` for the primary lineage
- `branch_role`: origin, bridge, variant, application, evaluation, criticism, replication, frontier
- `latest_frontier: true` for recent papers that materially move the focal question

For broad fields, produce several named main paths rather than one misleading chain.

### Phase 11 — Synthesize the report

Use `templates/research_report.md`.

The report must distinguish:

- retrieved facts
- paper authors' claims
- the analyst's synthesis
- uncertainty or missing evidence

For each central paper, provide:

- title, authors, date, venue/status
- identifiers and links
- a reader-oriented explanation that first establishes background and the problem, then explains the core idea, findings, significance, and limitations
- definitions for paper-specific or non-obvious concepts needed to understand that explanation
- a separate compact focus-relevant summary
- contribution to the lineage
- what it changes relative to named predecessors
- limitations and disputes
- repository/data links when available

### Phase 12 — Render and audit

Follow `tasks/07_render_and_audit.md`.

The interactive page must support:

- node click: metadata, an optional source-attributed featured figure, a structured reader-oriented paper explanation, compact focal-relation summary, role, links, evidence, code, publication state, conference/journal, and version family
- paper nodes with a justified `top` venue tier: a visually distinct top-venue badge with its basis visible
- edge click: relationship types, explanation, evidence, confidence
- conflict highlighting
- main-path highlighting
- search and filters by year, cluster, edge type, and relevance
- distinction between seed, origin, branch, benchmark, conflict, repository, and frontier nodes

Run validation and report:

- source coverage
- candidate count
- analyzed count
- included/excluded count
- unresolved identities
- abstract-only analyses
- missing full text
- conflicts with weak comparability
- stale repository or unpinned code


### Phase 13 — Expand from an existing node and merge incrementally

Follow `tasks/08_expand_from_node.md` when the user selects a node in an existing graph or supplies `operation: expand`.

#### 13.1 Load the prior research state

Read, at minimum:

- the current `graph.json`
- `run_manifest.json`
- the selected node and all incident reviewed edges
- relevant paper and evidence records referenced by that node
- prior expansion history, if present

The selected node becomes a **local seed**, not a replacement for the graph's original seed. Preserve its existing role while adding `expansion_seed_for` metadata.

#### 13.2 Define a local expansion frame

Record:

- `start_node_id`
- why this node was selected
- expansion focus
- direction: `backward`, `forward`, `both`, `related`, `conflicts`, `benchmark_use`, or `repository`
- local maximum depth and budgets
- whether the global main lineage may be revised
- requested output language

Default behavior is `both` with a smaller branch budget than a fresh standard run. Do not repeat searches already present in the candidate ledger unless refreshing the search cutoff or resolving a known gap.

#### 13.3 Retrieve and analyze the local branch

Use the normal retrieval, normalization, ranking, reading, relationship, conflict, benchmark, and repository phases, but rank candidates by both:

1. relevance to the selected node and local expansion focus; and
2. value added to the existing graph.

Prefer papers that create a new lineage, connect the node to an existing cluster, alter an existing relationship, reveal a conflict, or update the latest frontier. Treat candidates already present in the graph as updates rather than new nodes.

#### 13.4 Produce a graph patch

Write `graph_patch.json` rather than directly overwriting `graph.json`. The patch contains:

- expansion metadata and base revision
- `upsert_nodes`
- `upsert_edges`
- conflict and cluster upserts
- evidence IDs supporting every changed semantic assertion
- optional `main_path_reassessment`
- no destructive deletion by default

Every new or changed record must carry `added_in_revision` or `updated_in_revision` after an expansion merge. The initial revision-1 build is the baseline and should normally omit these fields; even if legacy data contains revision-1 stamps, the renderer must not treat the whole baseline as the “latest increment”. Stable canonical node IDs and edge IDs must be reused.

#### 13.5 Merge safely

Run:

```bash
python scripts/merge_expansion.py BASE_GRAPH graph_patch.json -o UPDATED_GRAPH --delta delta_report.json
```

The merge must:

- verify that the base graph ID and revision match the patch
- verify that `start_node_id` exists
- archive the previous graph revision
- upsert without dropping unrelated fields or evidence
- reject dangling edges and duplicate IDs
- append an expansion-history record
- update coverage statistics and search cutoff
- mark the selected node's latest expansion status
- emit counts of added and updated nodes, edges, conflicts, and clusters

If a new branch changes the interpretation of an existing edge or main path, retain the prior assertion in revision history and explain the revision in `delta_report.md`.

#### 13.6 Re-render the full graph

The new page must show the complete updated graph, not only the branch. It must also support:

- “continue research from this node” on node detail panels
- exporting an `expansion_request.json` for the selected node
- highlighting nodes and edges added or updated by the latest genuine expansion revision
- filtering to the latest increment
- displaying graph revision and expansion provenance

The static HTML may export the request but does not itself perform network research. The host agent executes the request and merges the resulting patch.

**Initial-build rule:** when `revision == 1` and there is no expansion history/latest-increment record, omit the “latest increment” filter and legend entry, do not apply incremental outlines/dashes, and do not show added/updated revision metadata in node or edge details.

## Output language and localization

- `output_language: zh-CN` means all analyst-authored prose and UI text are Simplified Chinese. Preserve original paper titles, names, venue names, identifiers, equations, code symbols, and short source quotations; optionally add a Chinese title translation in a separate field.
- `output_language: en` means English analyst-authored output.
- `output_language: bilingual` stores localized text in language maps such as `summaries.zh-CN` and `summaries.en`; the page allows switching or displays Chinese first with English below.
- Never machine-translate identifiers, repository paths, class/function names, benchmark names, metric names, or exact paper titles in a way that prevents lookup.
- On first mention in Chinese prose, use `中文译名（Original Term）` when a stable translation is useful; thereafter use one consistent term. Maintain a run-level terminology glossary for ambiguous terms.
- Translate source claims faithfully and mark analyst inference separately. When a wording dispute matters, preserve the original wording alongside the Chinese explanation.
- Node `title` remains the canonical/original title. Use `titles.zh-CN`, `summaries.zh-CN`, `roles.zh-CN`, and `explanations.zh-CN` for localized display when available. Keep legacy scalar fields for compatibility.
- `reader_summary` is not a translation of the abstract. It is an analyst-written explanation for an informed non-reader. Chinese prose should prefer clear subject-verb sentences, introduce one new concept at a time, expand unexplained abbreviations, and avoid chains of untranslated noun phrases when a short explanation is clearer.
- Preserve technical precision while improving accessibility: analogies may support the formal explanation, but must not replace the actual mechanism, assumptions, or evaluation conditions.
- Localize figure captions, alt text, reader notes, and selection reasons, but preserve the original figure number and source citation. A figure must remain understandable to an unread-paper audience and accessible without relying on color alone.

## Quality scoring

Do not reduce paper quality to venue prestige. Use a multidimensional profile:

- relevance to the focal question
- methodological rigor
- evidence strength
- evaluation breadth
- reproducibility
- code/data availability
- publication and review status
- venue tier only as a sourced contextual signal, never as a substitute for methodological assessment
- citation influence, age-normalized
- independent replications
- known corrections or retractions

Report scores as heuristic and explain the basis.

## Completeness language

Allowed:

- “all citing works returned by the queried sources as of DATE”
- “a high-coverage citation graph cross-checked across SOURCES”
- “the reviewed subset selected from N candidates”

Avoid:

- “all papers that exist”
- “complete literature”
- “definitive origin” when several origin definitions are plausible

## Failure handling

- If a paper identity is ambiguous, keep multiple candidates and explain the ambiguity.
- If full text is unavailable, use abstract-only analysis and downgrade confidence.
- If sources disagree on citation counts, retain source-specific counts and do not average them silently.
- If the graph becomes too large, switch to cluster-representative mode rather than truncating without explanation.
- If a repository has no reliable paper link, report the strongest candidates and matching evidence.
- If no substantive conflict is found, say so; do not manufacture controversy.

## Final response checklist

Before delivering:

- canonical seed resolved
- focus frame stated
- candidate graph retained
- reviewed graph evidence-backed
- main lineage marked
- conflicts adjudicated
- benchmark usage verified rather than assumed
- repository pinned and mapped when applicable
- latest search date stated
- coverage limitations stated
- links and identifiers included
- `graph.json` validates
- `index.html` renders
- requested output language is applied consistently to report, graph prose, conflict analysis, and UI
- graph revision and expansion history are valid
- node-centered expansion, when requested, produced a patch and delta rather than silently replacing prior work
- paper nodes expose preprint/publication status and venue; any top-venue badge has a recorded basis and as-of date
- any displayed paper figure is selectively chosen, source-attributed, rights-documented, accessible, and either safely embedded or explicitly allowed as a remote asset
- revision-1 baseline graphs show no “latest increment” markings
- every analyzed paper node contains a `reader_summary` suitable for a domain-relevant reader who has not read the paper
- reader summaries explain necessary background and concepts before using them, name comparison baselines, and make results and limitations understandable without opening the PDF


## Featured figure policy

A paper node may contain one `featured_figure`, but absence is normal. Add one only when it improves comprehension or materially improves navigation for a central paper. Prefer method overviews, architectures, pipelines, conceptual diagrams, and directly explanatory qualitative results. Avoid decorative images, generic examples, dense tables, tiny multi-panel plots, or figures selected only because they look attractive.

For every selected figure:

- identify the exact paper version and figure number/page;
- record a source citation and URL;
- record license or usage basis and `rights_status`;
- write localized caption, alt text, and a short reader note;
- explain the selection reason;
- save a compressed web-friendly local asset under `assets/figures/<node-id>/` where permitted;
- mark any analyst-created reconstruction explicitly and never pass it off as the original paper figure.

The renderer embeds safe local assets into the standalone page up to the configured byte limit. Remote image loading is off by default. If the image is unavailable or cannot be displayed responsibly, retain the textual attribution and omit the visual rather than breaking the page.
