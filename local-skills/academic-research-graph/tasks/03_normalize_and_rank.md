# Normalize and Rank

## Identity resolution

Identifier priority:

1. DOI
2. arXiv ID plus version
3. Semantic Scholar Corpus ID
4. OpenAlex ID
5. PMID/PMCID
6. high-confidence normalized title + authors + year

Create a version family when preprint, conference, journal, correction, or extended versions belong together.

## Date handling

Keep separate fields for:

- first public date
- preprint version dates
- conference date
- journal publication date
- correction/retraction date

Use first public date for historical priority and final publication date for venue/status reporting.

## Ranking

Score each candidate 0-1 for:

- focus relevance
- lineage importance
- bridge centrality
- methodological novelty
- conflict likelihood
- benchmark/repository evidence
- recency/frontier value
- evidence quality

Use the baseline script, then document manual overrides.

## Publication and venue normalization

For every paper node, populate structured `publication` metadata:

- status: preprint-only, under review, accepted, in press, published, withdrawn, retracted, or unknown
- document type and peer-review state
- primary conference/journal/workshop
- preprint, conference, journal, and extended-version records
- venue tier only when a field-specific basis and as-of date are recorded

Do not infer “top venue” from citation count or model familiarity. Use an explicit user/institution policy or a named ranking source, and retain the basis in the graph.
