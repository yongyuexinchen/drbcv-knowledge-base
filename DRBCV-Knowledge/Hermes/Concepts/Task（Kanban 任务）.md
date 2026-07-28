---
name: Task（Kanban 任务）
type: discriminant
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Task（Kanban 任务）

## 类型判定
判别型 — Task 是 Kanban 的最小工作单元，通过九种状态严格区分当前进度。

## 是什么
Task 是 Kanban Board 上的一个工作条目。包含 title、body、assignee（指派给哪个 Profile）、priority、workspace（工作目录）、claim_lock（并发锁）、状态和依赖关系。

## 输入-输出空间
**输入**：`hermes kanban create "任务标题" --assignee <profile>`
**输出**：Task 在 Board 上经历九态流转，最终 done/archived

## 正例（≥2个）
- 研究任务：`title="调研 Hermes Swarm 架构" assignee=researcher workspace=scratch` → 进入 ready → running → done
- 写作任务：`title="撰写深度文章" assignee=writer depends_on=[task_1, task_2]` → 等两个父 Task 都 done 后才 ready
- 人工审批任务：reviewer 执行中途发现问题 → `kanban_block(reason="代码示例缺错误处理")` → 人工修→unblock→继续

## 反例/边界（≥1个）
- `triage` 态只是粗糙想法，不是可直接执行的任务——必须经过 decompose 拆成 `todo` 子任务
- `todo → ready` 需要所有父 Task done/archived——只要有一个父 Task 还在 running，子 Task 就永远是 todo
- `claim_lock` 是原子 CAS 更新——同一 Task 不能同时被两个 Worker 认领
- `consecutive_failures` 超 `max_retries` → 自动 block，不会无限重试

## 详细解释
九态流转：
```
triage → todo → ready → running → done
                      ↓        ↓
                   (blocked)  (crashed/timeout)
                      ↓        ↓
                   unblock → ready（重新入队）
```

关键字段：`title`、`body`、`assignee`、`priority`、`workspace_kind`（scratch/dir/worktree）、`workspace_path`、`claim_lock`、`consecutive_failures`、`max_retries`。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| claim_lock CAS | UPDATE WHERE status=ready AND claim_lock IS NULL → 防止重复认领 |
| consecutive_failures | 连续失败超 max_retries（默认 2）→ 自动 block |
| Tenant | 可选命名空间 → 隔离 workspace 路径和记忆 key |

### Link 依赖规则
- parent_id -> child_id：父未 done/archived 时子永远 todo
- 支持 fan-out（一父多子）和 fan-in（多父一子）
- 所有父 done -> Dispatcher 自动推进子到 ready


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 组成 (part-of)
- [[Kanban Board（任务看板）]]

### 依赖 (depends-on)
- [[Workspace（工作目录）]] — 每个 Task 绑定一个 workspace
- [[Profile（多实例）]] — assignee 指向特定 Profile

### ← 被指向
- [[Dispatcher（调度器）]] (depends-on) — 推进 Task 状态
- [[Orchestrator（编排者）]] (depends-on) — 创建 Task 依赖图