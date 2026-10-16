## 中文支持

中文 matplotlib 出方框的根本原因：默认字体（DejaVu Sans 等）不含 CJK 字符表。`setup_style(lang='zh')` 自动做两件事：

1. 按优先级查中文字体：`Noto Sans CJK SC` > `Source Han Sans SC` > `SimHei` > `Microsoft YaHei`
2. 修负号方框：`plt.rcParams['axes.unicode_minus'] = False`

找不到任何 CJK 字体会抛清晰的安装提示（不会让你画完发现是方框）。

**中文期刊的"宋体 + 数字 Times New Roman"混排**：传 `serif_for_zh=True`，优先选 Noto Serif CJK / Source Han Serif / SimSun。

详见 `references/journal_specs.md` 末尾的字体安装小节。
