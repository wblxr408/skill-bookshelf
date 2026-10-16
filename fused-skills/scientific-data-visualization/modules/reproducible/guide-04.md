## Reference-gallery routing

Treat `figures/` as a visual reference corpus, not as generated examples. Never load the complete catalogue into context. Route in three stages:

1. Read `references/gallery-routing.md` only to select a **major family**.
2. Run `scripts/query_gallery.py --category <major-family>` or `--search <phrase>` to list only **minor families** or short candidate records.
3. Run `scripts/query_gallery.py --type-id <id>` for the compact exact record. Add `--detail` only for final selection, ambiguous recognition, or implementation.
4. For ambiguous visual matches, resolve a returned evidence ID with `--source-id src-XX` and inspect that one original screenshot before deciding.
