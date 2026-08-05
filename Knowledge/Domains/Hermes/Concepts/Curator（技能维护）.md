---
name: Curator（技能维护）
type: system
status: core
source: "[[Hermes教程-模块三-进化篇]]"
domain: hermes
---

# Curator（技能维护）

## 类型判定
系统型 — Curator 是 Skill 的后台生命周期管理系统：检测→过期→归档→合并→备份。

## 是什么
Curator 是 Hermes 的技能维护守护进程，自动管理 Agent 自建的本地 Skill。它跟踪每个 Skill 的使用频率，把长期闲置的 Skill 从 active → stale → archived（归档到 `.archive/`），合并重叠的 Skill，防止技能库无限膨胀占用 token。

## 输入-输出空间
**输入**：`~/.hermes/skills/` 中的 `created_by: "agent"` 技能 + 使用统计
**输出**：stale 标记、归档迁移、LLM Review 合并建议、备份

## 正例（≥2个）
- `tech-deep-dive-writing` 和 `blog-post-template` 重叠 → Curator 合并为 umbrella skill `writing/technical-blog`
- 30 天未使用的 `old-newsletter-format` → 自动标记 stale → 90 天归档
- Pinned 技能 `blog-kanban-workflow` → Curator 完全不碰

## 反例/边界（≥1个）
- **只处理 Agent 自建的 Skill**——用户手写的、Bundled 内置的、Hub 安装的都不碰
- Pinned 技能有三层保护：不自动迁移 + LLM Review 跳过 + `skill_manage delete` 也不能删
- Curator 自动运行需满足：enabled + 未 pause + 距上次运行超 `interval_hours`（默认 7 天）+ Agent 空闲超 `min_idle_hours`（默认 2 小时）
- 最大破坏性操作 = 归档（`.archive/`）——**从不删除**，始终可恢复

## 详细解释
两阶段执行：
1. **自动状态迁移**（不调用 LLM，免费）：`stale_after_days`(30天) 未使用 → stale；`archive_after_days`(90天) → 归档
2. **LLM Review**（可选，`consolidate: true` 开启）：辅助模型审查，决定保留/修补/合并/归档

配置：`curator.enabled`、`interval_hours`、`stale_after_days`、`archive_after_days`。可以用更便宜的模型：`auxiliary.curator.model: google/gemini-3-flash-preview`。

## 细节备注

### Pinned 三层保护
1. Curator 不自动迁移到 stale/archived
2. LLM Review 跳过
3. skill_manage delete 拒绝

### .usage.json 遥测
跟踪每个 Skill：use_count、view_count、patch_count、last_activity_at、state、pinned

### LLM Review
- 默认关闭（consolidate: false）→ 自动状态迁移不花钱
- 开启后调用辅助模型审查去重/合并
- 可指定便宜模型：auxiliary.curator.model: google/gemini-3-flash-preview


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Skill（技能系统）]] — Curator 管理 Skill 生命周期

### ← 被指向
- [[Agent Loop（Agent 循环）]] — Curator 防止 Skill 膨胀保护 token 预算