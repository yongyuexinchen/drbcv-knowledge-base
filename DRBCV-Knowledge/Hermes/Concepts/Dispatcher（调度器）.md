---
name: Dispatcher（调度器）
type: system
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Dispatcher（调度器）

## 类型判定
系统型 — Dispatcher 是 Kanban 的调度核心，负责四类动作的循环执行：回收、推进、认领、启动。

## 是什么
Dispatcher 是 Kanban Board 的后台循环进程，默认每 60 秒 tick 一次。每次 tick 执行四步：(1) stale recovery — 回收崩溃/超时的 running task；(2) recompute ready — 检查依赖满足的 todo task 并推进；(3) atomic claim — 通过 CAS SQL 更新认领 ready task；(4) spawn worker — 启动 assignee Profile 进程执行 task。

## 输入-输出空间
**输入**：Board 状态变化（新 task 创建、依赖满足、运行超时）
**输出**：Task 状态推进 + Worker 进程启动

## 正例（≥2个）
- 两个 researcher task 都 done → Dispatcher 检测到依赖满足 → 推进 writer task 到 ready → 认领 → 启动
- Worker 进程崩溃 → Dispatcher 检测 `claim_expires` 过期 → 回收 task 回 ready → 下次 tick 重新认领
- 连续失败 2 次 → Dispatcher 自动 block task → 等人工介入

## 反例/边界（≥1个）
- 默认 60s tick：不是实时系统，新 task 最多等 60s 才被处理
- CAS 认领的原子性：`UPDATE tasks SET status='running', claim_lock=? WHERE status='ready' AND claim_lock IS NULL` — 命中 0 行 = 已被其他调度器认领
- 默认运行在 Gateway 内部（`kanban.dispatch_in_gateway: true`），不需要单独进程
- `consecutive_failures >= max_retries` → 自动 block，不会无限重试

## 详细解释
```sql
-- CAS 认领：Update 命中 1 行 = 成功；0 行 = 已被抢
UPDATE tasks
   SET status = 'running',
       claim_lock = '<lock_id>',
       claim_expires = '<expire_time>'
 WHERE id = ?
   AND status = 'ready'
   AND claim_lock IS NULL;
```

失败自动处理：`failure_limit`（默认 2，可配 `kanban.failure_limit` 或在 task 上设 `max_retries`）。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| stale recovery | claim_expires 过期的 running task -> 回收 -> 重置为 ready |
| tick 间隔 | 默认 60 秒 |
| dispatch_in_gateway | 默认 true -> Dispatcher 在 Gateway 进程内运行 |

### CAS 认领 SQL
```sql
UPDATE tasks SET status='running', claim_lock=?, claim_expires=?
WHERE id=? AND status='ready' AND claim_lock IS NULL
```
命中 1 行 = 认领成功；命中 0 行 = 已被其他调度器认领


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 组成 (part-of)
- [[Kanban Board（任务看板）]]

### 依赖 (depends-on)
- [[Task（Kanban 任务）]] — 推进 Task 状态
- [[Profile（多实例）]] — 启动指定 Profile 的 Worker

### ← 被指向
- [[Gateway（消息网关）]] (depends-on) — Dispatcher 默认运行在 Gateway 内