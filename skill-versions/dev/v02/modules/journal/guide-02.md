## Core Rules (Mandatory)

- **10-Point Specify Gate**: Spec score `0-10`; must be `>=9` to enter Plan.
- **2-Action Save**: Append an entry to `.sparv/journal.md` every 2 tool calls.
- **3-Failure Protocol**: Stop and escalate to user after 3 consecutive failures.
- **EHRB**: Require explicit user confirmation when high-risk detected (production/sensitive data/destructive/billing API/security-critical).
- **Fixed Phase Names**: `specify|plan|act|review|vault` (stored in `.sparv/state.yaml:current_phase`).
