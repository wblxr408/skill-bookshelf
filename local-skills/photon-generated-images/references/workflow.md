# External image generation

Photon does not generate images. Use your agent's available generation tool. Export `generation.context` for the exact inspected revision, including reference pixels and a selection/mask when needed. Retain sourceRect, dimensions, scale, and target revision alongside the generation prompt. Image pixel `(u,v)` maps to document `(sourceRect.x + u * scale.x, sourceRect.y + v * scale.y)`.

After generation, inspect the target again. If the revision or target changed, report the conflict and deliberately decide whether the result still fits; never silently apply a stale generation result. Import the returned file with `image.place`, an explicit placement rectangle, and optional `maskFromSelection`. Keep transparency and source bytes in a smart object when appropriate. For outpainting, expand the canvas with a schema-discovered document operation and track its offsets before placing generated pixels. Review seams, mask edges, unwanted backgrounds, and retained source editability. Save both the generated asset and final Photon project.

Creating a layer mask over an existing mask requires `replace:true`; do not replace a client's mask implicitly. Preserve imported originals in smart objects and use `smartObject.export` to retrieve retained bytes. When delivering generated-image campaigns, `production.export` and `assets.plan/generate` can produce variants; inspect partial-output details if any write fails.


## Outpainting quality

A relevant generated scene is not enough: straight tonal or texture discontinuities
at the old canvas edge mean the workflow is unfinished. Include an overlap band
inside the old canvas in the generation context and ask the generator to continue
lighting, texture scale and recognizable forms. Keep the original source layer and
its transform intact. Place the generated asset on a separate layer with an editable
mask; use a gradual transition in the overlap band, then correct local color/contrast
with editable adjustments when needed. If the user requires every original visible
pixel unchanged, confine the blend to the new canvas and preserve the boundary colors.

Inspect native-resolution crops across each seam as well as a composition overview.
Revise the mask/grade or regenerate the problematic region when the first attempt
has a visible join. Compare the revised crops, preserving prior variants until the
replacement is accepted. If a bounded number of iterations cannot achieve a clean
join, report the visual failure explicitly; do not label a structurally valid import
as a finished outpaint.
