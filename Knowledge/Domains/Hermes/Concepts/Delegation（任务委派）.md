---
name: Delegation（任务委派）
type: system
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Delegation（任务委派）

## 类型判定
系统型 — Delegation 是单父→多子的任务分发系统，与 Kanban 互补（Delegation=同步短任务，Kanban=异步长任务）。

## 是什么
Delegation（委派）让父 Agent 生成独立子 Agent 并行处理任务。每个子 Agent 拥有独立对话、独立终端环境，互不干扰。完成后只返回结构化摘要（`result` + `summary`），不回传完整对话——控制 token 开销。

## 输入-输出空间
**输入**：`delegate_task(goal="...", context="...", toolsets=[...])` 或批量 `tasks=[{goal, context}]`
**输出**：每个子 Agent 完成时，`result`（最终回答）+ `summary`（执行摘要）回传父对话

## 正例（≥2个）
- 并行研究：「调研 A 方案」+「调研 B 方案」→ 两个子 Agent 同时搜索 → 5 分钟后两份报告回来
- 委派修 Bug：父 Agent 诊断问题 → 委派子 Agent「修复 test_foo.py 的断言错误」→ 子 Agent 独立修→测→报告
- 实战篇案例：researcher Worker 内再委派 3 个子 Agent 分别搜索不同来源

## 反例/边界（≥1个）
- **子 Agent 不知道父对话的上下文**——必须通过 `context` 参数传递所有必要信息
- **叶子节点不能再委派**：默认 `max_spawn_depth: 1`，子 Agent 不能继续 delegate
- 子 Agent 不能：clarify（问用户）、memory（写记忆）、delegation（继续委派）、send_message（发消息）
- 批量最多 3 并发（`max_concurrent_children`），超出直接报错
- **非持久**：父进程退出 → 未完成的子 Agent 全部丢弃
- 适用于短任务（几分钟），长任务应改用 Kanban

## 详细解释
```yaml
# config.yaml
delegation:
  max_concurrent_children: 3     # 并行上限
  max_spawn_depth: 1             # 委派深度（1=不许嵌套）
  orchestrator_enabled: true     # 是否允许 orchestrator 角色
```

Delegation vs Kanban：
| 维度 | Delegation | Kanban |
|------|-----------|--------|
| 持久性 | 进程级，退出即丢 | SQLite 持久化 |
| 任务时长 | 几分钟 | 小时/天 |
| 并发数 | 默认 3 | 无硬上限 |
| 依赖关系 | 无 | 有（parent→child link） |
| 人类介入 | 否 | 支持（block/comment/unblock） |

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 工具限制 | 子 Agent 不能 clarify / memory / delegation / send_message |
| context 传递 | 子 Agent 只知道 goal + context，不知道父对话历史 |
| 非持久 | 父进程退出 → 未完成的子 Agent 被丢弃 |

### Delegation vs Kanban 选择
| 条件 | Delegation | Kanban |
|------|-----------|--------|
| 任务时长 | < 5 分钟 | > 5 分钟 |
| 跨运行持久 | 否 | 是 |
| 需人工介入 | 否 | 是 |
| 任务间有依赖 | 否 | 是 |
| 失败自动重试 | 否 | 是 |


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — 子 Agent 运行独立的 Agent Loop
- [[Profile（多实例）]] — 子 Agent 复用父 Agent 的 Profile

### ← 被指向
- [[Kanban Board（任务看板）]] — 互补关系：短任务 Delegation，长任务 Kanban