# AI 记忆系统调研报告（修正版）

> 调研日期：2026-07-30 · 修正日期：2026-07-30
> ⚠️ 初版存在严重版本混用问题，此版为 ChatGPT 审计后的修正版本

---

## 0. 初版问题总结

| 问题 | 严重程度 | 修正 |
|------|---------|------|
| 混用 Letta V1 和 Agent SDK 两代架构 | 🔴 严重 | 已区分两代，标注 SDK 语言 |
| Mem0 架构描述基于旧版（Neo4j）| 🔴 严重 | 修正为 V3 向量存储方案 |
| LangChain Memory 用已过时的类 | 🟡 中等 | 替换为 LangGraph State + Store |
| Zep 过度简化为"企业 API" | 🟡 中等 | 补充 Graphiti 时间图能力 |
| "Dreaming = 独立人格基础" | 🟡 夸大 | 修正为"人格连续性的基础设施之一" |

---

## 一、正确版本对比

| 维度 | Mem0 (V3) | Zep/Graphiti | Letta V1 (旧) | Letta Agent SDK (新) | LangGraph | Memobase |
|------|-----------|-------------|---------------|---------------------|-----------|----------|
| **核心记忆模型** | 向量存储内实体链接 | 时间上下文知识图谱（实体+关系+有效期） | Memory Blocks（Persona/Human） | MemFS：文件式持久记忆 | State + Store + Thread | 用户画像 JSON |
| **存储** | 向量 DB（内置，不需要 Neo4j） | Graphiti（Neo4j 或 FalkorDB） | PostgreSQL | 本地文件系统 / App Server | PostgreSQL Checkpointer | 云 API |
| **Agent 记忆维度** | user / agent / app / session | agent / user / entity | Persona + Human 两块 | human / persona 文本块 | user_id + thread_id | user_id |
| **跨会话** | ✅ | ✅（时间图天然支持） | ✅（Archival） | ✅（MemFS 持久化） | ✅（Store + Checkpointer） | ✅ |
| **SDK 语言** | Python ✅ | Python ✅ | Python SDK（弃用中） | **TypeScript** 优先 | Python ✅ | Python ✅ |
| **部署** | Python SDK + 云 | Docker | Docker | CLI / App Server | Python 库 | 云 API |
| **维护状态** | ✅ 活跃 | ✅ 活跃 | ⚠️ Legacy | ✅ 主力开发 | ✅ 活跃 | ⚠️ 官网下线，仓库活跃 |
| **学习成本** | 低 | 中 | 中 | 中（需 TypeScript） | 中 | 低 |

---

## 二、逐方案修正

### Mem0 (V3) — 修正

**初版错误**：描述为"图数据库 Neo4j + 时间衰减 + 冲突解决"

**实际现状**：
- V3 开源算法已移除外部图存储（Neo4j/Memgraph），改为向量存储内实体链接
- 支持 `user` / `agent` / `app` / `run` 等多维度记忆隔离
- Memory Decay 是可选检索排序机制，**默认关闭**
- 可以保存 `agent_id: "yongyue"` 级别的记忆

**对永月的意义**：
-Mem0 **可以**存 Agent 维度的记忆，不等同于"完全不支持 Agent 记忆"
- 但它不提供人格模型——存什么、怎么组织、怎么保护核心人格，是你自己的事
- 适合作为记忆**存储层**，不适合作为人格**管理层**

### Letta — 重大修正

| | Letta V1（旧） | Letta Agent SDK（新，推荐） |
|------|------|------|
| SDK 语言 | **Python** | **TypeScript** |
| 记忆模型 | Memory Blocks（Persona/Human/Archival） | MemFS + Dreaming |
| 部署 | Docker + REST API | CLI 本地 / App Server |
| 当前状态 | ⚠️ Legacy，V1 SDK 逐步弃用 | ✅ 主力开发方向 |
| 官方推荐新项目？ | ❌ | ✅ |

**这意味着**：如果你要用 Letta 最新功能（MemFS + Dreaming），必须先碰 TypeScript。

**Dreaming 的真实定位**（修正过度拔高）：
- Dreaming 存在，确实使用后台子 Agent 回顾对话、巩固经验
- 可配置云端模型或本地模型，不一定需要自己备 GPU
- **但它不是"独立人格的技术基础"**——它只是"记忆巩固"这个功能的实现

### LangChain/LangGraph — 修正

**初版错误**：列的四个类（BufferMemory、SummaryMemory、KGMemory）大部分已是旧 API

**当前推荐路线**：
```
短期记忆：Thread ID + PostgreSQL Checkpointer 持久化
长期记忆：Store + 跨会话命名空间（user_id 维度）
```

**建议学习的实际 API**：
- `LangGraph State` — 替代老式 Memory 类
- `Checkpointer` — 持久化会话状态
- `Store` — 跨会话长期存储
- `Thread ID` — 会话隔离

### Zep/Graphiti — 修正

**初版过度简化**："企业用户事实提取 API"

**实际**：开源部分核心是 Graphiti——时间上下文知识图谱
- 实体、关系、事实有效时间、来源追踪
- 天生处理"过去是什么 → 现在是什么"的时间线变化
- 对 AI 伴侣其实很有价值（关系状态随时间变化）

**不推荐的原因修正**：不是"不适合 AI 伴侣"，而是"工程成本偏高，不适合作为第一个 Demo 的起点"

---

## 三、修正后的学习路径（不再做最终选型）

> **核心思路转变：不是"先调研再选一个"，而是"先手写再看工具替你做了什么"**

```
第一步（第 10 周）  手写最小记忆闭环
  FastAPI + PostgreSQL
  四个核心对象：
    agent_identity     永月是谁（人格定义）
    user_profile       用户是谁（画像）
    relationship_state 双方关系状态
    memory_event       事件/事实（时间线）

  手写流程：
    对话 → LLM 提取事实 → 分类到四个对象 → 存储 → 检索 → 注入 System Prompt

第二步（第 10 周）  LangGraph 持久化
  用 Checkpointer + Store 替换手写的 PostgreSQL 操作
  理解 thread memory vs 跨会话 store

第三步（第 11 周）  Mem0 对照实验
  接入 Mem0 V3，看它替代了手写流程中的哪些部分
  重点观察：agent_id 维度隔离是否够用

第四步（第 12 周）  Letta 独立试验（不进主项目）
  单独起一个 Letta Agent，研究 MemFS + Dreaming
  用同一组测试对话观察人格连续性
  注意：新版 SDK 是 TypeScript，可能需要额外学习成本

第五步（第 12 周）  统一测评
  同一组对话 → 分别跑手写方案 / Mem0 / Letta
  记录：记忆准确率、人格一致性、幻觉率
  最终选型基于数据，不基于文档描述
```

---

## 四、关键认知修正

### 1. Persona ≠ 独立人格

真正的 AI 伴侣人格需要六层：

```
L1  Identity          我是谁，核心价值和行为边界不可随意变化
L2  Human Profile     我对用户的长期认识
L3  Relationship      我们是什么关系，关系处于什么阶段
L4  Episodic Memory   我们共同经历过什么具体事件
L5  Semantic Memory   从多次事件中归纳出的稳定认识
L6  Reflection        如何从事件中更新理解，但不污染核心人格
```

- Letta 可以帮助实现 L4/L5/L6 中的部分
- Mem0 可以帮助实现 L2/L4 的存储
- **没有任何一个工具帮你定义 L1**——那是你作为设计者的事

### 2. "框架绑定"的风险

> 永月的"灵魂模型"应该由你自己定义，不能绑定在某个框架上。

工具会变、会被弃用（Letta V1 已经在发生），但如果你自己定义清楚了人格的六层模型，换工具只是换底层实现。

---

## 五、更新后的工具推荐（不排他）

| 场景 | 推荐 | 理由 |
|------|------|------|
| **第一个 Demo** | 手写 + PostgreSQL | 理解本质，不被框架概念迷惑 |
| **持久化会话** | LangGraph Store + Checkpointer | LangChain 生态标准方案 |
| **长期记忆存储** | Mem0 V3 | Python 原生、部署简单、生态成熟 |
| **人格连续性研究** | Letta Agent SDK | 最前沿但需要 TypeScript，独立试验 |
| **时间线事件追踪** | Zep/Graphiti | 强大但工程重，后期可考虑 |

---

*修正完毕。核心教训：调研 ≠ 选型。先手写，再对照，最后用实验数据做决策。*
