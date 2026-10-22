# Windows 运行环境

本文是书橱维护者补充的运行说明；原动效库、脚本、模板和创作方法由 Patrick / feitangyuan 提供。

## 本机已配置环境

本次安装将 Python 3.12 虚拟环境放在用户目录下 `.codex/skill-runtimes/onetake/python`，已安装核心依赖和 Chromium。Windows PowerShell 执行原说明中的 `python3 scripts/...` 时，改用以下解释器，并启用 UTF-8，避免中文 Windows 的默认编码影响字体和 JSON 读取：

```powershell
$env:PYTHONUTF8 = '1'
$otkPython = Join-Path $env:USERPROFILE '.codex/skill-runtimes/onetake/python/Scripts/python.exe'
& $otkPython '<技能目录>/scripts/render.py' '<项目目录>/comp.html' --out '<输出目录>/draft.mp4'
```

相对脚本路径从本技能目录解析。FFmpeg、FFprobe 和 Node.js 使用系统环境中的命令；工作文件和成片写入当前项目。不要把虚拟环境或凭据复制进分发包。

## 在其他电脑安装

先安装 Python 3.12、FFmpeg 和 Node.js，再创建自己电脑的虚拟环境：

```powershell
py -3.12 -m venv "$env:USERPROFILE/.codex/skill-runtimes/onetake/python"
$otkPython = Join-Path $env:USERPROFILE '.codex/skill-runtimes/onetake/python/Scripts/python.exe'
& $otkPython -m pip install playwright numpy scipy Pillow matplotlib fonttools brotli opencv-python
& $otkPython -m playwright install chromium
$env:PYTHONUTF8 = '1'
```

也可用 uv 创建相同路径的环境。旁白、词级时间戳和 3D 路线各自需要上游说明中的 Kokoro / faster-whisper 或 three.js / Blender；按任务安装，不属于核心渲染依赖。中文字体通过 look.py 的 --cjk 参数提供。

## 调用

Codex 使用 `$onetake`，Claude Code 使用 `/onetake`。例如：给这个 App 做 15 秒一镜到底发布片，提供 HTML 工程和 MP4。已有项目继续采用项目原框架；明确指定 onetake 时使用本技能。

许可为 PolyForm Noncommercial 1.0.0，Required Notice 和完整原文见根目录 LICENSE。商业用途按作者的 onetake Pro 授权处理。
