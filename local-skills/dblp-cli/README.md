# DBLP Skill (no MCP server)

Single-skill repo for DBLP search, fuzzy title/author lookup, venue info, statistics, and BibTeX collection/export. Current version: 0.1.0.

## Layout

- `SKILL.md` — skill metadata and usage notes.
- `scripts/dblp_cli.py` — CLI entry point (executable).
- `refs.bib` — sample export (ignored by git).

## Install (Codex)

1. Clone: `git clone <this-repo> ~/dblp-skills`
2. Link into Codex skills dir: `mkdir -p ~/.codex/skills && ln -s ~/dblp-skills ~/.codex/skills/dblp-cli`
3. Restart Codex; skill name is `dblp-cli`.

## Dependencies & Network

- Python 3.11+; `requests`. Legacy pyopenssl quirks are handled in the script.
- Requires outbound HTTPS to `https://dblp.org/`.

## Quickstart / Smoke test

```bash
./scripts/dblp_cli.py search --query "transformer and retrieval" --max-results 5
./scripts/dblp_cli.py add-bibtex --dblp-key conf/nips/VaswaniSPUJGKP17 --citation-key Vaswani2017
./scripts/dblp_cli.py export-bibtex --path /tmp/refs.bib
```
Smoke test:
```bash
./scripts/dblp_cli.py search --query "test" --max-results 1
./scripts/dblp_cli.py add-bibtex --dblp-key conf/nips/VaswaniSPUJGKP17 --citation-key Vaswani2017
./scripts/dblp_cli.py export-bibtex --path /tmp/refs.bib
```
Expected: first command returns JSON; export writes `/tmp/refs.bib` and clears the buffer.

## State / Cache

BibTeX buffer: `~/.codex/dblp-skill/state.json`, cleared after `export-bibtex`. Delete the file to reset.

## Packaging (optional)

You can package with Codex’s `package_skill.py`: `python /path/to/scripts/package_skill.py ~/dblp-skills`, then install the generated `.skill`.

---

# DBLP 技能（无需 MCP 服务器）

单技能仓库，提供 DBLP 搜索、模糊标题/作者检索、venue 信息、统计，以及 BibTeX 收集/导出。当前版本：0.1.0。

## 目录结构

- `SKILL.md`：技能元数据与用法。
- `scripts/dblp_cli.py`：CLI 入口（可执行）。
- `refs.bib`：导出示例（git 忽略）。

## 安装（Codex）

1. 克隆：`git clone <this-repo> ~/dblp-skills`
2. 链接到 Codex 技能目录：`mkdir -p ~/.codex/skills && ln -s ~/dblp-skills ~/.codex/skills/dblp-cli`
3. 重启 Codex，会话中的技能名为 `dblp-cli`。

## 依赖与网络

- Python 3.11+；`requests`。脚本内已处理旧版 pyopenssl 兼容。
- 需要访问 `https://dblp.org/`。

## 快速上手 / 冒烟测试

```bash
./scripts/dblp_cli.py search --query "transformer and retrieval" --max-results 5
./scripts/dblp_cli.py add-bibtex --dblp-key conf/nips/VaswaniSPUJGKP17 --citation-key Vaswani2017
./scripts/dblp_cli.py export-bibtex --path /tmp/refs.bib
```
冒烟：
```bash
./scripts/dblp_cli.py search --query "test" --max-results 1
./scripts/dblp_cli.py add-bibtex --dblp-key conf/nips/VaswaniSPUJGKP17 --citation-key Vaswani2017
./scripts/dblp_cli.py export-bibtex --path /tmp/refs.bib
```
预期：第一条返回 JSON；导出生成 `/tmp/refs.bib` 并清空缓冲。

## 状态 / 缓存

BibTeX 缓冲存放 `~/.codex/dblp-skill/state.json`，`export-bibtex` 后清空。删除可重置。

## 打包（可选）

可用 Codex 的 `package_skill.py` 打包：`python /path/to/scripts/package_skill.py ~/dblp-skills`，生成 `.skill` 后按 Codex 指引安装。
