# Resolve Input

## Paper input

1. Extract any DOI, arXiv ID, PMID, OpenAlex ID, Semantic Scholar Corpus ID, title, authors, and year.
2. Query at least two scholarly sources.
3. Prefer exact identifier matches.
4. If matching by title, normalize punctuation and whitespace, then verify first author and year.
5. Link preprint and publisher versions without discarding version-specific differences.
6. Record ambiguity rather than silently choosing.

## Concept, benchmark, or claim input

1. Expand synonyms, abbreviations, previous names, and related phrases.
2. Find recent surveys or authoritative overview papers.
3. Mine their definitions and historical references.
4. Generate candidate origin papers.
5. Classify each candidate as first term, first formalization, first implementation, first demonstration, or popularization.
6. Search both backward from surveys and forward from candidate origins.

## GitHub repository input

Inspect, in order:

1. `CITATION.cff`, `codemeta.json`, Zenodo badge, DOI badge, arXiv badge
2. README paper links and BibTeX blocks
3. documentation, release notes, package metadata, and repository topics
4. PDF filenames and title strings
5. author identities and organization
6. web search using repository name plus distinctive method names

Return a ranked list if more than one paper is plausible.
