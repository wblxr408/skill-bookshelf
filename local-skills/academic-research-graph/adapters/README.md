# Retrieval Adapter Contract

The host environment may expose APIs, web tools, connectors, or local corpora differently. Each adapter should normalize its output rather than leaking source-specific schemas into the analysis layer.

## Paper adapter output

```json
{
  "source": "openalex",
  "source_id": "...",
  "title": "...",
  "authors": ["..."],
  "abstract": "...",
  "dates": {},
  "venue": "...",
  "identifiers": {},
  "urls": {},
  "references": ["source-specific IDs"],
  "citations": ["source-specific IDs"],
  "citation_count": 0,
  "topics": [],
  "open_access": {},
  "retrieved_at": "ISO-8601"
}
```

## Repository adapter output

```json
{
  "url": "...",
  "owner": "...",
  "name": "...",
  "default_branch": "...",
  "commit_sha": "...",
  "metadata": {},
  "files": [],
  "releases": [],
  "issues": [],
  "paper_candidates": [],
  "retrieved_at": "ISO-8601"
}
```

## Required behavior

- paginate until configured limits
- record retrieval errors and rate limits
- retain source-specific counts
- avoid silently dropping missing references
- cache by source ID and retrieval date
- preserve raw responses when licensing permits
