## 常见任务示例

### 任务 A：用户只丢一个 CSV 说"帮我把这个画成论文图"

**思考-绘制工作流的范例**：

1. **第 0 步**：问用户"你这份数据主要想说服读者相信什么？"——是组间差异？时间趋势？变量关系？
2. **第 1 步**：跑 `python scripts/profile_data.py data.csv` 得到剖析报告
3. **第 2 步**：读报告里"列类型 + 样本量 + 分组结构"，结合用户的论证目标查 `chart_selection.md` 决策。**主动给出推荐 + 理由 + 1-2 备选**
4. **拿到用户确认后**进入第 3-7 步：查期刊规范、配环境、画、自检、导出

不要跳过任何一步。

### 任务 B：用户说"我想用柱状图展示三组各 5 个样本的均值"

**主动拦截的范例**：

```
你要的"三组各 5 个样本均值柱状图"会触发科研画图的经典 P1 错误
（参见 viz_pitfalls.md）——n=5 太小，柱状图的高度 + 一根误差棒无法
告诉读者数据真实分布。审稿人看到很可能要求"show individual data points"。

我建议改成 **箱线图 + stripplot 叠加每个点**：5 个点直接可见，
不掩盖任何信息，反而更可信。代码也只多一行。

要按原方案画，还是改成箱线+stripplot？
```

如果用户坚持要柱状，那也照做——但**至少**强制叠加 stripplot 显示每个点。

### 任务 C：多面板组合图

用户："给我画一个 Figure 1：4 个 panel，分别是 PCA、loss 曲线、混淆矩阵、生存曲线。"

流程：
1. 确认目标期刊（决定整张图 7.2 in 还是 7.16 in；Nature `a/b/c` vs IEEE `(a)(b)(c)`）
2. 各 panel 独立画，**保证字号、配色、坐标尺度统一**（同一变量在 4 个 panel 里同色）
3. 用 `plt.subplots(2, 2, figsize=(7.2, 5.4))` 组合（`setup_style` 已默认开 constrained_layout）
4. `layout_tools.finalize_figure(fig)` 理顺版面，再 `add_panel_labels(fig, style='nature')` 打 a/b/c/d——**统一 figure 坐标自动横竖对齐**，不要手摆 `ax.text`（易错位，见 viz_pitfalls P18；IEEE 用 `style='ieee'` → (a)(b)(c)）
5. **视觉自检闭环**：`render_preview` 渲 PNG → `audit_layout` 程序自检 → `Read` 读图核对子图对齐/遮盖 → 回改 → 通过后再导出 + 灰度检查

详细配方见 `plot_recipes.md` 第 9 节。

### 任务 D：带显著性标注的统计图

用户："3 组数据，箱线图加显著性标注。"

流程：
1. profile 确认 n（n<10 → 必须叠 stripplot）
2. 跑统计检验（**用户必须告知**用了什么检验，是否多重比较校正）
3. 画箱线 + stripplot
4. 用 `matplotlib.lines.Line2D` 或 `statannotations` 在组之间画显著性桥
5. **图注必须写**：误差类型 / n / 检验方法 / 校正 / 符号含义

配方见 `plot_recipes.md` 第 4 节。
