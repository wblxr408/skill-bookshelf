# 宿主与安装路径

Codex 可安装到 ~/.agents/skills/context-bridge；Claude Code 可安装到 ~/.claude/skills/context-bridge。也可选择客户端实际识别的 skills 目录。两端各自安装即可，不依赖发布者机器上的 junction。

在技能目录之外执行脚本时，用你实际安装目录的绝对路径。Python 3.9+，核心脚本只使用标准库。例如 PowerShell：

```powershell
$skillPath = Join-Path $env:USERPROFILE '.agents/skills/context-bridge'
python (Join-Path $skillPath 'scripts/requirements.py') brief '<bundle>' --scope '<scope>'
```

Basic Memory 分支需要使用者自己的 MCP 配置和项目；本地交接分支不依赖 Basic Memory。不要复制发布者的聊天 ID、仓库现场或凭据。不同客户端不会自动共享登录态或线程。
