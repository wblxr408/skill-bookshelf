## 脚本说明

| 脚本 | 干啥 | 主入口 |
|---|---|---|
| `profile_data.py` | EDA：列类型 / 样本量 / 分布 / 异常 / 相关 / 初步图型建议 | `profile_data(source, group_cols)` |
| `setup_style.py` | 期刊预设 + CJK 字体配置 + SciencePlots 包装 | `setup_style(journal, lang, use_sciplots, serif_for_zh)` |
| `export_figure.py` | 多格式 + 按最终尺寸 + 灰度预览 | `export_figure(fig, basename, formats, dpi, size_inches, grayscale_preview)` |
| `check_figure.py` | 文件合规自检（格式 / DPI / 字体嵌入） | `check_figure(path, min_dpi, target_inches)` |
| `layout_tools.py` | 子图标签对齐 + constrained/tight 兜底理版 | `add_panel_labels(fig, style)` / `finalize_figure(fig)` |
| `visual_qa.py` | 渲染 PNG 预览 + 程序自检（缺字 / 裁切 / 刻度重叠） | `render_preview(fig, out)` / `audit_layout(fig)` |
