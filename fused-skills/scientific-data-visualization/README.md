# 统一科研绘图 · 完整融合版

Skill 名：`scientific-data-visualization`；维护：王博；发布版本：2026-10-16.1。

融合个人可复现绘图流程与 SciPilot 的图型判断和期刊出图方法。

## 下载与安装

从 https://bo-skill-bookshelf.vercel.app/#skill/scientific-data-visualization--local 下载单项包。解压后在包含 install.py 的目录运行：

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills" --only scientific-data-visualization
```

macOS / Linux：

```sh
python3 install.py --dest "$HOME/.agents/skills" --only scientific-data-visualization
```

Claude Code 将目标换为 `~/.claude/skills`。Codex 也可使用其实际配置识别的 `~/.codex/skills`。以客户端当前配置为准；重新打开会话后显式使用 `$scientific-data-visualization`，Claude Code 使用 `/scientific-data-visualization`。

同名目录默认拒绝覆盖。确需替换时加 `--replace`，旧目录备份到目标目录下 `.bo-backups/<时间>/`，安装器输出备份位置。安装依赖：dev。单项 ZIP 已带齐这些依赖及其依赖；不需要再下载仓库收录版。

从 Git 克隆安装：先运行 `python tools/build_downloads.py --out <输出目录>` 生成标准包后解压安装，或者把本项与清单依赖目录复制到同一 skills 目录。

## 使用示例

用 $scientific-data-visualization 分析 data.csv，先判断数据结构和图型，再输出 SVG 与 PNG。

预期产物：绘图规格、图形与渲染报告。

使用边界：图形不能替代统计推断；不自动制造显著性。

## 运行依赖

Python 3.10+。按任务使用 numpy、pandas、matplotlib、scipy、PyYAML、openpyxl；期刊方案按需用 seaborn、SciencePlots、plotly。

包内脚本使用已安装的 Python / Node；外部服务、模型、连接器和系统编译工具不会随 Skill ZIP 自动安装，也不会共享发布者账户。按选择的操作加载 SKILL.md 中相应分支，不要一次读取整套参考资料。

## 文件与来源

SKILL.md 为正式入口；modules / scripts / references / 模板等保留完整资源。ATTRIBUTION.md 列原作者和模块来源，CHANGES.md 列个人融合与此次可移植修改，distribution.json 列依赖与源文件数量。

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。
