# 统一前端设计 · 完整融合版

Skill 名：`impeccable`；维护：王博；发布版本：2026-10-16.1。

统一视觉设计、实现、响应式和界面精修。

## 下载与安装

从 https://bo-skill-bookshelf.vercel.app/#skill/impeccable--local 下载单项包。解压后在包含 install.py 的目录运行：

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills" --only impeccable
```

macOS / Linux：

```sh
python3 install.py --dest "$HOME/.agents/skills" --only impeccable
```

Claude Code 将目标换为 `~/.claude/skills`。Codex 也可使用其实际配置识别的 `~/.codex/skills`。以客户端当前配置为准；重新打开会话后显式使用 `$impeccable`，Claude Code 使用 `/impeccable`。

同名目录默认拒绝覆盖。确需替换时加 `--replace`，旧目录备份到目标目录下 `.bo-backups/<时间>/`，安装器输出备份位置。安装依赖：dev。单项 ZIP 已带齐这些依赖及其依赖；不需要再下载仓库收录版。

从 Git 克隆安装：先运行 `python tools/build_downloads.py --out <输出目录>` 生成标准包后解压安装，或者把本项与清单依赖目录复制到同一 skills 目录。

## 使用示例

用 $impeccable 为这个页面设计并实现与现有品牌一致的界面，先说明视觉方向，再完成当前交互。

预期产物：界面代码、视觉方案与观察证据。

使用边界：需要实际浏览器验证；设计指南不能证明功能正确。

## 运行依赖

Node.js 18+（使用 JS 工具时）；Impeccable engine 由保留的启动器按原项目方式获取。浏览器验证需客户端提供浏览器工具。

包内脚本使用已安装的 Python / Node；外部服务、模型、连接器和系统编译工具不会随 Skill ZIP 自动安装，也不会共享发布者账户。按选择的操作加载 SKILL.md 中相应分支，不要一次读取整套参考资料。

## 文件与来源

SKILL.md 为正式入口；modules / scripts / references / 模板等保留完整资源。ATTRIBUTION.md 列原作者和模块来源，CHANGES.md 列个人融合与此次可移植修改，distribution.json 列依赖与源文件数量。

各模块分别适用其原许可。保留模块内 LICENSE / NOTICE；不得用王博的署名替代原作者。
