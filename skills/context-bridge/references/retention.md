# checkpoint 保留与回收：仅登记、规划清理或容量提醒时读取

## 保存时减少增长

只在有新的关键状态、迁移边界或风险证据时封包；同一状态不重复生成。普通进度更新写包外可变草稿，关键状态先落盘，不能为了省空间延迟必要 checkpoint。不要重复复制依赖目录、构建缓存和无关日志。

checkpoint 不可原地覆盖；新包完整保存自身恢复所需的原文和小型状态。大文件可以指向已有持久文件，但要记录路径、哈希及可访问性；外部文件不属于包内哈希保障。若恢复依赖旧包，必须登记 depends_on。来源追溯链接仅在原文已完整复制到新包且运行时不需要旧包时，才可视作非依赖。

本版本没有内容寻址的共享对象仓库；不会声称所有大文件只存一份。以后需要共享对象存储时必须同时实现引用追踪和垃圾回收，不能仅靠硬链接假装独立备份。

## 默认策略

- 每个任务最近 3 个非隔离版本；候选至少 7 天；移入隔离区后再等待 7 天。
- 额外保护 current、last_received、pinned、in_use、非 retired 版本，以及这些版本的全部传递依赖。
- retired 版本只有确认无读者、具备保留中的 self_contained 替代包、通过跨版本要求检查时才进入候选。
- 每任务默认软预算 512 MiB，包括已登记隔离包。超额只报告，不能越过保护规则强删。

参数是可调整的本地默认值，不是性能结论。未登记、校验失败、关系不完整或状态不明的目录全部保留。禁止扫描/删除其他会话、Git 历史、Basic Memory、工作树、锁文件或工作目录。

## 任务根目录登记

只管理一个明确任务的专用 checkpoint 根目录，包是该目录直接子目录。不要把整个项目、outputs 或个人技能目录作为管理根。在根目录创建包外 ".retention.json"，按实际证据维护：

```json
{
  "schema": 1,
  "task_id": "实际任务ID",
  "current": "cp-002",
  "last_received": "cp-002",
  "policy": {"keep_last": 3, "min_age_days": 7, "trash_days": 7, "budget_mib": 512},
  "items": [
    {"id": "cp-001", "manifest_sha256": "实际64位哈希", "created_utc": "2026-09-01T00:00:00+00:00", "lifecycle": "retired", "pinned": false, "in_use": false, "depends_on": [], "superseded_by": "cp-002", "no_readers_confirmed": true, "self_contained": true},
    {"id": "cp-002", "manifest_sha256": "实际64位哈希", "created_utc": "2026-09-10T00:00:00+00:00", "lifecycle": "received", "pinned": false, "in_use": true, "depends_on": [], "self_contained": true}
  ]
}
```

新包 lifecycle=active、in_use=true；真实 receipt 与锁接管成功后才能设 received / last_received。旧包只有核实读者停止、替代包完整且校验通过，才设 retired / no_readers_confirmed=true。不得为了让清单变小而虚报状态。current 和 last_received 可为 null（确实没有时）。self_contained 是恢复依赖审查的声明，脚本无法验证所有自然语言路径。不把“旧”自动等同于“可删”。

## 先规划，再执行

1. 停稳该任务的登记和清理写入。执行：
   `python <skill>/scripts/retention.py plan <absolute-task-root> --out <outside-plan.json>`
   命令只写清单，不移动或删除包。输出清单哈希、可回收量、隔离量、受保护/异常原因与软预算状态；无需读取包内全文。清单在根目录之外，避免混入登记。
2. 核对具体候选。用户已授权执行该保留策略时，直接执行；仅询问机制/创建技能不视为删除现有资料的授权。运行：
   `python <skill>/scripts/retention.py apply <absolute-task-root> --plan <outside-plan.json> --expected-plan <plan-sha256>`
   apply 要求精确清单哈希，重新读取登记、重新计算保护并校验候选；任何变化拒绝旧计划。quarantine 移入专用 .trash，不立即释放磁盘；只有已过隔离宽限期的 purge 才删除。
3. 清理按事件触发：成功接管后、任务结束或容量提示时规划；不创建定时器，不在每轮对话检查。默认仍是 plan，不擅自启用后台删除。

计划执行中断会保留 .retention.pending.json。发现它时停止继续清理，检查日志中源/目标实际位置与哈希后修复登记，再移走该中断标记保留审计副本；不得盲目重试、猜测移动完成或删除未知目录。脚本保留的 deleted 登记是小型追溯记录，不含原始大文件；大量历史任务的登记归档需要另外明确范围。

## 取回隔离包

隔离期内先停止清理，确认 .trash/<id> 哈希匹配、原路径不存在、目录没有链接；把该包移回同一任务根的 <id>，更新 lifecycle=retired、in_use=true 或 pinned=true 并去掉 trashed_utc。不要让接收端从待删除隔离路径继续任务。已 purge 的包只能从其他备份恢复。
