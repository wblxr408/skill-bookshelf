---
name: intent-review
description: Review proposed AI work at the level of user purpose, tradeoffs, and system boundaries. Use for design reviews, change reviews, and before approving substantial agent output.
---

# Intent review

Begin with the decision the user is trying to make, not a line-by-line inspection. Check:

- Does this solve the actual user problem?
- Is the chosen scope proportionate to the value?
- Are the important boundaries and non-negotiable constraints preserved?
- What meaningful tradeoff did the proposal choose, and is it acceptable?
- What evidence would justify proceeding?

Rely on automated checks for formatting, syntax, and routine correctness when those are available. Surface only issues that change the decision, behavior, risk, cost, or future maintainability. End with a clear recommendation, required changes, or a specific open question.
