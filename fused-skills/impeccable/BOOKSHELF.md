# 统一前端设计 · 书橱整理说明

原作者/分发来源：Paul Bakaus / Impeccable / Anthropic。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [Paul Bakaus / Impeccable](https://github.com/pbakaus/impeccable)
- [Anthropic](https://github.com/anthropics/skills)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=impeccable`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $impeccable 为这个页面设计并实现与现有品牌一致的界面，先说明视觉方向，再完成当前交互。

运行条件：Node.js 18+（使用 JS 工具时）；Impeccable engine 由保留的启动器按原项目方式获取。浏览器验证需客户端提供浏览器工具。

需要实际浏览器验证；设计指南不能证明功能正确。

## 来源与去重

合并 4 份安装记录，保留 3 个资源版本。已吸收或兼容名称：frontend-design。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。
