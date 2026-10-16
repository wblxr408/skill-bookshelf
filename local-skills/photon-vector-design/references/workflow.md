# Vector and logo review

Use a small number of anchors with intentional incoming/outgoing handles. Close silhouette subpaths explicitly and select the fill rule deliberately. Request `shape.create` and `shape.path.set` schemas, then inspect the actual operation IDs available for Boolean composition. Verify holes and overlaps on contrasting backgrounds. Render at the intended small usage size as well as a larger crop; check cusps, tangent continuity, optical balance, and bounding boxes. Keep path and type layers editable. A rasterized approximation is not evidence of a successful vector task.

`pixels.warpMesh` is a destructive raster operation with explicit split/move/remove steps; preserve an editable vector or smart-object source when using it. For Bézier designs, prefer direct vector geometry and Boolean operations so handles stay editable.

Use `text.format` for live character and paragraph changes and `library.textStyle.*` for reusable styles. Use `effect.describe` before adding typed shadows, strokes, bevels or overlays with `layer.effect.set`; preserve existing effects when revising one component. Save/reopen checks must compare path handles, bounds and formatting, not only layer names and previews.
