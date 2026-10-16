# 统一任务连续性 · 完整融合版

Skill 名：`context-bridge`；维护：王博；发布版本：2026-10-16.1。

把本地交接、不可变记忆检查点和任务状态恢复组合起来。

## 下载与安装

从 https://bo-skill-bookshelf.vercel.app/#skill/context-bridge--local 下载单项包。解压后在包含 install.py 的目录运行：

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills" --only context-bridge
```

macOS / Linux：

```sh
python3 install.py --dest "$HOME/.agents/skills" --only context-bridge
```

Claude Code 将目标换为 `~/.claude/skills`。Codex 也可使用其实际配置识别的 `~/.codex/skills`。以客户端当前配置为准；重新打开会话后显式使用 `$context-bridge`，Claude Code 使用 `/context-bridge`。

同名目录默认拒绝覆盖。确需替换时加 `--replace`，旧目录备份到目标目录下 `.bo-backups/<时间>/`，安装器输出备份位置。安装依赖：dev。单项 ZIP 已带齐这些依赖及其依赖；不需要再下载仓库收录版。

从 Git 克隆安装：先运行 `python tools/build_downloads.py --out <输出目录>` 生成标准包后解压安装，或者把本项与清单依赖目录复制到同一 skills 目录。

## 使用示例

用 $context-bridge 保存这个长任务的目标、最新修正、工作现场和下一步，以便之后恢复。

预期产物：本地交接包或 Basic Memory 检查点。

使用边界：其中 harness 原作者仍待核实；不宣称完整保留所有语义。

## 运行依赖

Python 3.9+，核心脚本仅用标准库。Basic Memory 保存/恢复分支需要用户自行配置 Basic Memory MCP；本地交接分支可独立使用。

包内脚本使用已安装的 Python / Node；外部服务、模型、连接器和系统编译工具不会随 Skill ZIP 自动安装，也不会共享发布者账户。按选择的操作加载 SKILL.md 中相应分支，不要一次读取整套参考资料。

## 文件与来源

SKILL.md 为正式入口；modules / scripts / references / 模板等保留完整资源。ATTRIBUTION.md 列原作者和模块来源，CHANGES.md 列个人融合与此次可移植修改，distribution.json 列依赖与源文件数量。

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 Basic Memory 插件元数据署名 Basic Machines，license=MIT，来源 plugins/codex；harness 原始作者未确认。
