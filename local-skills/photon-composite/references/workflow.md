# Compositing checks

Inspect source dimensions and alpha before placement. Use `image.place` with an explicit document-space rectangle and smartObject when source preservation matters. Align perspective and lighting, then use editable masks, clipping, blend modes, shadows, and grading. Inspect isolated layer and mask previews at edge detail. Confirm masks remain editable, the source asset is retained, and foreground elements did not move during background edits. A group preview includes its children; compare the full composition after every substantial transform.

For `core.layers.warpSmartObjects` perspective, `corners` are OFFSETS from existing corners, clockwise from top left—not absolute destination coordinates. Inspect geometry and keep preview crops explicit when artwork extends outside the canvas.

Use `layer.smartFilterMask.create`, `layer.smartFilterMask.update`, and `layer.smartFilterMask.delete` with the stack or explicit filter target described by each schema. Render a smart-filter mask with `smartFilterMask:true`, `layerId`, and optional `filterId`; paint it with `tool.gesture` target `smartFilterMask`. Mask edits must leave source pixels intact.

Use `document.package` when delivering a portable copy with embedded linked assets. It preserves currently retained source bytes; use explicit link refresh only when requested. Prefer typed `layer.effect.set` updates for shadows and overlays. After perspective, warp or liquify work, compare both visible pixels and editable bounds after fresh reopening.
