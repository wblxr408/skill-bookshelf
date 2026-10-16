---
name: pdf
description: Read, create, edit, render, and validate PDFs, including interactive forms, layout fidelity, extraction, and export.
metadata:
  version: "fusion-2026-10-05"
---

# PDF — unified PDF workflow

Read [the execution contract](references/fusion-policy.md). Use the requested PDF operation to select only the needed guide.

| Need | Read next |
|---|---|
| Read/extract/review PDF content | [read and inspect](references/read-and-inspect.md) |
| Create, edit, render, or verify layout | [author and render](references/author-and-render.md) |
| Fill, repair, preserve, or explicitly flatten an interactive AcroForm | [forms](references/forms.md) |
| Runtime dependencies and tool fallback | [runtime](references/runtime.md) |

The native and portable resources are retained in [native module](modules/native/PLAYBOOK.md) and [portable module](modules/portable/PLAYBOOK.md). Use the bundled workspace runtime first; Python pypdf/pdfplumber/reportlab and Poppler/PyMuPDF are tools for the chosen operation, not all mandatory dependencies for every request.

Render affected pages for layout judgment and inspect text only for semantic checks. A visible form value is not enough: verify the canonical AcroForm field tree and page widgets. Keep forms interactive unless the user requests a static result; preserve the source and signatures. Do not create duplicate field names when repairing widgets.

For an actual PDF authoring operation, run the retained root `container_tools/mark_artifact_operation_started.mjs` once immediately before authoring when the host requires this artifact contract. Use workspace scratch/output conventions, sensible typography, and accurate links/citations. Batch actual fixes and confirm affected pages; do not rerender unchanged pages in a loop.
