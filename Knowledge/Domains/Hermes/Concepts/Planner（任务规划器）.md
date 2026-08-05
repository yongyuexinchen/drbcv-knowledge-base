---
name: Planner（任务规划器）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: hermes
---

# Planner（任务规划器）

## 类型判定
系统型 — Planner 是 Hermes 的"战略层"，负责将用户意图拆解为可执行的子任务，决定调用哪个 Skill 或工具。

## 是什么
Planner 是 Hermes 的中央决策模块。它不直接执行任务，而是判断任务类型、拆解为子步骤、选择合适的 Skill 或工具链下发。它是 Hermes 区别于 Grok 的关键——**Hermes 管"要做什么"，Grok 管"怎么改代码"**。

## 输入-输出空间
- **输入**：用户自然语言任务（如"实现一个 RAG 测试程序"）
- **输出**：结构化的子任务列表 + 每步指定的执行者（Skill / 原生工具 / 委派子 Agent）

## 正例（≥2个）
1. **编码任务**：用户说"写一个爬虫" → Planner 识别为 execution 类 → 下发 `grok-build` Skill → Grok 执行
2. **博客任务**：用户说"写一篇深度文章" → Planner 识别为 creative 类 → 创建 Kanban 任务 → Orchestrator→Researcher→Writer→Reviewer→Publisher
3. **简单问答**：用户说"1+1=?" → Planner 跳过，直接 LLM 回复

## 反例/边界（≥1个）
- Planner 不执行具体操作（不改文件、不跑命令）——那是 Grok 的事
- Planner 不记忆——结果交给 Memory 模块
- 如果 Planner 判断错误（把简单问题当复杂任务拆解）→ 增加不必要的 token 消耗

## 详细解释
Planner 的工作流：
```
用户意图 → 分类器（判别任务类型）
  ├── 简单问答 → 直接 LLM 回复
  ├── 编码/执行 → 下发 grok-build Skill
  ├── 创作/写作 → 创建 Kanban 任务
  ├── 研究/搜索 → 委派子 Agent 或 web_search
  └── 记忆/配置 → 调用对应工具
```

核心原则：**战略→战术拆解**。Hermes Planner 决定"做什么+分几步+谁来执行"，不陷入"怎么实现"的细节。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 任务分类 | 判别 coding / creative / research / config 四类 |
| 粒度控制 | 下发给 Grok 的是"叶子级编码任务"，不是"做一个系统" |
| 验收标准 | 下发时必须带可核验的验收条件（如"pytest 全绿"） |

### 与 Grok Planner 的层级关系
```
Hermes Planner（战略）     Grok goal_planner（战术）
─────────────────────     ─────────────────────
"做一个RAG系统"            "要创建3个文件,依次:"
  ├─ 调研技术路线            ├─ vector_store.py
  ├─ 编码实现 → Grok         ├─ retriever.py
  └─ 测试验证               └─ test_rag.py
```
两者不是冲突，是父子层级。Hermes 拆任务，Grok 拆实现步骤。

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — Planner 在 Agent Loop 中运行
- [[Skill Router（技能路由）]] — Planner 决策后由 Router 执行分发

### ← 被指向
- [[Skill（技能系统）]] — Skill 的 When to Use 触发条件由 Planner 判断
- [[Delegation（任务委派）]] — Planner 可决定委派子 Agent 处理子任务
