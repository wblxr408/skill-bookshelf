# Retrieve Candidate Graph

## Initial expansion

For every seed retrieve:

- references cited by the seed
- works citing the seed
- related works
- surveys/reviews containing the seed or focal concept
- papers using distinctive benchmark, dataset, method, or repository names
- newest citing papers by publication date

## Adaptive frontier

Assign each candidate a provisional score. Expand when score >= configured threshold or when the candidate is a bridge, conflict, benchmark, replication, or frontier candidate.

Maintain:

- `frontier_queue`
- `visited_ids`
- `identity_aliases`
- `candidate_ledger`
- per-source retrieval timestamps

## Candidate ledger fields

- canonical_id
- discovered_from
- discovery_edge
- source_database
- title/authors/year
- provisional relevance
- depth
- inclusion status
- exclusion reason
- identity confidence
- full-text availability

## Exclusion reasons

Use explicit values:

- incidental citation
- unrelated application domain
- duplicate/version alias
- insufficient metadata
- outside date range
- no substantive connection
- low-value derivative
- budget cutoff
- non-scholarly item

Never delete excluded records from the ledger.
