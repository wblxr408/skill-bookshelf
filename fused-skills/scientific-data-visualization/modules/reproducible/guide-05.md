## Prompt-and-table routing

When the runtime input is only a table plus a human prompt, do not inspect the reference screenshots. Build the local index once with `scripts/build_gallery_index.py`, then run:

```powershell
python scripts/route_from_prompt.py data.xlsx --sheet Sheet1 --prompt "比较不同处理组的分布，优先显示离群值" 
```

The router uses local `rg` retrieval over a line-oriented index, then rejects chart types incompatible with the actual column profile. It returns at most three compact candidates. Rebuild the index after catalogue edits. If a new PNG appears in `figures/` without a catalogue mapping, `build_gallery_index.py --check` must fail; classify it before using it as evidence.

If the desired type is absent, report it as absent instead of pretending that a visually similar type is an exact reference match.
