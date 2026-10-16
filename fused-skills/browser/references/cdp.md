# cdp

Use retained root/module CDP .cjs/.js helpers only when a remote-debugging browser is the intended session or the preferred adapters have a diagnosed gap. Edge is the existing Windows launcher preference; localhost:9222 must refer to the actual intended browser. Preserve the chosen authentication profile, verify the tab and page before eval/interactions, and use the script's actual file extension/CLI contract.

Check existing package.json and dependencies before npm install; do not install twice or launch a fresh browser when the target is already running. Treat start/profile/navigation/eval/pick/screenshot helpers as retained capabilities, not proof that CDP is the user's most successful general route. Never silently reuse the wrong user's tab/profile.

For the retained helpers use `node <skill-root>/scripts/run-cdp.cjs <start|nav|eval|pick|screenshot|viewport> [helper arguments]`. The launcher resolves the existing `ws` dependency from installed browser runtimes, passes arguments unchanged, and keeps the current working directory. `node <skill-root>/scripts/run-cdp.cjs --check` checks dependencies without launching or interacting with a browser. Read the selected helper's CLI before invoking it; do not start a browser merely to inspect dependencies.
