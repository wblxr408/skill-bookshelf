# 研究入口分流版 · 书橱整理说明

原作者/分发来源：Imbad0202 / Academic Research Skills。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [Imbad0202 / Academic Research Skills](https://github.com/Imbad0202/academic-research-skills)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=deep-research`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $deep-research 调研这个问题，交付可追溯的来源、分歧和证据边界。

运行条件：支持联网检索的 AI 客户端；论文链接、数据库或模型服务需用户自己的连接。不会随包分发 API 密钥。

此项是个人路由修改版，不是另造一套研究方法。

## 来源与去重

合并 3 份安装记录，保留 3 个资源版本。已吸收或兼容名称：无额外别名。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 ARS 当前公开许可为 CC BY-NC 4.0（原作者 Cheng-I Wu）；其完整文本随包保留。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。
