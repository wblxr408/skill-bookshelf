# 统一浏览器操作 · 书橱整理说明

原作者/分发来源：stellarlinkco / myclaude（原 cexll） / OpenAI。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [stellarlinkco / myclaude（原 cexll）](https://github.com/stellarlinkco/myclaude)
- [OpenAI](https://github.com/openai/skills)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=browser`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $browser 按当前可用的浏览器工具完成这个网页操作，记录实际交互结果。

运行条件：已有标签页操作需要客户端提供 cua_repl 等浏览器工具。CDP 路线需 Node.js 18+，在安装后的 browser 目录执行 npm install；本地验收需自行安装 Playwright 与浏览器。

历史成功支持选路，不代表适配器具有普遍可靠性排名。

## 来源与去重

合并 4 份安装记录，保留 4 个资源版本。已吸收或兼容名称：playwright。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 myclaude 当前公开 LICENSE 为 AGPL-3.0，随包保留；各旧模块没有版本对应许可时明确保留这一边界。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。
