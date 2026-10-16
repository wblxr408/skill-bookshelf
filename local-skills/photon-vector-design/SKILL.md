---
name: photon-vector-design
description: Design editable logos, icons, paths and typography in Photon using Bézier geometry and vector operations.
---

Use shape.create or tool.gesture for pen-tool geometry. Each path point has an anchor plus incoming/outgoing Bézier handles. Closed subpaths and fill rules determine holes. Prefer a small number of purposeful points. Inspect the silhouette at both small and large sizes, then refine handles. Use shape Boolean operations for cutouts and text.create for live lettering.

The installed CLI launcher is `~\.photon\bin\photon.exe`. Invoke that absolute path with shell-appropriate quoting (PowerShell uses `& 'PATH'`; POSIX shells use `'PATH'`). Do not depend on `photon` being on PATH. Discover operations with the launcher followed by `capabilities --params '{"query":"TOPIC"}'` and read exact parameters with `describe --params '{"operation":"OPERATION"}'`. The MCP `photon` tool exposes the same operations. Do not guess operation names or parameter formats.

Use `session.list` to identify the requested open document, including unsaved work. Otherwise use `session.open` with an explicit path or `session.create` with width and height. Choose live or headless mode to match the request. Keep the returned session/document IDs. Inspect before editing and pass the observed `expectedRevision` on every mutation. A conflict means inspect again; do not overwrite or silently retry against a newer revision.

For the CLI, `execute OPERATION --session ID --document ID --revision N --params JSON` performs an edit. Use `--input FILE` for complex geometry or batches. `batch` takes `steps`, optionally with `as` names; a later parameter can reference an earlier result using `{"$ref":"name.layerId"}`. A batch is one undoable document transaction. Save/export is a separate operation.

Use `render` or MCP `photon_preview` to inspect the result. Preview metadata maps image pixels back to document coordinates. Request isolated layers or regions when more detail is needed. Keep vectors, type, masks, effects and smart objects editable where the task benefits. Save to the requested destination using `document.save`; preserve the original when asked for a variant. Report existing unsupported capabilities clearly.

Read [protocol and review guidance](references/protocol.md) for discovery, units, conflicts, fonts, and save checks. Read [workflow details](references/workflow.md) when planning this workflow.
