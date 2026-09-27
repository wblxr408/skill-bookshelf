# checkpoint 制作入口

checkpoint 保存任务上下文；Git 保存已提交代码。没有 Git 也能交接。有 Git 时记录仓库、分支、HEAD、暂存/未暂存改动、未跟踪及必要的忽略文件。HEAD 无法恢复未提交工作；跨目录迁移时保存所需文件副本或可恢复补丁并验证。不得仅为迁移自动 commit、stash、reset 或清理工作树。

使用任务可访问的持久目录，遵守宿主 outputs/work 约定。每个包使用新 task-id/UTC-id 目录，旧包不覆盖。

| 文件 | 用途 |
|---|---|
| START.md | 目标、当前阶段、下一工作块 scope、包版本、恢复入口 |
| STATE.md | 决策原因、完成/未完成、验证、现场、在途操作、授权范围 |
| INDEX.md | 材料 ID、路径、定位符、版本、加载条件和依赖 |
| requirements.json | 带版本和原文依据的要求账本 |
| evidence/ | 关键原文、必要附件及易变证据副本 |
| manifest.json | 封包时生成的字节校验表 |

按步骤加载，不预读后续说明：

1. 写 START / STATE / INDEX。STATE 包含实际目录、Git 状态或 non-git、用户原有改动、运行作业及重连办法、关键决定与理由、失败尝试与前提、验证结果、未完成项。区分 verified / inferred / unknown。记录原始聊天与附件覆盖缺口，不把摘要称为全文备份。重要外部引用需要快照才被包内哈希保护。
2. **现在仅加载 [requirements.md](requirements.md)**：编写要求账本、对照可见用户指令核对覆盖、运行检查。全局目标与硬约束常驻，其他要求按 scope 分块。保留明确原文，不保存隐藏推理。
3. 仅保存 checkpoint 且继续源端工作：记录 source_writer=active；该包可供检查但不能直接接管。需要迁移或其他对话可能写同一目录时，**此时加载 [ownership.md](ownership.md)**，取得协作锁、完成在途写入并记录 source_writer=quiesced。锁文件放工作目录，不能放进不可变包。
4. 内容不再变化后执行 `python <skill>/scripts/bundle.py seal <bundle>`，再运行 `verify <bundle> --expected-manifest <返回的sha256>`。内容变化就另建版本并注明 supersedes；不覆盖 manifest 掩盖变化。
5. 写恢复提示：task-id、绝对包路径、manifest 哈希、原工作目录、下一工作块 scope。只有用户明确要求新建对话时，**此时读取 [dispatch.md](dispatch.md)**。否则提供恢复入口并继续当前授权工作。

脚本失败先修正明确问题，不通过缩减要求、删证据或修改旧哈希绕过校验。尚未交接的包不能宣称迁移完成。

封包完成后若启用 checkpoint 生命周期管理，或用户要求控制空间，此时才读 [retention.md](retention.md)。登记新包并更新当前指针；不要直接覆盖或删除旧版本。未启用时无需加载清理规则。
