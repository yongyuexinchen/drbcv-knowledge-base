---
name: Hermes Architecture（Hermes 核心架构）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: hermes
---

# Hermes Architecture（Hermes 核心架构）

## 类型判定
系统型 — 这是 Hermes 的"操作系统"级全景，定义了模块边界、分层关系和外部执行器的接入方式。

## 是什么
Hermes 定位为 **Personal Cognitive Operating System（个人认知操作系统）**。它不是聊天机器人，而是以长期记忆、知识管理、Skill 系统和 Agent 调度为核心的认知基础设施。外部编码代理（Grok Build、Codex、Claude Code）作为可插拔的"执行器"接入。

## 输入-输出空间
- **输入**：用户意图（自然语言，多渠道：桌面客户端 / Telegram / Discord）
- **输出**：执行结果 + 耐久记忆沉淀 + 知识库更新

## 正例（≥2个）
1. **编码**："写一个爬虫" → Gateway 接收 → Planner 分类为 execution → Skill Router 加载 `grok-build` → Grok CLI 执行 → Memory 写入
2. **写作**："写一篇深度文章" → Planner 分类为 creative → Router 匹配博客 Skill → Kanban 创建任务 → Orchestrator→Researcher→Writer→Reviewer→Publisher
3. **记忆查询**："我们上次讨论的 RAG 方案是什么？" → session_search 检索 → 返回上下文

## 反例/边界（≥1个）
- Hermes **不做代码执行**——那是 Grok/Codex/Claude Code 的事
- Hermes **不替代 Obsidian**——它同步 Obsidian，但 Obsidian 是独立的笔记工具
- Hermes **不是"一个大模型+工具"**——它是模块化的 Agent 调度系统

## 详细解释
```
                         ┌─────────────────────────┐
                         │     Hermes Gateway       │  ← 多端接入 (TG/DC/Desktop)
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │       Planner            │  ← 战略层 (做什么)
                         └───────────┬─────────────┘
                                     │
                      ┌──────────────┼──────────────┐
                      ▼              ▼              ▼
               ┌──────────┐  ┌──────────┐  ┌──────────┐
               │ Skill    │  │ Skill    │  │ Skill    │
               │ research │  │ coding   │  │ creative │
               └────┬─────┘  └────┬─────┘  └────┬─────┘
                    │              │              │
                    ▼              ▼              ▼
              SciSpace/     Grok Build/     Kanban Swarm
               RAG          Codex/Claude    (多Agent)
         ┌──────────────────────────────────────────────┐
         │              Hermes Memory + Knowledge        │
         │          (SQLite + Obsidian 同步)              │
         └──────────────────────────────────────────────┘
```

## 细节备注

### 核心模块
| 模块 | 职责 | 类比 |
|------|------|------|
| Memory | 长期记忆、偏好、教训 | Linux 文件系统 |
| Knowledge Base | DRBCV 知识卡片、Obsidian 同步 | 数据库 |
| Skill System | 可复用工作流程 | 应用程序 |
| Planner | 任务拆解与分发 | 内核调度器 |
| Gateway | 多端消息接入 | 网络栈 |
| Delegation | 子 Agent 并行执行 | 多线程 |

### 设计红线
1. Core 不依赖任何外部执行器（Grok/Codex 可插拔）
2. 记忆主权单一（不开双脑）
3. 进程边界 = 架构边界（subprocess 而非链接库）

## 个人见解
> 我现在终于理解：Hermes 不是一个"更好的 ChatGPT"，它是一个以我为中心的认知操作系统。Grok 是它的"手"，但所有的记忆、知识、决策都归 Hermes。
>
> （填写你的理解）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — 所有模块在 Loop 中运行
- [[Memory（持久记忆）]] — 耐久信息存储
- [[Skill（技能系统）]] — 可扩展的能力模块

### ← 被指向
- [[Planner（任务规划器）]] — 战略层实现
- [[Skill Router（技能路由）]] — 分发层实现
- [[Delegation（任务委派）]] — 并发执行实现
