# 统一浏览器操作 · 完整融合版

Skill 名：`browser`；维护：王博；发布版本：2026-10-16.1。

按任务在已登录标签页操作、隔离验收和调试浏览器之间选路。

## 下载与安装

从 https://bo-skill-bookshelf.vercel.app/#skill/browser--local 下载单项包。解压后在包含 install.py 的目录运行：

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills" --only browser
```

macOS / Linux：

```sh
python3 install.py --dest "$HOME/.agents/skills" --only browser
```

Claude Code 将目标换为 `~/.claude/skills`。Codex 也可使用其实际配置识别的 `~/.codex/skills`。以客户端当前配置为准；重新打开会话后显式使用 `$browser`，Claude Code 使用 `/browser`。

同名目录默认拒绝覆盖。确需替换时加 `--replace`，旧目录备份到目标目录下 `.bo-backups/<时间>/`，安装器输出备份位置。安装依赖：dev。单项 ZIP 已带齐这些依赖及其依赖；不需要再下载仓库收录版。

从 Git 克隆安装：先运行 `python tools/build_downloads.py --out <输出目录>` 生成标准包后解压安装，或者把本项与清单依赖目录复制到同一 skills 目录。

## 使用示例

用 $browser 按当前可用的浏览器工具完成这个网页操作，记录实际交互结果。

预期产物：操作结果、截图和行为证据。

使用边界：历史成功支持选路，不代表适配器具有普遍可靠性排名。

## 运行依赖

已有标签页操作需要客户端提供 cua_repl 等浏览器工具。CDP 路线需 Node.js 18+，在安装后的 browser 目录执行 npm install；本地验收需自行安装 Playwright 与浏览器。

包内脚本使用已安装的 Python / Node；外部服务、模型、连接器和系统编译工具不会随 Skill ZIP 自动安装，也不会共享发布者账户。按选择的操作加载 SKILL.md 中相应分支，不要一次读取整套参考资料。

## 文件与来源

SKILL.md 为正式入口；modules / scripts / references / 模板等保留完整资源。ATTRIBUTION.md 列原作者和模块来源，CHANGES.md 列个人融合与此次可移植修改，distribution.json 列依赖与源文件数量。

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 myclaude 当前公开 LICENSE 为 AGPL-3.0，随包保留；各旧模块没有版本对应许可时明确保留这一边界。
