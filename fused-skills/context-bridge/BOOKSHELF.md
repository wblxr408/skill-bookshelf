# 统一任务连续性 · 书橱整理说明

原作者/分发来源：王博 / wblxr408 / Basic Memory。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [王博 / wblxr408](https://github.com/wblxr408/skill-bookshelf)
- [Basic Memory](https://github.com/basicmachines-co/basic-memory)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=context-bridge`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $context-bridge 保存这个长任务的目标、最新修正、工作现场和下一步，以便之后恢复。

运行条件：Python 3.9+，核心脚本仅用标准库。Basic Memory 保存/恢复分支需要用户自行配置 Basic Memory MCP；本地交接分支可独立使用。

其中 harness 原作者仍待核实；不宣称完整保留所有语义。

## 来源与去重

合并 9 份安装记录，保留 6 个资源版本。已吸收或兼容名称：bm-checkpoint, bm-orient, harness。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 Basic Memory 插件元数据署名 Basic Machines，license=MIT，来源 plugins/codex；harness 原始作者未确认。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。

## 宿主与插件状态

本地插件目录包含缓存；文件存在不代表该插件目前启用。使用需对应宿主、插件及可用连接器。
