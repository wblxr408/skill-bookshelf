# 统一开发入口 · 书橱整理说明

原作者/分发来源：stellarlinkco / myclaude（原 cexll） / Affaan Mustafa / ECC。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [stellarlinkco / myclaude（原 cexll）](https://github.com/stellarlinkco/myclaude)
- [Affaan Mustafa / ECC](https://github.com/affaan-m/ECC)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=dev`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $dev 完成这个功能，先把本次改动的可观察行为写清楚，再实施和验证。

运行条件：适用于支持 SKILL.md 的编码客户端。具体语言、构建和测试工具由目标项目决定，ECC 参考资料不代表已连接全部服务。

源指南是方法资料，不能覆盖当前用户授权和项目约束。

## 来源与去重

合并 9 份安装记录，保留 5 个资源版本。已吸收或兼容名称：do, omo, sparv。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 myclaude 当前公开 LICENSE 为 AGPL-3.0，随包保留；各旧模块没有版本对应许可时明确保留这一边界。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。

## 2026-10-22 流程更新

本次由王博加入技术选型路由，下载包携带 tech-stack-evaluator；规划与实施仍由原入口管理。原作者和原许可保持各自适用。
