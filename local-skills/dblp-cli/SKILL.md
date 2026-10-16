---
name: dblp-cli
description: Local DBLP helper without MCP; use to search DBLP, fuzzy title/author queries, venue lookup, BibTeX collection/export, and stats via the bundled CLI script instead of running an MCP server.
---

## 本机已安装的运行环境

本机依赖和调用方式见 [运行环境说明](references/research-runtime.md)。Python 脚本使用 `python`，并从本技能目录解析脚本的绝对路径；R 使用该说明中的 R 与包库路径。

# Usage

- Scope: DBLP search, fuzzy title/author lookup, venue info, BibTeX collect/export, stats. No MCP server needed.
- Entry: `scripts/dblp_cli.py` (executable). Depends on `requests`; needs network access to `https://dblp.org/`.
- State: BibTeX buffer stored at `~/.codex/dblp-skill/state.json`, cleared after `export-bibtex`.

## Common commands

```bash
scripts/dblp_cli.py search --query "transformer and retrieval" --max-results 5 --year-from 2018 --venue-filter iclr

scripts/dblp_cli.py fuzzy --title "attention is all you need" --similarity-threshold 0.6 --max-results 5 --include-bibtex

scripts/dblp_cli.py author --name "Geoffrey Hinton" --similarity-threshold 0.7 --max-results 10

scripts/dblp_cli.py venue --name ICLR

scripts/dblp_cli.py stats --input results.json   # or --input -

scripts/dblp_cli.py add-bibtex --dblp-key conf/nips/VaswaniSPUJGKP17 --citation-key Vaswani2017
scripts/dblp_cli.py export-bibtex --path /tmp/refs.bib
```

## Parameter notes

- `search` supports `--year-from/--year-to` and `--venue-filter`; `--include-bibtex` fetches BibTeX.
- `fuzzy`/`author` use `--similarity-threshold` in [0,1]; higher is stricter.
- `stats` expects an array with `title/authors/venue/year`; supports stdin via `--input -`.
- `add-bibtex` strips `.bib` suffix or `dblp.org/rec/` prefix and overwrites duplicate citation keys.
- `export-bibtex` appends `.bib`, creates parent dirs, and clears the buffer after export.

## Tips

- Use `search` or `fuzzy` to get `dblp_key`, then immediately `add-bibtex`, and export once at the end.
- Add author/year hints for better hits, e.g. `--query "attention vaswani 2017"`.
- DBLP may rate-limit; keep request rate reasonable.
