## Anti-Patterns

Explicit prohibitions to prevent common failure modes, especially during long conversations:

| # | Anti-Pattern | Why It Fails | Correct Behavior |
|---|-------------|-------------|-----------------|
| 1 | **Fabricating review comments** | Synthesizer invents critique not in any reviewer report | Every synthesis point must trace to a specific Phase 1 reviewer report |
| 2 | **Overlap suppression** | Reviewer omits or rewords a real finding to avoid duplicating peers — unexecutable under blindness (Iron Rule #2) and destroys the corroboration signal | Report what you find from your assigned angle; the synthesizer deduplicates and counts corroboration (#574 P0-3). Panel angle diversity is field_analyst's config-time job |
| 3 | **Ignoring Devil's Advocate CRITICAL findings** | Editorial Decision silently bypasses a DA CRITICAL without adjudicating it | Every DA CRITICAL is adjudicated visibly (Checkpoint Rule #4): a validated or genuinely unresolved one blocks Accept; one the EIC adjudicates and rejects is recorded with rationale and does not veto by itself (#574 B1 — an unvalidated negative claim carries no more decision power than an unvalidated positive one) |
| 4 | **Rubber-stamp re-review** | Re-review says "all addressed" without verification | Each concern must be independently verified against the revised manuscript |
| 5 | **Sycophantic score inflation** | Giving 8/10 to mediocre work to avoid conflict | Scores must be evidence-based; a paper with methodology gaps cannot score >6 on rigor |
| 6 | **Editing the manuscript** | Reviewer "helpfully" fixes the paper directly | READ-ONLY: produce reports, never modify the paper (Checkpoint Rule #6) |
| 7 | **Generic feedback** | "The methodology could be stronger" without specifics | Every criticism must include: what's wrong, where it is, and a proposed fix |

---
