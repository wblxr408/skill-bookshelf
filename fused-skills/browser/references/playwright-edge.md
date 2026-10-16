# playwright edge

Use Playwright with installed Microsoft Edge (`channel=msedge`) for local frontend acceptance when available. Prefer the existing project Playwright dependency and established setup; use the retained CLI adapter if appropriate. On Windows call npx.cmd or the runtime executable directly, and use the Bash wrapper only on a compatible shell. Keep a controlled browser session separate from the user's normal profile unless the user asks otherwise.

Exercise the meaningful user path and related viewport widths in a batched run; recorded historical widths 320/390/1440 are useful defaults, not a universal checklist. Capture evidence, check relevant console/network failures, and verify layout/image loading only where material. Close an isolated verification browser when done; preserve the user's existing tabs. Use the module's trace/tab/download guidance for those explicit needs; do not write Playwright test files merely to automate a one-off browse.
