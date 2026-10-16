## Workflow

1. Parse `$ARGUMENTS`，先锁定入口文件，再根据用户诉求推断模块；若缺参数，只追问缺失项。
2. 若请求同时覆盖多个兼容模块，按“路由规则”中的顺序串行执行，并分模块回报结果。
3. Read the one reference file tied to that module (see "Read next" column).
4. Run the corresponding script with `uv run python ...`.
5. Return findings as `% Module (L##) [Severity] [Priority]: ...`. Report exact command and exit code on failure.
6. If template and structure are both unclear, run `template` first, then `structure`.
