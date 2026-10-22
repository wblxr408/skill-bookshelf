# security-audit · 安装、来源与整理说明

原作者：Cloudflare, Inc.；MIT 许可见 LICENSE。上游固定版本：https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8 。

解压书橱 ZIP 后执行 `python install.py --dest "~/.agents/skills" --only security-audit`，Claude Code 将目标改为 `~/.claude/skills`。Codex 用 `$security-audit`，Claude Code 用 `/security-audit`。

## 运行依赖

支持工具调用与子代理的编程客户端；Node.js 用于两个零依赖报告校验器。Windows 的校验命令通过 WSL / Linux Node 执行，见包内 WINDOWS.md。执行目标代码时需要上游规定的操作系统沙箱。

示例：用 $security-audit 对这个仓库做 standard 安全审计，输出架构、覆盖台账、findings.json 和报告；仅将有完整源码证据及验证结果的问题标记为 confirmed。

## 本次整理

- 补齐上游仓库根目录 README、MIT LICENSE 与固定版本来源记录。
- 补充 Windows / WSL 校验运行说明；原审计流程、报告 schema 和两个验证器保持上游实现。

本包带齐上游技能目录的所有领域指南、schema、两个验证器及其测试资料。客户端、模型、目标工程、账户和操作系统沙箱由实际使用环境提供。本次安装验证报告契约与下载分发，没有执行用户项目安全审计。
