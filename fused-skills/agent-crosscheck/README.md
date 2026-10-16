# 统一成果审查 · 完整融合版

Skill 名：`agent-crosscheck`；维护：王博；发布版本：2026-10-16.1。

同时从用户目的和技术正确性审阅成果，输出一份去重结论。

## 下载与安装

从 https://bo-skill-bookshelf.vercel.app/#skill/agent-crosscheck--local 下载单项包。解压后在包含 install.py 的目录运行：

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills" --only agent-crosscheck
```

macOS / Linux：

```sh
python3 install.py --dest "$HOME/.agents/skills" --only agent-crosscheck
```

Claude Code 将目标换为 `~/.claude/skills`。Codex 也可使用其实际配置识别的 `~/.codex/skills`。以客户端当前配置为准；重新打开会话后显式使用 `$agent-crosscheck`，Claude Code 使用 `/agent-crosscheck`。

同名目录默认拒绝覆盖。确需替换时加 `--replace`，旧目录备份到目标目录下 `.bo-backups/<时间>/`，安装器输出备份位置。安装依赖：dev。单项 ZIP 已带齐这些依赖及其依赖；不需要再下载仓库收录版。

从 Git 克隆安装：先运行 `python tools/build_downloads.py --out <输出目录>` 生成标准包后解压安装，或者把本项与清单依赖目录复制到同一 skills 目录。

## 使用示例

用 $agent-crosscheck 审查这份结果是否满足原目标，给出有证据的问题和最小修复建议。

预期产物：带证据的问题和最小修复建议。

使用边界：融合由王博完成；两个原始入口作者尚无足够证据。

## 运行依赖

支持技能的 AI 客户端；开发结果审查共享包内 dev 规则。独立审查角色仅在用户授权和工具可用时使用。

包内脚本使用已安装的 Python / Node；外部服务、模型、连接器和系统编译工具不会随 Skill ZIP 自动安装，也不会共享发布者账户。按选择的操作加载 SKILL.md 中相应分支，不要一次读取整套参考资料。

## 文件与来源

SKILL.md 为正式入口；modules / scripts / references / 模板等保留完整资源。ATTRIBUTION.md 列原作者和模块来源，CHANGES.md 列个人融合与此次可移植修改，distribution.json 列依赖与源文件数量。

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。 原始 agent-crosscheck / intent-review 作者尚未核实，不宣称原始部分为王博原创。
