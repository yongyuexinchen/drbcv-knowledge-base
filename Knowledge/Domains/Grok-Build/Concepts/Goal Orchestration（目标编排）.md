---
name: Goal Orchestration（目标编排）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: grok-build
---

# Goal Orchestration（目标编排）

## 类型判定
系统型 — Goal Orchestration 是 Grok Build 内部的 Agent Loop，通过多角色流水线将任务拆解为工具调用序列。

## 是什么
Grok 内部不是"一个 LLM + 工具"的简单循环。它采用**多角色流水线**：classifier（分类）→ planner（拆解）→ strategist（策略）→ next_step（决策）→ 工具循环 → verifier（校验）→ summarizer（总结）→ stop_detector（终止）。每个角色有独立的 prompt 模板（`goal_*.md`）。

## 输入-输出空间
- **输入**：用户任务 + 工作目录上下文 + 可用工具列表
- **输出**：完成的任务结果 + session 记录

## 正例（≥2个）
1. **简单任务**："写 fibonacci.py" → classifier 判定为单文件生成 → planner 跳过 → 直接工具循环创建+运行
2. **复杂任务**："创建 Markdown 笔记 CLI 工具" → classifier→planner 拆为 5 步 → strategist 决定先后 → 工具循环每步建文件/写 SQL/写测试 → verifier 跑 pytest → summarizer 总结

## 反例/边界（≥1个）
- `--max-turns 30` 限深后，超过即 `stop_reason=max_turns_reached`（半成品）
- 与 Hermes Planner 是父子关系：Hermes 管"做什么"（战略），Grok goal_planner 管"怎么分步实现"（战术）
- goal_stop_detector 负责判断"任务是否完成"，避免无限循环

## 详细解释
完整流水线：
```
goal_classifier      → 这是什么类型的任务？
goal_planner         → 需要哪些步骤？
goal_strategist      → 先做哪个后做哪个？
goal_next_step       → 下一步具体做什么？
  ↓
工具循环 (≤ max_turns 轮)
  ├── read_file    ├── search_replace
  ├── run_terminal_cmd    └── grep/list_dir
  ↓
goal_verifier        → 验收标准满足了吗？
goal_summarizer      → 总结做了什么
goal_stop_detector   → 可以停止了吗？
```

## 细节备注

### 与 Hermes Agent Loop 对比
| 维度 | Hermes Agent Loop | Grok Goal Orchestration |
|------|------------------|------------------------|
| 层级 | 战略 | 战术 |
| 角色 | Planner → Tool Loop | Classifier→Planner→Strategist→...→StopDetector |
| 工具 | Hermes 全工具集 | 编码工具（文件/终端/搜索） |
| 记忆 | Memory 模块 | 不开（GROK_MEMORY=0） |

### 关键模板
| 模板 | 作用 |
|------|------|
| goal_classifier_prompt.md | 任务类型判别 |
| goal_planner_prompt.md | 步骤拆解 |
| goal_task_discipline.md | 任务纪律约束 |
| goal_continuation_directive.md | 续接指令 |

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Tool Calling（工具调用）]] — 工具循环的执行层
- [[Session Management（会话管理）]] — 编排过程记录在 session 中

### ← 被指向
- [[Grok Build Overview（Grok Build 总览）]] — 是 Grok 的核心运行时
- [[Hermes-Grok Integration（Hermes-Grok 集成）]] — Hermes 通过 Headless 模式触发编排
