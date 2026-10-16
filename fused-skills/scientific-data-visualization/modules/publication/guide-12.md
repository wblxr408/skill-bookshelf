## 依赖

```
matplotlib>=3.7
seaborn>=0.13
plotly>=5.18
pandas>=2.0
numpy>=1.24
scipy>=1.10            # profile_data 的偏度计算用到
Pillow>=10.0           # check_figure / grayscale preview
SciencePlots>=2.1      # 可选；装了样式更接近期刊
pypdf>=4.0             # 可选；check_figure 字体嵌入检查
kaleido>=0.2.1         # 可选；plotly 导出 PDF/PNG
```

可选依赖缺失时本技能仍能跑——会优雅降级并提示。
