---
name: Kanban Board（任务看板）
type: system
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Kanban Board（任务看板）

## 类型判定
系统型 — Kanban Board 是 Hermes 的多 Agent 协作基础设施：持久化 SQLite 工作队列 + 调度器 + Worker 执行的三层架构。

## 是什么
Kanban 是 Hermes 的多 Agent 协作层。它把 Task（任务）、Link（依赖）、Comment（评论/交接）、Workspace（工作目录）和 Dispatcher（调度器）放进一个持久的 SQLite 看板里，让多个 Profile 以异步方式协作——比 Delegation 更强：跨运行持久、有依赖关系、支持人工介入。

## 输入-输出空间
**输入**：用户或 Agent 创建 Task → Orchestrator 拆解为子 Task 图（link 依赖）→ Dispatcher 推进
**输出**：各 Worker 依次完成子 Task → 最终 Task 完成 → result/summary 写入 Board

## 正例（≥2个）
- 博客自动发布系统：选题→研究→撰写→审核→发布，五个 Profile 依次执行，审核阶段人工介入
- 多项目并行：一个 Board 里同时跑 Blog 流水线 + Code Review 流水线 + 日报流水线
- Kanban Swarm：一条命令自动创建 researcher×2 + writer + reviewer + publisher 的完整拓扑

## 反例/边界（≥1个）
- Board 之间是**硬隔离**——不同 Board 的 Task 互不可见
- 不是实时系统：Dispatcher 默认每 60s tick 一次
- Worker 崩溃/超时后 Dispatcher 自动回收（stale recovery）→ 连续失败超限自动 block → 等人工介入

## 详细解释
三层架构：
```
Control Plane：CLI / Gateway / Dashboard → 用户指令入口
State Plane：SQLite + Dispatcher → 任务状态 + 调度
Execution Plane：独立 Profile Worker → 执行

所有协调通过 Board 流转，Worker 之间无直接通信。
```

六种协作模式：
| 模式 | 说明 | 场景 |
|------|------|------|
| Fan-out | 一拆多并行 | 多角度研究 |
| Pipeline | 上下游流水线 | researcher→writer→reviewer |
| Fan-in | 多汇总到一 | 研究综合 |
| Long-running journal | 定时任务 + 共享 workspace | 日报周报 |
| Human-in-the-loop | block→人工→unblock | 需要审批 |
| Fleet farming | 一个 Profile 管 N 个对象 | 多服务器巡检 |

## 细节备注

### 六种协作模式速查
| 模式 | 结构 | 场景 |
|------|------|------|
| Fan-out | 1->N 并行 | 多角度调研 |
| Pipeline | A->B->C 串行 | 研究->写作->审核 |
| Fan-in | N->1 汇总 | 研究综合 |
| Long-running journal | 定时重复+共享 workspace | 日报/周报 |
| Human-in-the-loop | block->人工->unblock | 需要审批 |
| Fleet farming | 1 Profile->N 对象 | 多服务器巡检 |

### 并发安全
- SQLite WAL 模式：并发读取 + 单个写入
- claim_lock CAS 更新：防止同一 task 被两个 worker 认领
- Board 之间硬隔离：不同 Board 的 Task 互不可见


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Profile（多实例）]] — Worker 是独立的 Profile 进程
- [[Task（Kanban 任务）]] — Board 的基本单元
- [[Dispatcher（调度器）]] — Board 的调度核心

### ← 被指向
- [[Delegation（任务委派）]] — 互补：Delegation=短同步，Kanban=长异步
- [[Orchestrator（编排者）]] (depends-on) — Orchestrator 操作 Board 拆解任务