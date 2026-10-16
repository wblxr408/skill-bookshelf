# Benchmark and Repository Analysis

## Benchmark verification

Confirm benchmark use through at least one direct artifact:

- methods/experimental section
- result table or figure
- evaluator configuration
- dataset loader
- command line or script
- official submission record

Record:

- benchmark version
- subset/split
- metric and evaluator
- protocol deviations
- whether comparable to official results
- whether code evidence agrees with paper text

## Repository analysis

Pin a commit and capture:

- repository URL
- commit SHA
- default branch
- license
- release/tag closest to paper publication
- install and reproduction commands
- entry points
- model modules
- data pipeline
- training loop
- evaluation loop
- configs
- checkpoints
- tests
- issues describing known failures

## Paper-to-code map

For every major paper component, map:

- paper section/equation/algorithm
- implementation file/function/class
- implementation status: exact, approximate, modified, absent, unclear
- evidence

Flag undocumented implementation details and post-paper code changes.
