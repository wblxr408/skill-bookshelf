---
name: orch-fix-defect
description: Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, and gated commit — by delegating each phase to the matching ECC agent. Use when existing behavior is broken or wrong.
metadata:
  origin: ECC
---

> Local integration: this is a technical reference, not an independently discoverable skill. Read [the local execution contract](../../../../references/fusion-policy.md) first. Mandatory TDD applies. Do not create or run smoke/hash/file-presence/import/startup/shallow-health or other superficial checks unless the user explicitly requests the specific check, even as auxiliary diagnostics. General verification requests and source/CI examples do not authorize them. No automatic agents, scripts, hooks, model changes, installs, messages, publication, or schedules are authorized by this guide.



# orch-fix-defect

Actor · action · target: **orch · fix · defect**. Thin wrapper over the shared
engine in [`orch-pipeline`](../orch-pipeline/GUIDE.md).

## When to Use

- Something is **broken**: wrong output, an error, a crash, a regression.
- Distinguish from siblings:
  - behavior is correct but you want it different → `orch-change-feature`.
  - the capability does not exist yet → `orch-add-feature`.

## Operation settings

- **Default size floor:** small (often trivial).
- **Phase mask:** 0 → (light 2 only if root cause is non-obvious or standard+) →
  4 → 5 → 6. Research (1) is usually skipped.
- **First move (phase 4):** reproduce the bug as a **new failing** test
  (regression test), then fix until it goes green. Proving the bug exists first
  is what separates a fix from a tweak.

## How It Works

1. Run the `orch-pipeline` engine with the settings above.
2. If the root cause is unclear, scope it with `code-explorer` before the red
   test; escalate build breaks to `build-error-resolver` / `/build-fix`.
3. Stop at **Gate 1** (only if a plan was produced) and **Gate 2** (pre-commit).
4. Add `security-reviewer` if the defect sits in a security-sensitive path.

## Example

```
orch-fix-defect: poller crashes on empty NWS response
→ write failing test reproducing the crash → fix to green
→ code-review → commit  [GATE 2: confirm]   (commit: fix:)
```
