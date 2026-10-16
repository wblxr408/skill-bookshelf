# Nondestructive photo finishing

Preserve the original image in a smart object or separate source layer. Use editable adjustments and smart filters for grading. Inspect the filter schema and defaults before passing parameters; units vary by filter. Review before/after previews at the same crop and scale, including highlights, skin/product colors, shadow detail, and halos. Check layer visibility and mask coverage when a result appears blank. Retouch with explicit source and target layers; verify protected pixels outside the intended region.

Use `layer.adjustment.new` for editable grading and `document.adjustment` only for an intended pixel correction. Their schemas specify the supported fields for each adjustment kind. Curves use `input`/`output` coordinates in 0–255 units; do not substitute vector point fields. Some spatial adjustments cannot exist as adjustment layers and must be applied to preserved-source raster copies.

Inspect `color.profiles` before changing color interpretation. `document.profile.assign` leaves samples unchanged and changes what the numbers mean; `document.profile.convert` changes samples to preserve appearance. Do not assign a different profile as a shortcut for conversion. Supply a registered profile name or ICC byte array explicitly. `document.color` supports mode and bit-depth conversion; indexed, bitmap and duotone conversions require their corresponding `options` object. Review returned flattening notes before saving a variant over a source document.

Use `filter.context` to obtain the filter input origin before pixel-coordinate liquify strokes. Use the `forwardWarp` tool name; unsupported names are rejected. A clone source uses an Alt-modified down/up before the destination stroke. Tool opacity 100 means fully opaque; 1 means one percent.

For background removal, begin with an opaque source so the test proves segmentation rather than reuse of existing transparency. Toggle the resulting mask to verify source preservation. Full-resolution PNG/TIFF exports can retain supported ICC profiles; inspect the reopened profile and returned format-loss notes.

For clone/heal strokes, `tool.gesture` also accepts an explicit `cloneSource` anchor and source rotation, scale and flips. This avoids changing the human's shared Clone Source slots. Read the exact schema before constructing it. Use `effect.describe` and `layer.effect.set` to retain editable shadows, glows, overlays and other layer styles. Smart-filter masks are distinct from ordinary layer masks; inspect and render the intended mask explicitly. Export retained originals with `smartObject.export` when checking source preservation.

Verify exported image mode and depth after fresh reopening. RGB16 PNG and native-channel TIFF use the tiled decoder. An analytical CMYK working space has no embeddable ICC data; heed the explicit export loss rather than claiming portable color equivalence. PNG previews are display images and do not establish high-depth sample preservation.
