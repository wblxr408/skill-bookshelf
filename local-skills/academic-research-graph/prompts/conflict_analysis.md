# Conflict Analysis Prompt

Compare two claims using the same focal question.

Extract for each side:

- exact claim
- scope/domain
- assumptions
- dataset/split
- metric
- protocol
- model/compute scale
- evidence

Then classify:

- direct conflict
- scope conflict
- measurement conflict
- version conflict
- interpretation conflict
- replication failure
- criticism without empirical conflict
- reconciled

Explain whether the disagreement is genuine, conditional, or only apparent. Do not force a conflict label.

Localization:

- Write the adjudication in `output_language`.
- Preserve the original wording of disputed claims when translation could alter scope, negation, or confidence.
- In Chinese output, distinguish clearly between “作者声称”, “证据显示”, and “分析者推断”.
