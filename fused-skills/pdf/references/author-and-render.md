# author and render

Use reportlab or the project's existing PDF-producing tool for the actual layout; use pypdf for structural edits. Preserve source copies. Choose sensible margins, typography, page breaks, image/vector resolution, links, and content hierarchy. Native-module tools/contract requirements retain the host's one-time authoring marker. Use workspace scratch and user output directories.

Render changed pages, inspect clipping, alignment, overflow, font glyphs, readability, and image quality; batch fixes then confirm affected output. Check that text/order/links required by the task are actually present. Do not let text extraction substitute for visual review or regenerate unchanged pages without a reason.
