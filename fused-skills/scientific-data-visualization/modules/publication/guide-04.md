## 核心工作流（8 步）

**这是本技能与普通画图工具的根本区别——不能上来就画**。每一步缺位前一步的成果都不该执行。

### 第 0 步：理解任务

开画前**先搞清楚两件事**：

1. **这张图要论证什么观点 / 回答什么问题？** 同样数据，论点不同图就不同（详见 `references/chart_selection.md` 的"同一批数据、不同论点 → 不同图"小节）
2. **数据在哪里？长什么样？** 文件路径 / 字段含义 / 多少行 / 是否已经清洗

**如果用户没说清论证目标**，主动问一句："你这张图主要想说服读者相信什么？" 或从论文上下文推断并明确告诉用户你的假设。**不要默认"用户知道自己要什么"**。

### 第 1 步：剖析数据

调用 `scripts/profile_data.py`：

```bash
python scripts/profile_data.py data.csv --group group --group condition
```

输出包含：每列类型、样本量、缺失率、连续列的描述统计 + 偏度 + 异常值、分组样本量分布、相关性矩阵、初步图型建议。

不会读这份报告？查 `references/data_profiling.md`。

**重点核对**：
- 列类型识别对不对？（数字 ID 被认成 ordinal 是常见误判）
- 每组 n 是多少？小样本警告？
- 是否高度偏态？是否需要对数轴？

### 第 2 步：选图

**这是顾问职责的核心**。基于第 0、1 步的事实，查 `references/chart_selection.md` 的决策框架决定图型。要点：

- **给出推荐 + 简短理由 + 1-2 个备选**（不要只丢一个选择给用户）
- 如果数据维度过多（如分组组合 > 12）→ **明确建议拆图**，而不是硬塞
- 如果用户指定的图型**不适合数据**（如 n=5 要画均值柱）→ **善意指出问题并说明更好的选择**，让用户决定。详见下方"主动拦截"小节
- 如果数据特征意味着特殊处理（双峰分布、严重异常值、跨量级）→ 在选图建议里明确提及

### 第 3 步：查期刊规范

确定目标期刊后查 `references/journal_specs.md` 拿到：单/双栏宽（mm 与 inch）、字号、推荐字体、DPI、矢量格式偏好。

不知道目标期刊就问一句。"毕业论文 / 中文核心 / 英文 SCI / NeurIPS" 都对应不同规范。

### 第 4 步：配环境

```python
from setup_style import setup_style
setup_style(journal='nature', lang='en')             # 英文 Nature
setup_style(journal='general', lang='zh', serif_for_zh=True)   # 中文宋体混排
```

`SciencePlots` 装了自动用，没装回退到内置预设——不会因为缺它崩溃。

### 第 5 步：绘制

按 `references/plot_recipes.md` 对应章节的配方画。每节都有可直接复制的 Python 代码 + 常见坑。

画图时强制做到：
- `figsize=(目标宽, 目标高)` 单位英寸——直接定最终尺寸
- 用 `seaborn.color_palette('colorblind')` 或 Okabe-Ito + 冗余编码（不同线型/marker）
- 误差棒 / 阴影要在图注交代是 SD / SEM / 95% CI + n

### 第 6 步：自检闭环（机器 + AI 读图）

**三层都要过，缺一层都可能带病投稿**：

1. **语义层**：`references/viz_pitfalls.md` 18 条科研画图禁忌——图型/配色/误差是否踩坑
2. **形式层**：`references/publication_checklist.md` 形式合规（尺寸、DPI、字号、误差交代）
3. **视觉层（v2.1 新增）**：出图后**渲染 PNG → 程序自检 → AI 读图复核 → 回改**的闭环：
   - `visual_qa.render_preview(fig, 'figs/_preview.png')` 渲一张预览
   - `visual_qa.audit_layout(fig)` 程序抓**缺字乱码 / 文字裁切 / 刻度重叠**（确定性问题）
   - **用 `Read` 工具读这张 PNG**，对照 `references/visual_review.md` 的 8 项清单核对
     **图例压数据 / 子图标签对齐 / 配色灰度可分**（程序难判的感知问题）
   - 发现问题 → 按 `visual_review.md` 回改表改 → 重渲 → 再读，直到通过

任何一层不通过就回去改图。**矢量图的导出放在闭环通过之后**，把问题挡在投稿之前。

### 第 7 步：导出

```python
from export_figure import export_figure
export_figure(
    fig, basename='figs/fig1',
    formats=['pdf', 'svg', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,    # 自动出灰度版供色盲检查
)
```

最后跑一遍 `scripts/check_figure.py --strict` 机器审计。
