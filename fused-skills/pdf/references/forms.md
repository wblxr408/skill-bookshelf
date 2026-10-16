# forms

Retain the native module's complete Fill And Validate AcroForms section and its code. Inspect reader.get_fields and every page Widget, following Parent/Kids. A widget's appearance value is not proof of canonical AcroForm field correctness. Reattach genuinely orphaned widgets, update all relevant pages, and assert expected names/values after writing.

When distinct canonical/widget objects share a name without a Parent relation, do not blindly reattach and create duplicate fields; diagnose the ambiguity. Keep interactive by default. Flatten only when explicitly requested: paint existing values plus changes, remove Widget annotations, and remove the AcroForm tree as appropriate. Preserve a signed source and make no silent signature-preservation claim after mutation. Render completed pages as well as checking structural values.
