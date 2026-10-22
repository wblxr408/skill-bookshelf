# 王博的本地全量 Skill 分发包

本包包含完整 Skill 源文件、脚本、参考资料、模板、来源说明和必要的共享 Skill 依赖。各技能 README 列使用示例与运行依赖；ATTRIBUTION.md 和 CHANGES.md 区分原作者与王博的融合修改。原始许可保留在模块及 licenses 中，不能将整个集合笼统视为 MIT。

## 安装

安装器需要 Python 3.9+，仅使用标准库。解压 ZIP 后进入包含 install.py 的目录。Windows PowerShell：

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills"
```

macOS / Linux：

```sh
python3 install.py --dest "$HOME/.agents/skills"
```

Claude Code 使用 `~/.claude/skills`；Codex 可使用其实际发现的 `~/.agents/skills` 或配置的 `~/.codex/skills`。以客户端当前配置为准。安装后重新打开会话，Codex 显式调用 `$skill-name`，Claude Code 调用 `/skill-name`。

## 只装某一项

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills" --only engineering-toolbox
```

安装器根据清单同时安装共享依赖。默认拒绝覆盖所有冲突项，拒绝时不会改写已安装的 Skill。确需替换时加 `--replace`：先将已有目录移到目标下 `.bo-backups/<时间>/`，再安装新版本；输出中包含备份位置。

单项包已带必要依赖，因此它不一定只含一个 Skill。整套包含 163 个可分发主版本，论文关联入口存在相互引用，安装器会去重并处理循环引用。

## 手动安装与源码

手动复制 `skills/` 内的所有目录到目标 skills 目录，保留目录名和相邻关系。不要只复制 SKILL.md。安装目录只能保留一份希望启用的同名入口，避免仓库旧版和融合版同时被发现。

Git 源码及全量去重报告位于 https://github.com/wblxr408/skill-bookshelf ，主版本见 fused-skills / local-skills，独立来源版本见 skill-versions 。从仓库构建 ZIP：`python tools/build_downloads.py --out <输出目录>`。ZIP 根目录中的 install.py 为同仓库 distribution/install.py 的副本。

此包不包含 API 密钥、用户会话、模型、TeX/Typst/Poppler 等系统工具或 node_modules。使用到对应操作时，按各项 README 安装具体依赖。未宣称所有外部工具和来源能力已在你的环境中运行验证。

## 去重规则与状态

291 份已记录入口归并为 164 个逻辑项；1 项依据已知原许可只保留来源入口。不同资源版本在源码仓库保留，ZIP 默认提供各项主版本。插件目录可能含缓存，使用仍需对应宿主和连接器。以网页和 manifest.json 的实际清单为准。
