## Connection fallback

If native tools are absent or fail to connect, automatically use the read-only fallback through the same configured Basic Memory MCP:
`& '~\AppData\Roaming\uv\tools\basic-memory\Scripts\python.exe' '~\.codex\bin\basic-memory-query.py' --query 'relevant keywords' --project main`
Use `--identifier 'permalink'` to read a note, `--search-type title` for full-title search, or `--health` for diagnosis. The helper has bounded timeouts and retries a transient transport failure once. If it also fails, report the limitation briefly and stop repeated connection attempts for this task until recovery evidence, a meaningful environment change, or an explicit retry request occurs. Continue independent work using current evidence; do not invent historical facts or claim retrieval succeeded. When a decision depends on unavailable history, state that uncertainty. Connection diagnosis requested by the user may make targeted recovery attempts.

当前增强入口与证据边界见 [enhanced-memory.md](enhanced-memory.md)。


## 2026-10-15：运行环境与错误证据

Codex 的 `mcp_servers.basic-memory.command` 必须指向安装器使用的 Basic Memory 专用 Python：`~/AppData/Roaming/uv/tools/basic-memory/Scripts/python.exe`。查询脚本自身读取此配置并启动服务，故仅更换调用查询脚本的解释器不足以修复错误服务环境。

本次 Anaconda 启动桥接器时缺少 fastembed，在握手前退出。新查询入口会报告非零退出码和有界脱敏 stderr；确定的进程失败不再按短暂 EOF 重试。不得仅以 stdout closed 推断网络波动，也不应自动关闭模型来掩盖依赖问题。

连接修复后须执行实际 main 检索和中文笔记读取；不要用握手或工具目录代替业务证据。已打开聊天的工具目录可能仍缓存失败，独立 MCP 调用成功不表示该聊天目录已刷新；可在当前聊天继续用同一配置的只读入口，新聊天由宿主重新初始化。
