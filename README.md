# Skill Bookshelf

这是一个个人 Codex skill 书橱：按稳定的目录名保存每个 skill 的 `SKILL.md`、脚本、模板和参考资料，方便检索、复用、版本管理与分享。

仓库聚焦于可直接放入 Codex skill 目录使用的工作流资产。每个子目录自包含其说明和所需资源；目录按名称排序，避免同一 skill 在不同位置出现不同版本。

## 本地全量书橱 · 已去重

书橱网站：https://bo-skill-bookshelf.vercel.app/ 。本次盘点 **288 份本地入口**、184 个名称，归并为 **163 个逻辑 Skill**，合并 125 份重复/兼容入口，并保留 218 个不同资源版本。

范围覆盖共享、Codex、Claude Code、插件目录（含缓存）及本项目；有文件不等于插件当前已启用。相同用途但没有充分归并依据的技能仍分开保留。同名和已确证的兼容/融合入口合为一张书卡，原名称仍可搜索。

- [逐项去重报告](docs/local-skill-dedup-report.md) · [全部记录与版本落点 JSON](docs/local-skill-dedup-report.json)
- [全部作者与来源](ATTRIBUTION.md) · [安装器和依赖清单](distribution/)
- [下载全部可分发主版本](https://bo-skill-bookshelf.vercel.app/downloads/bo-local-skills.zip)

主版本复用 `fused-skills/` 或保存于 `local-skills/`，不同资源来源保存在 `skill-versions/` 或已有 `skills/`。每项 `BOOKSHELF.md` / `BOOKSHELF.json` 记录安装、来源与此次分发适配；保留上游原始说明和许可。明确禁止再分发的 Niko 条目仍收录，链接现有来源，不加入下载包。

## 完整融合版 · 下载即用

线上书橱：https://bo-skill-bookshelf.vercel.app/ 。融合目录位于 [`fused-skills/`](fused-skills/)，保留完整脚本、参考资料、模板与模块。原 `skills/` 目录是较早的收录版本；安装时选择其中一个同名版本，避免重复启用。

- [下载整套 11 项 ZIP](https://bo-skill-bookshelf.vercel.app/downloads/bo-fused-skills.zip)
- [安装与使用说明](distribution/README.md)
- [原作者与来源总表](ATTRIBUTION.md)

| 完整融合版 | 主要个人改动 | 来源与具体差异 |
| --- | --- | --- |
| [impeccable](fused-skills/impeccable/) | 保留两个原始能力模块，使用短入口按需加载。 | [原作者](fused-skills/impeccable/ATTRIBUTION.md) · [修改记录](fused-skills/impeccable/CHANGES.md) |
| [paper-audit](fused-skills/paper-audit/) | 按快速审查、深度方法、投稿门槛与修订复核选择分支。 | [原作者](fused-skills/paper-audit/ATTRIBUTION.md) · [修改记录](fused-skills/paper-audit/CHANGES.md) |
| [academic-paper](fused-skills/academic-paper/) | 保留英文 TeX、中文学位论文和 Typst 的脚本与资料。 | [原作者](fused-skills/academic-paper/ATTRIBUTION.md) · [修改记录](fused-skills/academic-paper/CHANGES.md) |
| [scientific-data-visualization](fused-skills/scientific-data-visualization/) | 保留 reproducible 与 publication 两条绘图分支。 | [原作者](fused-skills/scientific-data-visualization/ATTRIBUTION.md) · [修改记录](fused-skills/scientific-data-visualization/CHANGES.md) |
| [dev](fused-skills/dev/) | 按任务选载技术指南，保留现有设计、记忆与连续性所有者。 | [原作者](fused-skills/dev/ATTRIBUTION.md) · [修改记录](fused-skills/dev/CHANGES.md) |
| [context-bridge](fused-skills/context-bridge/) | 按保存、恢复、任务状态分支渐进加载。 | [原作者](fused-skills/context-bridge/ATTRIBUTION.md) · [修改记录](fused-skills/context-bridge/CHANGES.md) |
| [agent-crosscheck](fused-skills/agent-crosscheck/) | 将目的、边界、代价与正确性放到同一审查入口。 | [原作者](fused-skills/agent-crosscheck/ATTRIBUTION.md) · [修改记录](fused-skills/agent-crosscheck/CHANGES.md) |
| [pdf](fused-skills/pdf/) | 按任务选择原生或便携处理模块。 | [原作者](fused-skills/pdf/ATTRIBUTION.md) · [修改记录](fused-skills/pdf/CHANGES.md) |
| [browser](fused-skills/browser/) | 已有页面和登录态优先 cua_repl。 | [原作者](fused-skills/browser/ATTRIBUTION.md) · [修改记录](fused-skills/browser/CHANGES.md) |
| [deep-research](fused-skills/deep-research/) | 研究入口负责检索、来源核验和综合。 | [原作者](fused-skills/deep-research/ATTRIBUTION.md) · [修改记录](fused-skills/deep-research/CHANGES.md) |
| [engineering-toolbox](fused-skills/engineering-toolbox/) | 以版本 2.2.3 的来源快照建立 311 项映射。 | [原作者](fused-skills/engineering-toolbox/ATTRIBUTION.md) · [修改记录](fused-skills/engineering-toolbox/CHANGES.md) |

每项完整目录附 README、ATTRIBUTION、CHANGES 和许可材料。单项包携带共享依赖，安装器默认拒绝覆盖，显式替换时保留备份。

## 个人自建好用技能

| Skill | 定位 |
| --- | --- |
| [project-index-router](skills/project-index-router/) | 在实施前定位最小且正确的项目文档集，减少无关阅读。 |
| [visual-style-router](skills/visual-style-router/) | 为图像和视觉表达任务选择合适的呈现风格。 |
| [context-bridge](skills/context-bridge/) | 为长任务建立可追溯检查点，并支持在新对话中继续工作。 |
| [scientific-data-visualization](skills/scientific-data-visualization/) | 科学数据可视化。 |

## 目录

所有 skill 均位于 [`skills/`](skills/)；下列目录按字母顺序排列。

| Skill | 方向 |
| --- | --- |
| [-21risk-automation](skills/-21risk-automation/) | 21risk 自动化 |
| [academic-paper](skills/academic-paper/) | 学术论文写作 |
| [academic-paper-reviewer](skills/academic-paper-reviewer/) | 学术论文评审 |
| [academic-pipeline](skills/academic-pipeline/) | 学术研究流水线 |
| [agent-crosscheck](skills/agent-crosscheck/) | 第二轮审查 |
| [algorithmic-art](skills/algorithmic-art/) | 算法艺术 |
| [all-images-ai-automation](skills/all-images-ai-automation/) | 图像服务自动化 |
| [bib-search-citation](skills/bib-search-citation/) | BibTeX 文献检索与引用 |
| [browser](skills/browser/) | 浏览器自动化 |
| [codeagent](skills/codeagent/) | 多后端代码代理 |
| [context-bridge](skills/context-bridge/) | 长任务上下文迁移 |
| [cover-letter](skills/cover-letter/) | 投稿附信 |
| [deep-research](skills/deep-research/) | 深度研究 |
| [dev](skills/dev/) | 端到端开发 |
| [do](skills/do/) | 结构化功能开发 |
| [engineering-memory](skills/engineering-memory/) | 工程经验记忆 |
| [frontend-design](skills/frontend-design/) | 前端界面设计 |
| [harness](skills/harness/) | 多会话代理编排 |
| [hatch-pet](skills/hatch-pet/) | Codex 动态宠物 |
| [intent-review](skills/intent-review/) | 意图与边界审查 |
| [latex-paper-en](skills/latex-paper-en/) | 英文学术论文 LaTeX |
| [latex-thesis-zh](skills/latex-thesis-zh/) | 中文学位论文 LaTeX |
| [lean-agent-harness](skills/lean-agent-harness/) | 精简代理指令 |
| [omo](skills/omo/) | 多代理代码工作流 |
| [one-day-prototype](skills/one-day-prototype/) | 一日原型 |
| [paper-audit](skills/paper-audit/) | 论文审计与投稿检查 |
| [pdf](skills/pdf/) | PDF 创建、阅读和审查 |
| [playwright](skills/playwright/) | Playwright 浏览器自动化 |
| [product-requirements](skills/product-requirements/) | 产品需求文档 |
| [project-index-router](skills/project-index-router/) | 项目索引路由 |
| [prototype-prompt-generator](skills/prototype-prompt-generator/) | UI/UX 原型提示词 |
| [scene-to-art-lab](skills/scene-to-art-lab/) | 实景艺术实验室 |
| [scientific-data-visualization](skills/scientific-data-visualization/) | 科学数据可视化 |
| [scipilot-figure-skill](skills/scipilot-figure-skill/) | 科研图表顾问 |
| [skill-install](skills/skill-install/) | Skill 安装 |
| [sparv](skills/sparv/) | SPARV 工作流 |
| [task-contract](skills/task-contract/) | 任务契约 |
| [task-lanes](skills/task-lanes/) | 任务分流 |
| [test-cases](skills/test-cases/) | 测试用例 |
| [typst-paper](skills/typst-paper/) | Typst 学术论文 |
| [visual-style-router](skills/visual-style-router/) | 视觉风格路由 |
| [workflow-skill-capture](skills/workflow-skill-capture/) | 工作流沉淀为 skill |

## 使用方式

将所需目录复制或链接到 Codex 的 skills 目录。进入某个 skill 后先阅读其 `SKILL.md`；它是该 skill 的使用入口和权威说明。

## 维护约定

- 一个 skill 一个目录，目录名保持稳定。
- 相关脚本、模板与参考资料跟随 skill 保存。
- 依赖安装产物和本地凭据不提交到仓库。

## 署名更正

`scene-to-art-lab` 的原作者为 **Niko**，不是王博的署名；按第三方收录处理，其个人非商业许可限制再分发。原作者来源与王博融合贡献分别保留，不将整套第三方资料统一改署名或改成 MIT。
