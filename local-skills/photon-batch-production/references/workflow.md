# Bounded batch programs

An atomic `batch` accepts `steps` containing operation/params and optional `as` result names. A later parameter can use `{"$ref":"created.layerId"}`. Repeat blocks use `repeat` and `steps`; conditional blocks use `if`, `then`, and `else`. At most 1000 operations execute in one transaction. Failure rolls back the whole document transaction.

For longer workflows `script.run` accepts a declarative photon-script program: `let`, `edit`, `transaction`, `ifValue`, bounded `repeat`, and the existing script operations. No JavaScript is evaluated. File output stays outside transactions. Keep request IDs for retries, record each result and resulting revision, and use jobs.status/jobs.cancel for long requests. Review representative outputs visually and verify every requested variant's dimensions, naming, content, and save/reopen behavior.

Use `export.plan` and `export.asset` with kind `layers`, `artboards`, `comps`, or `slices`. Compare actual outputs with each composition's intended geometry, not just file existence. Transfer resource data with portable preset packs before applying pattern IDs in another document. Keep exports and other external effects outside atomic editing transactions.

`production.export` builds bounded variants from a revision-checked source copy; it leaves the original unchanged. `production.recipe.write` and `production.recipe.run` store and execute declarative production recipes. These are Photon recipes, not standalone OS executables. Discover their supported steps and output fields. If a production operation fails after writing files, inspect its `written` and `failures` details; external outputs are not rolled back.

`assets.plan` previews filename-driven layer outputs and `assets.generate` writes them. Review naming, scale and directory before execution. `document.package` creates a portable project copy embedding the retained bytes of linked sources; refresh links first only if the task calls for their current on-disk contents. `actions.library.*` exposes the shared Actions panel; `actions.record.start/stop` records committed operations from one explicit document. Imported legacy action steps may be unsupported: inspect errors rather than counting a partial replay as success.

`export.plan` includes skipped entries with reasons such as `hidden`; they are diagnostics, not scheduled files. Filter out entries with `skipped`. `options.name` overrides the batch name prefix and `options.suffix` is appended to each basename before the extension.
