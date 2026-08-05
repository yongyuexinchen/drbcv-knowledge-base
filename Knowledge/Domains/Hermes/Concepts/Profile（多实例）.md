---
name: Profile（多实例）
type: system
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Profile（多实例）

## 类型判定
系统型 — Profile 是一个完整的 Agent 实例的配置/状态隔离系统，多 Profile = 多 Agent 团队。

## 是什么
Profile 是 Hermes 的实例隔离机制。每个 Profile 拥有独立的 `config.yaml`、`.env`、`SOUL.md`、`memories/`、`skills/`、`sessions/`——本质上是独立人格 + 独立记忆 + 独立工具的完整 Agent。创建 Profile 后自动生成同名命令别名（如 `coder chat`）。

## 输入-输出空间
**输入**：`hermes profile create <name> --description "..."` → 在 `~/.hermes/profiles/<name>/` 创建完整目录
**输出**：`<name> chat`、`<name> config set ...`、`<name> gateway start` 等别名命令

## 正例（≥2个）
- 博客系统的四个角色：`researcher`（DeepSeek、限 web 工具）、`writer`（Claude、限终端+文件）、`reviewer`（Claude、限文件）、`publisher`（限 terminal+git）
- 程序员助手：`coder` Profile（terminal+file+web）→ `coder chat` 专门写代码；`writer` Profile（Claude）→ 写文档
- Gateway 接入：每个 Profile 可以独立启动一个 Gateway，有独立的 bot token

## 反例/边界（≥1个）
- Profile 之间的技能和记忆是**完全隔离**的——researcher 学会的技巧 writer 不知道（除非共享外部技能目录）
- 最多 1 个 Profile 同时设为默认（`hermes profile use <name>`）
- 克隆时可选范围：`--clone`（只复制 config+.env+SOUL.md）、`--clone-all`（全量复制包括记忆）

## 详细解释
Profile 工作原理：别名命令在启动前设置 `HERMES_HOME=~/.hermes/profiles/<name>`，之后所有文件读写都在这个隔离目录内。

```bash
hermes profile create coder --description "写代码的 Agent"
# 生成别名 → 可以直接用：
coder chat       # 等价于 hermes -p coder chat
coder model      # 选择 coder 的模型
```

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 别名命令 | 创建 coder → 自动生成 coder chat、coder gateway start 等 |
| HERMES_HOME 隔离 | 每个 Profile 根目录 = ~/.hermes/profiles/<name>/ |
| Gateway 独立 | 每个 Profile 可启动自己的 Gateway + 独立 bot token |

### 克隆选项
| 参数 | 复制内容 |
|------|---------|
| 默认 | 空白 Profile，仅初始化内置 Skill |
| --clone | config.yaml + .env + SOUL.md |
| --clone-all | 完整状态（含记忆、会话、技能） |
| --clone-from NAME | 从指定 Profile 克隆 |


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### ← 被指向
- [[Kanban Board（任务看板）]] (depends-on) — Board 把 task 指派给特定 Profile
- [[Delegation（任务委派）]] (depends-on) — 委派启动的目标是一个 Profile
- [[Orchestrator（编排者）]] (is-a) — Orchestrator 是一种特殊 Profile