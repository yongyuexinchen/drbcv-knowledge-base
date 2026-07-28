---
name: Session Search（会话搜索）
type: system
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
---

# Session Search（会话搜索）

## 类型判定
系统型 — Session Search 是 Hermes 的历史对话检索引擎，v0.15 重建后从 ~90s 降到 ~20ms（4500 倍），且零费用。

## 是什么
Session Search 让 Hermes 能搜索所有历史会话。基于 SQLite FTS5 全文索引，无需调用 LLM。Agent 在用户提到过去对话或怀疑有历史上下文时，先调 `session_search` 回忆，而不是让用户重复信息。

## 输入-输出空间
**输入**：`session_search(query="Docker deployment", limit=3)`
**输出**：匹配的会话列表（session_id、标题、命中片段、上下文窗口、首尾消息摘要）

## 正例（≥2个）
- 用户「上次我们讨论的 Docker 方案怎么样了？」→ Agent Discovery 搜索 → 找到会话 → Scroll 查看完整上下文 → 回答
- Writer Agent 「之前的技术文章是什么风格？」→ session_search → 找到类似文章 → 当作风格参考
- 无参数 Browse：用户「我最近在做什么？」→ 按时间列出近期会话

## 反例/边界（≥1个）
- v0.15 前依赖 LLM 摘要（慢+贵）→ v0.15 用 FTS5 纯 SQL（快+免费）
- Discovery 模式默认只搜索 user+assistant 消息（tool 结果被过滤）
- FTS5 查询语法：`docker deployment`（AND）、`docker OR kubernetes`（OR）、`"exact phrase"`（精确）、`deploy*`（前缀）
- CJK（中日韩）用 trigram 索引，英文用标准 FTS5 索引——两套并行

## 详细解释
三种调用形态（根据参数自动判断）：

| 形态 | 参数 | 用途 |
|------|------|------|
| Discovery | `query` | 按关键词搜索 |
| Scroll | `session_id` + `around_message_id` | 在命中会话里前后翻看 |
| Browse | 无参数 | 按时间浏览近期会话 |

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| FTS5 trigram | CJK 用 trigram 索引，英文用标准 FTS5 |
| 三种形态 | Discovery(query) / Scroll(session_id+msg_id) / Browse(无参数) |
| 零费用 | v0.15 去除 LLM 依赖 → 纯 SQLite FTS5 → ~20ms |

### v0.15 前后对比
| 维度 | v0.14 前 | v0.15+ |
|------|---------|--------|
| 搜索方式 | LLM 摘要 | SQLite FTS5 |
| 耗时 | ~90s | ~20ms |
| 费用 | 每次耗 token | 零 |
| 准确性 | 依赖摘要质量 | 精确匹配 |

### FTS5 查询语法
docker deployment (AND) · docker OR kubernetes (OR) · "exact phrase" · deploy* (前缀) · python NOT java (排除)


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Session（会话）]] — 搜索的原始数据来源

### ← 被指向
- [[Memory（持久记忆）]] — 互补：Memory=稳定事实，Session Search=历史对话
- [[Agent Loop（Agent 循环）]] — Agent 在循环中调用此工具