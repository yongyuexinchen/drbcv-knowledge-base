---
name: Skill Router（技能路由）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: hermes
---

# Skill Router（技能路由）

## 类型判定
系统型 — Skill Router 是 Planner 的执行分发层，将分类好的任务匹配到对应的 Skill 或工具链。

## 是什么
Skill Router 是 Hermes 的"调度中枢"。Planner 判定了任务类型后，Router 根据 Skill 的 frontmatter `description`（触发条件）匹配最合适的 Skill，加载其 SKILL.md 到系统提示词中，Agent 按 Skill 中的步骤执行。

## 输入-输出空间
- **输入**：任务类型标签（coding / creative / research / config）+ 任务描述
- **输出**：选中的 Skill 被加载到系统提示词 → Agent 按 SKILL.md 范式执行

## 正例（≥2个）
1. **grok-build Skill**：任务类型=coding → Router 匹配到 `grok-build` Skill（description 含"Use when delegating coding/execution tasks"）→ 加载技能 → Adapter 调用 Grok CLI
2. **blog-kanban-workflow**：任务类型=creative，触发词含"写文章/博客" → Router 匹配博客 Skill → 创建 Kanban 任务
3. **无匹配**：简单问候 → Router 无匹配 → 走默认 Agent Loop（LLM 直接回复）

## 反例/边界（≥1个）
- Router 不修改 Skill 内容——只负责匹配和加载
- Skill 未安装时 Router 无法匹配 → 回退到通用 Agent Loop 或建议用户安装
- 多个 Skill 同时匹配 → 按优先级加载，相关信息注入系统提示词

## 详细解释
Router 匹配逻辑：
```
任务进入 → 遍历 skills_list → 匹配 description 触发条件 → 
加载 SKILL.md → 注入 system prompt → Agent 按步骤执行
```

对于 grok-build Skill：
```
任务"写一个爬虫" → Router 匹配 → 加载 grok-build SKILL.md →
Agent 看到调用范式: terminal(command="python grok_adapter.py run ...") →
实际执行 Adapter → Grok CLI → 返回结果
```

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 匹配机制 | 基于 Skill description 的语义匹配 |
| 降级策略 | 无匹配 → 通用 Agent Loop；Skill 失败 → 回退其他 Skill |

### 架构位置
```
User → Hermes Core → Planner（战略判断）→ Skill Router（分发）→ Skill 执行
```
Router 是 Planner 和 Skill 之间的桥梁，不承担规划职责。

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Planner（任务规划器）]] — 拿到 Planner 的任务分类后执行匹配
- [[Skill（技能系统）]] — 管理可用的 Skill 池

### ← 被指向
- [[Delegation（任务委派）]] — 某些 Skill 内部会委派子 Agent
