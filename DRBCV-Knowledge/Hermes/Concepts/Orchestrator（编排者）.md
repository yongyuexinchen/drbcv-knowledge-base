---
name: Orchestrator（编排者）
type: discriminant
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Orchestrator（编排者）

## 类型判定
判别型 — Orchestrator 是一种特殊的 Agent 角色：它只做拆解和汇总，不执行具体工作。区分于 Worker（执行者）。

## 是什么
Orchestrator 是 Kanban 工作流中的编排角色。它负责：(1) 接收 triage task → 判断是否需要拆分；(2) 扫描可用 Profile → 生成子 Task 图（含 assignee + 依赖关系）；(3) 子 Task 完成后 → 汇总结果 → 判断总目标是否完成。Orchestrator 不自己搞研究、写代码、写文章。

## 输入-输出空间
**输入**：triage task（高层目标描述）
**输出**：子 Task 图（多个 todo task + link 依赖关系）

## 正例（≥2个）
- 博客系统 Orchestrator：「写一篇关于 Hermes Swarm 的深度文章」→ 拆成 5 个子 Task：research×2 → write → review → publish
- 多项目编排：「重构用户系统」→ 拆成 backend API + frontend + test + deploy，分别指派不同 Profile
- auto_decompose：Orchestrator Profile 在 Dispatcher tick 时自动处理所有 triage task

## 反例/边界（≥1个）
- Orchestrator **不应该有执行工具**：应禁用 terminal、file、web、browser（只保留 kanban + memory）
- Orchestrator 不知道 Task 的具体执行细节——它只看子 Task 的 `kanban_complete(summary=...)` 摘要
- 如果 Orchestrator 自己下场干活 = 角色混乱 = 输出质量下降
- 必须有 `kanban.orchestrator_profile` 指向真实存在的 Profile

## 详细解释
Orchestrator Profile 配置：
```bash
hermes profile create orchestrator --clone --description "编排者，不执行具体任务"
orchestrator tools disable terminal file web browser code_execution
hermes config set kanban.orchestrator_profile orchestrator
hermes config set kanban.auto_decompose true
```

**约束原则**：
1. 只看 Profile 列表和 description → 路由给真实存在的 Profile
2. 不自己干活 → 工具集受限
3. 加载 `kanban-orchestrator` skill → 注入行为约束

## 细节备注

### 子特性
| 特性                   | 说明                                                    |
| -------------------- | ----------------------------------------------------- |
| auto_decompose       | kanban.auto_decompose: true -> tick 时自动处理 triage task |
| decompose vs specify | decompose=拆成子 task 图；specify=补全成明确 spec               |

### 推荐配置
```bash
hermes profile create orchestrator --clone
orchestrator tools disable terminal file web browser code_execution
hermes config set kanban.orchestrator_profile orchestrator
hermes config set kanban.auto_decompose true
```


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 属于 (is-a)
- [[Profile（多实例）]] — Orchestrator 是一种特殊 Profile

### 依赖 (depends-on)
- [[Kanban Board（任务看板）]] — 在 Board 上创建子 Task
- [[Task（Kanban 任务）]] — 创建 Task 图

### ← 被指向
- [[Kanban Swarm]] (implements) — Swarm 一键启动 Orchestrator 拓扑