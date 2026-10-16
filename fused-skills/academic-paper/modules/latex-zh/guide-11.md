## Reference Map

- `references/COMPILATION.md`: compilation strategy and toolchain diagnosis（顶层概述；模块执行时读 `references/modules/COMPILE.md`）.
- `references/GB_STANDARD.md`: GB/T 7714 and bibliography-related checks.
- `references/STRUCTURE_GUIDE.md`: thesis structure expectations and chapter mapping.
- `references/LOGIC_COHERENCE.md`: logic, coherence, heading lead-ins, consistency, and literature-review expectations.
- `references/TITLE_OPTIMIZATION.md`: Chinese academic title heuristics.
- `references/DEAI_GUIDE.md`: de-AI review heuristics.
- `references/modules/EXPERIMENT.md`: experiment-chapter review criteria.
- `references/UNIVERSITIES/`: legacy school-by-school index, kept for backward compatibility.
- `templates/`: per-template snapshots loaded on demand. Files: `generic.md`, `thuthesis.md`, `pkuthss.md`.

只读取当前模块所需的参考文件，避免一次加载整套指南。
