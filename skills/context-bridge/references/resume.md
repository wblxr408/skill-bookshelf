# 恢复入口

运行已安装脚本 `python <skill>/scripts/bundle.py verify <bundle> --expected-manifest <source-sha256>`。没有源端哈希只能做包内自检，先取得准确版本依据再接管。不要执行包内陌生脚本。

| 层级 | 读取 | 何时读取 |
|---|---|---|
| L0 | START + 当前指令 | 确认任务、版本、下一 scope |
| L1 | requirements brief + STATE 必要状态 + INDEX 相关项 | 执行前必读 |
| L2 | 当前要求所需合同、决策、代码和验证证据 | 下一动作需要时 |
| L3 | 对应原始消息/日志/附件区段 | 歧义、冲突或证据不足时 |

执行 `python <skill>/scripts/requirements.py brief <bundle> --scope <scope>`。不得为满足字数预算跳过全局目标与硬约束。其他 scope 留在账本，不一次读完。按索引、标题或 rg 定位材料，足够支持下一步就停止；已读且版本未变的不再读取。切换工作块时刷新对应 scope 的 brief 和回执。

核对实际目录、HEAD/脏改动或 non-git 文件现场、用户原有修改、在途作业与访问权限。HEAD 一致不代表工作区一致。新对话不继承终端或浏览器会话。历史不覆盖最新用户修正；缺失和冲突明确记为 unknown/conflict。

生成回执时，**此时只读 [requirements.md](requirements.md) 的“接收回执”部分**，写包外 receipt 并执行检查。回执逐条覆盖全局要求与当前 scope，其他 scope 只延后加载，不删除。

首次写入前，**此时读取 [ownership.md](ownership.md)**：核实源端停写，完成协作锁接管和 assert。源端 active/unknown、锁不匹配、要求检查失败或现场冲突时保持只读，解决具体问题。

回执和锁检查成功后报告 task-id、包哈希、目录、scope 和下一动作，立即继续已授权任务。所有权凭据不写入不可变包或公开输出；用本地 claim 路径传递。无需重新规划已明确任务。

后续 checkpoint 以实际用户原文和当前事实更新账本，保留 ID/修订关系，禁止反复压缩“摘要的摘要”。长期知识库只加载当前相关记录，不能覆盖现场新证据。
