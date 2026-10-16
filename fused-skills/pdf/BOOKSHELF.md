# 统一 PDF 工作流 · 书橱整理说明

原作者/分发来源：OpenAI。王博负责分类、去重与分发适配；原有融合修改见本目录 CHANGES.md（如有）。

- [OpenAI](https://github.com/openai/skills)

## 安装与使用

单项包携带清单中的共享依赖。解压后运行 `python install.py --dest "~/.agents/skills" --only=pdf`。同名默认拒绝覆盖；显式 `--replace` 时先备份。Claude Code 将目标换为 ~/.claude/skills；其他客户端按其识别目录配置。macOS/Linux 可使用 python3。

用 $pdf 读取这份 PDF 并处理表单，保留交互字段，输出修改结果和受影响页预览。

运行条件：Python 3.10+；按操作安装 pypdf、pdfplumber、reportlab、PyMuPDF。Poppler / pdftoppm 为可选渲染工具；Node.js 仅供宿主需要的文档标记脚本。

本地 pdf 的精确原始谱系未完全核实，保留该证据边界。

## 来源与去重

合并 2 份安装记录，保留 2 个资源版本。已吸收或兼容名称：无额外别名。原始使用说明见 README.md。独立来源版本见 BOOKSHELF.json 和仓库 skill-versions。

## 此次分发修改

- 本机原始文件仅读取，没有改写安装目录。
- 排除依赖安装产物、缓存、环境配置和冗余旧压缩包。
- 保留脚本、模板、图片、参考资料与原许可；仅对公开副本中的发布者主目录做可移植替换。

## 许可

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。

来源待核实项保持待核实，不以收藏者或分发者代替原作者。

## 宿主与插件状态

本地插件目录包含缓存；文件存在不代表该插件目前启用。使用需对应宿主、插件及可用连接器。
