# Windows 与 WSL 运行说明

这是王博为本机安装及书橱分发补充的说明。Cloudflare 的审计流程、验证器与报告 schema 保持原实现。

## 已安装的本机环境

技能位于用户目录 `.agents/skills/security-audit`，Claude Code 的同名目录共用这一份。现有 WSL 发行版是 Ubuntu-20.04，校验器专用 Linux Node.js v22.23.4 位于用户目录 `.codex/skill-runtimes/security-audit/node-linux/bin/node`。

原生 Windows Node 缺少上游 CLI 要求的 O_NOFOLLOW / O_NONBLOCK 组合。原校验器按设计拒绝读取输入；在 WSL 中执行原 CLI，可保留原始安全文件读取约束。

```powershell
$auditNode = & wsl.exe -d Ubuntu-20.04 --exec wslpath -u "$env:USERPROFILE/.codex/skill-runtimes/security-audit/node-linux/bin/node"
$auditSkill = & wsl.exe -d Ubuntu-20.04 --exec wslpath -u "$env:USERPROFILE/.agents/skills/security-audit"
$auditOutput = & wsl.exe -d Ubuntu-20.04 --exec wslpath -u 'D:/你的审计输出目录'
& wsl.exe -d Ubuntu-20.04 --exec $auditNode "$auditSkill/validate-findings.cjs" "$auditOutput/findings.json"
& wsl.exe -d Ubuntu-20.04 --exec $auditNode "$auditSkill/validate-coverage-ledger.cjs" "$auditOutput/coverage-ledger.json"
```

其他电脑使用自己的 Linux / macOS Node，或在自己的 WSL 中安装 Node 后运行 `node validate-findings.cjs <输出路径>/findings.json` 与 `node validate-coverage-ledger.cjs <输出路径>/coverage-ledger.json`。这两个校验器不需要 npm 依赖。

## 使用范围

Codex 使用 `$security-audit`，Claude Code 使用 `/security-audit`。安全问题和聚焦审查采用 guidance 模式；明确要求仓库全面审计或报告时，按上游 full audit 的六阶段工作流执行。

WSL 在本次安装中提供报告校验运行时；它本身不等于上游要求的目标代码执行沙箱。运行被审计仓库的构建、测试、服务或复现前，仍需满足 SKILL.md 中无外网、环境允许列表、只读目标、限制写入范围与资源配额的执行要求。缺少控制时使用源码证据，并保留精确的 needs_validation 缺口。本次安装没有审计任何用户项目。

完整上游来源与版本见 UPSTREAM.json，MIT 许可与 Cloudflare 署名见 LICENSE。
