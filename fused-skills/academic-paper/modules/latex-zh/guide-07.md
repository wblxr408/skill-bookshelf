## Required Inputs

- 论文入口文件，例如 `main.tex`。
- 可选 `--section SECTION`，当用户只关注某一章或某一节。
- 可选 bibliography 路径，当任务聚焦参考文献。
- 可选学校/模板上下文，当用户关心 `thuthesis`、`pkuthss` 或特定高校要求。

如果参数不完整，保留已推断出的模块，只追问缺失的入口 `.tex` 文件、section、bibliography 路径或学校/模板上下文，不额外扩展问题。
