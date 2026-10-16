# 研究到投稿流水线 · 书橱整理说明

原作者/分发来源：Imbad0202 / Academic Research Skills。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [Imbad0202 / Academic Research Skills](https://github.com/Imbad0202/academic-research-skills)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=academic-pipeline`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

None

运行条件：None

整体流程较重，单点修改宜直接选对应技能。

## 来源与去重

合并 3 份安装记录，保留 3 个资源版本。已吸收或兼容名称：无额外别名。原始使用说明见 SKILL.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

见源项目说明，本站不另授许可

来源待核实项保持待核实，不以收藏者或分发者代替原作者。
