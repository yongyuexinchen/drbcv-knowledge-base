---
name: Workspace（工作目录）
type: discriminant
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Workspace（工作目录）

## 类型判定
判别型 — 区分三种 task 执行环境的隔离模式：scratch（临时）、dir（持久）、worktree（Git 分支）。

## 是什么
Workspace 是 Kanban Task 绑定的工作目录，Worker 启动后在此目录执行。三种模式：`scratch`（自动创建临时目录，用完可删）、`dir:<path>`（指定已有目录，持久化）、`worktree`（Git worktree，代码任务专用，避免冲突）。

## 输入-输出空间
**输入**：Task 的 `workspace_kind` + `workspace_path`
**输出**：Worker 进程的 `HERMES_KANBAN_WORKSPACE` 环境变量指向此目录

## 正例（≥2个）
- 研究任务 → `scratch`：临时目录，研究完就清理
- 博客写作 → `dir:/home/user/blog-repo`：已有仓库，writer 直接编辑草稿
- 代码修复 → `worktree`：独立的 Git worktree，修完可以单独提交

## 反例/边界（≥1个）
- scratch 目录在 task done/archived 后**不会自动清理**——需要 `hermes kanban gc` 手动清理
- dir 模式下如果路径不存在 → Worker 启动失败
- 多 Task 共用 dir → 可能冲突，需要自行协调
- Tenant 影响 Workspace 路径：不同 tenant 的 task 默认隔离到不同子目录

## 详细解释
三种模式对比：
| 模式 | 路径 | 持久性 | 隔离性 | 适用 |
|------|------|--------|--------|------|
| scratch | Board 的 `workspaces/<task_id>/` | 用完可删 | 完全隔离 | 调研、临时分析 |
| dir | 用户指定的绝对路径 | 持久 | 可共享 | 写作、已有项目 |
| worktree | Git repo 的独立分支 | 持久 | 完全隔离 | 代码修改 |

Workspace 通过 `HERMES_KANBAN_WORKSPACE` 环境变量注入 Worker 进程，Worker 在内部用 `cd` 或直接引用此路径。

## 细节备注

### 三种模式对比
| 模式 | 路径 | 持久性 | GC |
|------|------|--------|-----|
| scratch | Board 自动创建临时目录 | task done 后可删 | hermes kanban gc |
| dir:<path> | 用户指定已有目录 | 持久 | 不自动清理 |
| worktree | Git repo 独立分支 | 持久 | 手动删分支 |

### 使用原则
- 调研/分析 -> scratch
- 写作/已有项目 -> dir
- 代码修改 -> worktree（避免主分支污染）


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 组成 (part-of)
- [[Task（Kanban 任务）]] — 每个 Task 绑定一个 workspace

### ← 被指向
- [[Kanban Board（任务看板）]] (depends-on) — Board 管理 workspace 的创建和 gc
- [[Tenant（多租户）]] (depends-on) — Tenant 影响 workspace 路径隔离