# Operation discovery and review

Use MCP `photon` for structured requests and `photon_preview` for native images. For CLI workflows the installed launcher is `~\.photon\bin\photon.exe`; invoke that absolute path in your shell rather than assuming PATH is configured. Configuration and tool permission errors are blockers: never modify harness permissions to bypass them.

`capabilities` accepts a short topic query and returns a ranked page. Follow `nextOffset` with `offset` when more matches are needed; `total` reports the full count. `describe` takes `{ "operation": "shape.create" }` and returns the exact schema. Do not infer field names from another image editor.

1. Choose an existing document explicitly, or create one in the requested live/headless mode.
2. Inspect its layer IDs, revision, dimensions, fonts, and relevant properties.
3. Use document pixels for anchors, handles, bounds, and placement. Opacity and scale use 0–1 fractions.
4. Read the operation schema, then execute with `documentId`, `sessionId`, and the inspected `expectedRevision`.
5. Review the returned revision and inspect a native preview. Use isolated layers or crops to check details.
6. Save as a separate operation. Verify reopening and report any limitations, without calling an unsuccessful operation complete.

A revision conflict means another edit happened. Inspect the changed target before submitting a new request. Never replace the expected revision blindly. A transaction is one undo entry; external effects such as saving, printing, preferences, and clipboard operations cannot be rolled back with document edits. `OUTCOME_UNKNOWN` requires inspection/recovery before deliberate reapplication.

Text needs an explicit font. Discover installed fonts with `fonts.list`, then check every required script with `fonts.check`. Inspection reports missing fonts and characters. Keep generated assets and previews under a shared artifact directory; in Flatpak use `~/.photon/artifacts`, never assume host `/tmp` is shared.
