# 技术栈与依赖选型 · 书橱整理说明

原作者 Alireza Rezvani；原始项目采用 MIT 许可。王博负责按项目约束选型、中文入口、证据边界及 OpenSpec/dev 流程集成。固定版本、原始路径和修改见 UPSTREAM.json；原入口见 references/upstream-skill.md。

## 安装与使用

解压单项 ZIP，使用 `python install.py --dest "~/.agents/skills" --only tech-stack-evaluator`。Claude Code 可将目标改为 ~/.claude/skills，Codex 按其实际发现目录配置。开始新一轮对话后可显式调用 `$tech-stack-evaluator` 或 `/tech-stack-evaluator`。

示例：为一个带账号、订单和模型 API 的网站选择后端与关键库；读取项目约束、比较候选、引用当前官方资料、说明推荐理由及代价。

## 流程与运行条件

OpenSpec 规划时完成必要选型并记录在原设计位置；dev 实施时复用决定，新增关键库再补充调查。若只安装本技能，可通过技能描述自动选择或显式调用；整套分发中的相关入口已接入条件路由。全局主动触发规则见仓库 docs/technology-selection-integration.md，用户可按需要加入自己的 AGENTS.md/CLAUDE.md。

宿主需要文件读取和适用的当前资料检索能力。基本选型不要求执行 Python；保留的 Python 脚本仅按需计算，默认值与示例评分不能证明当前技术、安全、成本或维护状态。

## 来源与许可

上游：https://github.com/alirezarezvani/claude-skills/tree/27cfcd0fb0a41f60adffcbd5271fdf8839f86ed2/engineering-team/skills/tech-stack-evaluator 。保留 LICENSE、完整 scripts/references/assets，本站不替代原作者署名。

## 多维选型适配

明确每次覆盖开发速度、运行速度、资源性能、安全、生态、复用、库质量与有效供给等 14 维；先筛硬约束，再按项目优先级和证据取舍。 详见 [选型准则](references/evaluation-rubric.md) 与 [决策模板](references/decision-template.md)。原始上游资源和许可保留，主入口与本地准则决定实际工作流。
