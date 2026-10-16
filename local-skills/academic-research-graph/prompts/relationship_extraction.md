# Relationship Extraction Prompt

For a pair of papers or a paper and repository, determine whether a substantive relationship exists.

Do not infer a semantic relationship merely because one cites the other.

Return:

- source_id
- target_id
- citation_direction
- relationship_types
- primary_relationship
- concise explanation centered on the focal question
- changed component
- evidence level
- evidence IDs
- confidence
- main_path candidate: yes/no

Reject the edge when evidence is insufficient.

Localization and incremental context:

- Write the explanation in `output_language`; preserve relationship type codes in English.
- When expanding an existing graph, state whether the edge is new, updates an existing edge, bridges an existing cluster, or changes the main-path interpretation.
- Reuse the existing canonical edge ID when the semantic relationship already exists.
