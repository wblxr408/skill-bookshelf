# onetake · 安装、来源与整理说明

- 原作者：Patrick / feitangyuan
- 上游：https://github.com/feitangyuan/onetake
- 收录日期：2026-10-22
- 许可：PolyForm Noncommercial 1.0.0；个人、学习、研究等非商业用途。Required Notice 与完整许可保留于 LICENSE，商业授权见作者 onetake Pro。

Required Notice: Copyright (c) 2026 Patrick. onetake is free for noncommercial use only.

下载并解压书橱 ZIP 后，执行 `python install.py --dest "~/.agents/skills" --only onetake`。Claude Code 将目标改为 `~/.claude/skills`。客户端下一轮重新发现技能后，用 `$onetake` 或 `/onetake` 调用。

## 运行依赖

Python 3.12；Playwright + Chromium、NumPy、SciPy、Pillow、Matplotlib、fonttools、brotli、OpenCV；FFmpeg / FFprobe、Node.js。Windows 配置见包内 references/windows-runtime.md；旁白与 3D 依赖按任务另配。

Windows 和本机环境见 [运行说明](references/windows-runtime.md)；其他平台按上游 README.md 配置。

## 本次整理

- 补充 Windows 虚拟环境与 UTF-8 运行说明，原动效与渲染实现保留。
- 示例成片 MP4 / GIF 链接至原作者，分发包保留脚本、模板、字体、图库与案例拆解。

上游案例成片与 GIF 在作者仓库查看；本包包含完整核心工具和创作资源，不包含虚拟环境、浏览器二进制、私有账户或 Pro 案例工程。
