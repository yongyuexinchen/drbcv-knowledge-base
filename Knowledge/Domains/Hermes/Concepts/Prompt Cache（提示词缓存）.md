---
name: Prompt Cache（提示词缓存）
type: connection
status: core
source: "[[Hermes教程-模块五-实战篇]]"
domain: hermes
---

# Prompt Cache（提示词缓存）

## 类型判定
连接型 — 它连接了"省钱"和"系统设计"两个世界：缓存命中 → 费用大幅降低 → 系统提示词必须保持稳定。

## 是什么
Prompt Cache 是 LLM API 的一种优化机制：当连续请求的 prompt 前缀相同时，服务端缓存该前缀的 KV-cache 计算结果，后续请求只需支付缓存读取费（通常便宜 90%），而不必重新计算。Antropic、DeepSeek、OpenAI 都支持。

## 输入-输出空间
**输入**：连续多个 API 请求，它们共享相同的 prompt 前缀（通常是 system prompt + 工具定义）。
**输出**：命中的请求 token 费用大幅降低（cache_write 一次性写入费 + cache_read 廉价读取费），未命中则正常计费。

## 正例（≥2个）
- Hermes 的系统提示词（工具定义 + SOUL.md + Memory）在多轮对话中不变 → 全部命中缓存，每轮只付新消息的费用
- Anthropic Claude：缓存命中后 prompt price 从 $15/MTok 降到 $1.50/MTok（10 倍差价）
- DeepSeek：缓存命中后 prompt price 从 ¥1/MTok 降到 ¥0.1/MTok（同样 10 倍差价）

## 反例/边界（≥1个）
- 每轮对话都改 system prompt → 缓存前缀变化 → 从未命中 → 每次都付全价
- 中途修改工具定义（新增/删除 tool schema）→ 前缀变化 → 缓存失效
- 缓存有 TTL（通常 5-10 分钟无请求后清空）→ 低频对话不会命中
- 缓存有最小长度阈值（DeepSeek 要求 ≥4KB 前缀才缓存）→ 短前缀不触发缓存

## 详细解释
Prompt Cache 利用了 Transformer 的自回归特性：生成下一个 token 时，所有历史 token 的 KV-cache 已经算过了。如果前缀没变，就不用重算。

**为什么 Hermes 强调"不要中途改工具/上下文"？** 因为每次修改 system prompt 或 tool schema，整个前缀就变了，缓存全部失效。保持稳定 = 省钱。

**缓存标记**：有些 API（如 Anthropic）要求显式标记哪些内容要缓存（`cache_control: {type: "ephemeral"}`）。DeepSeek 自动检测重复前缀，无需手动标记。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| Anthropic cache_control | 需显式标记 {"type":"ephemeral"}；最多 4 个断点；最小缓存块 1024 tokens |
| DeepSeek 自动检测 | 无需手动标记；前缀需 >= 4KB 才触发 |
| TTL | Anthropic 5 分钟；DeepSeek 约 5-10 分钟无请求后清空 |
| cache_write vs cache_read | write 费比正常 prompt 贵约 1.25x；read 费便宜 90% |

### 使用原则
- 保持 system prompt + 工具定义在会话期间不变 → 缓存持续命中
- 低频对话（间隔 > 10 分钟）几乎无法命中缓存


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[OpenAI 兼容 API]] — 缓存机制在 API 层面实现
- [[Context Window（上下文窗口）]] — 缓存的是上下文前缀

### ← 被指向
- [[Agent Loop（Agent 循环）]] (depends-on) — Agent Loop 的设计必须保持前缀稳定以利用缓存
- [[Skill（技能系统）]] (depends-on) — Skill 加载会修改 system prompt → 可能破坏缓存
- [[Memory（持久记忆）]] (depends-on) — Memory 写入不改当前会话已注入的快照 → 保护缓存