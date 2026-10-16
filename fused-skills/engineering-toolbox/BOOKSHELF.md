# 工程专项工具箱 · 书橱整理说明

原作者/分发来源：Affaan Mustafa / ECC。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [Affaan Mustafa / ECC](https://github.com/affaan-m/ECC)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=engineering-toolbox`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $engineering-toolbox 从目录中选择与当前技术问题匹配的一份专项指南，交给当前任务的主入口使用。

运行条件：使用包内 dev 的 ECC 资料库；具体框架、外部服务和依赖按所选指南配置。

311 是映射规模，不代表每项服务都在本机实测。

## 来源与去重

合并 2 份安装记录，保留 1 个资源版本。已吸收或兼容名称：无额外别名。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。
