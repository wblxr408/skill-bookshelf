# Academic Research Graph Skill

A reusable Skill for evidence-backed citation-lineage research, controversy analysis, benchmark adoption checks, repository-to-paper resolution, code/paper comparison, **incremental research from any existing graph node**, and interactive literature graph generation.

Version 0.2.4 adds native DeepSeek Harness bundle packaging while preserving the existing ChatGPT Skill workflow. The selective, source-attributed paper figures introduced in 0.2.3 remain optional and accessible, and the earlier reader-oriented summaries, publication/venue display, and baseline-safe increment highlighting remain intact.

## What it produces

- a focused research report in the requested language
- a broad candidate citation graph plus a reviewed semantic graph
- claim- and evidence-level paper relationships
- conflict analysis that distinguishes real contradiction from scope or evaluation differences
- verified benchmark adoption
- paper/repository implementation mapping
- a standalone interactive HTML network view with reader-oriented paper guides, selective source-attributed featured figures, preprint/publication venue details, and optional top-venue badges
- node-centered expansion requests, graph patches, merge history, and delta reports

## Typical prompts

- “分析 arXiv:2406.05720，追踪来源和有意义的后续工作，并确认哪些论文真正使用了它的 benchmark。用中文输出。”
- “从当前图中的 `paper:deit` 节点继续向后调研数据效率分支，并补回原图。”
- “Map the origin, variants, criticism, and current frontier of Vision Transformer.”
- “Start from this GitHub repository, identify its paper, compare code with the method, and map follow-up work.”

## Directory layout

- `SKILL.md`: main agent instructions
- `tasks/`: phase-specific procedures, including node expansion
- `prompts/`: evidence extraction and localization templates
- `schemas/`: build request, expansion request, graph, and graph-patch schemas
- `scripts/`: initialization, expansion initialization, patch merge, ranking, validation, and HTML rendering
- `templates/`: report template
- `examples/`: sample build request, expansion request, patch, baseline/expanded graphs, and baseline/expanded pages
- `config/venue_tiers.example.yaml`: non-authoritative example of a sourced venue-tier policy

## Build a new graph

```bash
python scripts/init_run.py --name vit-lineage --out runs --focus "ViT 的演化" --language zh-CN
# Populate graph.json and evidence files through the research workflow.
python scripts/validate_graph.py runs/vit-lineage/graph.json
python scripts/render_site.py runs/vit-lineage/graph.json -o runs/vit-lineage/index.html
```

## Continue from an existing node

```bash
python scripts/init_expansion.py runs/vit-lineage/graph.json paper:deit \
  --out runs/vit-lineage/expansions/deit-data-efficiency \
  --focus "继续追踪数据高效视觉 Transformer 的后续方法与争议" \
  --direction forward --language zh-CN

# The research agent fills graph_patch.json and evidence files.
python scripts/merge_expansion.py \
  runs/vit-lineage/graph.json \
  runs/vit-lineage/expansions/deit-data-efficiency/graph_patch.json \
  -o runs/vit-lineage/graph.json \
  --delta runs/vit-lineage/expansions/deit-data-efficiency/delta_report.json

python scripts/validate_graph.py runs/vit-lineage/graph.json
python scripts/render_site.py runs/vit-lineage/graph.json -o runs/vit-lineage/index.html
```

Paper detail panels are written for field-relevant readers who have not read the paper: they establish background, define necessary concepts, explain the problem and core idea, contextualize findings, and state limitations. They also show whether a work is preprint-only or formally published, its conference/journal, version family, and a special top-venue badge only when a tier basis is recorded. For selected high-value papers, the panel may show one representative figure—typically a method overview, architecture, pipeline, conceptual diagram, or especially informative qualitative result—with exact source attribution, accessible alt text, and a short explanation of why the figure helps understand the paper. Figures are not mandatory for every paper.

The HTML node detail panel can export the same expansion request. The static page does not itself access the network; the host agent executes the request and merges the evidence-reviewed patch.

A revision-1 build is treated as the baseline: it does not show “latest increment” filters, outlines, or added/updated badges. Those controls appear only after a real node expansion creates a later revision.

## Language behavior

- `zh-CN`: Chinese analyst-authored report, summaries, edge explanations, conflict analysis, and UI.
- `en`: English output.
- `bilingual`: localized maps with deterministic bilingual display.
- Canonical paper titles, identifiers, venue names, benchmark names, code paths, and symbols remain unchanged for lookup.

## Design boundary

The included scripts do not attempt to hide API-specific retrieval behind a brittle universal crawler. Retrieval adapters should be implemented for the tools available in the host environment. The Skill defines their required normalized output in `adapters/README.md`.
