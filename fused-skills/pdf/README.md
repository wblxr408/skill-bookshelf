# 统一 PDF 工作流 · 完整融合版

Skill 名：`pdf`；维护：王博；发布版本：2026-10-16.1。

组合本地与官方 PDF 方法，统一提取、编辑、渲染与表单处理。

## 下载与安装

从 https://bo-skill-bookshelf.vercel.app/#skill/pdf--local 下载单项包。解压后在包含 install.py 的目录运行：

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills" --only pdf
```

macOS / Linux：

```sh
python3 install.py --dest "$HOME/.agents/skills" --only pdf
```

Claude Code 将目标换为 `~/.claude/skills`。Codex 也可使用其实际配置识别的 `~/.codex/skills`。以客户端当前配置为准；重新打开会话后显式使用 `$pdf`，Claude Code 使用 `/pdf`。

同名目录默认拒绝覆盖。确需替换时加 `--replace`，旧目录备份到目标目录下 `.bo-backups/<时间>/`，安装器输出备份位置。安装依赖：dev。单项 ZIP 已带齐这些依赖及其依赖；不需要再下载仓库收录版。

从 Git 克隆安装：先运行 `python tools/build_downloads.py --out <输出目录>` 生成标准包后解压安装，或者把本项与清单依赖目录复制到同一 skills 目录。

## 使用示例

用 $pdf 读取这份 PDF 并处理表单，保留交互字段，输出修改结果和受影响页预览。

预期产物：PDF、提取数据与版面预览。

使用边界：本地 pdf 的精确原始谱系未完全核实，保留该证据边界。

## 运行依赖

Python 3.10+；按操作安装 pypdf、pdfplumber、reportlab、PyMuPDF。Poppler / pdftoppm 为可选渲染工具；Node.js 仅供宿主需要的文档标记脚本。

包内脚本使用已安装的 Python / Node；外部服务、模型、连接器和系统编译工具不会随 Skill ZIP 自动安装，也不会共享发布者账户。按选择的操作加载 SKILL.md 中相应分支，不要一次读取整套参考资料。

## 文件与来源

SKILL.md 为正式入口；modules / scripts / references / 模板等保留完整资源。ATTRIBUTION.md 列原作者和模块来源，CHANGES.md 列个人融合与此次可移植修改，distribution.json 列依赖与源文件数量。

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。
