---
name: browser
description: Operate browser UI and verify web interfaces using proven cua_repl and Playwright Edge workflows, with CDP as a diagnosed fallback.
metadata:
  version: "fusion-2026-10-05"
---

# Browser — evidence-based browser automation

Choose the browser explicitly requested by the user, including an @mentioned tab. Otherwise use the route that fits the task and available tools. Avoid switching adapters midway through a successful session.

| Need | Preferred route |
|---|---|
| Existing user tab, authenticated navigation, in-app preview, interactive page work | [cua_repl](references/cua.md) when exposed |
| Repeatable local frontend acceptance, several viewports, isolated test browser, console/network assertions | [Playwright Edge](references/playwright-edge.md) |
| Existing remote-debugging session or a demonstrated gap in the above | [CDP](references/cdp.md), using retained scripts |
| Native Windows application outside a browser | The existing `computer-use` plugin when exposed and permitted; it retains its distinct Windows runtime |

Successful local history supports cua_repl for WaterGuard browser work and Playwright Edge for ten independent apps at 320, 390, and 1440 pixels. It does not establish a universal reliability ranking or prove CDP failed. See [evidence](references/evidence.md).

Initialize the currently exposed UI runtime with its documented entry point. Observe the page before interacting, refresh stale targets after navigation/state changes, and verify the meaningful result. Use a hidden/isolated browser for automated checks when practical. Keep credentials in the selected browser session. Download waits require adapter-specific evidence; a timed-out wait does not prove a download succeeded. For a diagnosed failure, choose a supported equivalent and carry over explicit target/state, rather than blindly repeating clicks.

Retained [CDP module](modules/cdp/PLAYBOOK.md) and [Playwright module](modules/playwright/PLAYBOOK.md) supply scripts, trace, tabs, screenshots, and detailed operations. PowerShell should invoke available executables directly; Bash wrappers are optional adapters. `/browser` and `$playwright` intents resolve here.
