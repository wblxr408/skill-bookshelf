# OpenSpec 规格同步 · 书橱整理说明

原作者/分发来源：OpenSpec。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [OpenSpec](https://github.com/Fission-AI/OpenSpec)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=openspec-sync-specs`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

使用 $openspec-sync-specs 完成具体任务；先读取入口，按需加载相关参考资料。

运行条件：按源文件中的运行依赖说明配置 Python、Node 或相应专用工具。

按 SKILL.md 及其运行说明配置依赖；原作者与许可不因本站收录而改变。

## 来源与去重

合并 3 份安装记录，保留 2 个资源版本。已吸收或兼容名称：无额外别名。原始使用说明见 SKILL.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

MIT

来源待核实项保持待核实，不以收藏者或分发者代替原作者。
