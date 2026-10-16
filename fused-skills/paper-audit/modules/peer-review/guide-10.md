## Calibration Mode (v3.2)

Opt-in mode that measures this reviewer's FNR / FPR / balanced accuracy against a user-supplied gold set (5-20 papers with known outcomes). Runs `full` 5x per paper with fresh context, cross-model default-on. Produces a Calibration Report attached as a confidence disclosure to subsequent reviews in the session.

> See `references/calibration_mode_protocol.md` for full spec: intake rules, ensembling methodology, output format, and failure cases this mode does not fix.

---
