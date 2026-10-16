# 统一论文审查 · 书橱整理说明

原作者/分发来源：bahayonghang / Imbad0202 / Academic Research Skills。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [bahayonghang](https://github.com/bahayonghang/academic-writing-skills)
- [Imbad0202 / Academic Research Skills](https://github.com/Imbad0202/academic-research-skills)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=paper-audit`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $paper-audit 审查这篇稿件，按严重性列出证据、位置和最小修订建议。

运行条件：Python 3.10+；PDF 输入按需安装 pypdf 或 PyMuPDF；稿件相关编译依赖由稿件项目提供。

审查结论受稿件和可访问证据限制。

## 来源与去重

合并 7 份安装记录，保留 5 个资源版本。已吸收或兼容名称：academic-paper-review, academic-paper-reviewer。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 ARS 当前公开许可为 CC BY-NC 4.0（原作者 Cheng-I Wu）；其完整文本随包保留。 academic-writing-skills 根目录未找到统一 LICENSE；保留作者的安装/自行修改说明及原文件，不另宣称 MIT 或商业许可。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。
