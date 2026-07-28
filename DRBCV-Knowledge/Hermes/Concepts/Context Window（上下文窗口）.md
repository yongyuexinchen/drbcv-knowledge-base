---
name: Context Window（上下文窗口）
type: connection
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
cross_ref: "[[上下文窗口]]"  # 酒馆 vault 已有，本卡聚焦 Hermes 特有的压缩机制
---

# Context Window（上下文窗口）

## 类型判定
连接型 — 它决定了 Agent 能记住多少历史、能处理多大的文件、以及何时触发压缩。

## 是什么
Context Window（上下文窗口）是 LLM 一次能"看到"的最大 token 数。包含 system prompt、历史消息、工具定义、工具结果——所有内容加起来不能超过这个上限。超了要么截断、要么压缩。

## 输入-输出空间
**输入**：system prompt + 历史消息 + 工具 schema + pending tool results
**输出**：如果总 token 数 > 窗口 → Hermes 触发压缩或截断；否则正常提交给 LLM

## 正例（≥2个）
- Claude Sonnet 4：200K 窗口，可以一次读完整本技术书
- Gemini 3 Flash：1M 窗口（业界最大），一次处理几小时视频字幕
- DeepSeek V4：128K 窗口
- GitHub Copilot：400K 窗口

## 反例/边界（≥1个）
- 官方标称 200K ≠ 实际可用 200K——Attention 机制在长上下文尾部的准确度下降（"Lost in the Middle"效应）
- 上下文压缩会丢失细节：Hermes 默认在 50% 窗口时自动压缩，压缩后的历史是摘要而非原文
- 窗口大 ≠ 适合塞满——token 越多响应越慢、越贵

## 详细解释
Hermes 的上下文压缩配置：
```yaml
compression:
  enabled: true
  threshold: 0.50     # 达窗口 50% 时触发
  target_ratio: 0.20  # 保留最近 20% 不压缩
  protect_last_n: 20  # 最近 20 条消息强制不压缩
```

压缩策略：旧消息 → LLM 摘要 → 替换原文 → 保留最近消息 + 关键信息。手动触发：`/compress`。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| Lost in the Middle | Attention 在长上下文中部准确度下降——重要信息放开头或结尾 |
| 压缩截断 | 保留前 70% + 后 20%（共 90%），中间丢弃 |

### 常见模型窗口对照
| 模型 | 窗口 | 约等于 |
|------|------|--------|
| GPT-5-mini / DeepSeek V4 | 128K | 一本 200 页书 |
| Claude Sonnet 4 | 200K | 三本书 |
| Gemini 3 Flash | 1M | 十五本书 |
| GitHub Copilot | 400K | 六本书 |

### 使用原则
- 不要因为窗口大就塞满——越多越慢越贵，中间越容易被忽略
- 窗口利用率 50% 时 Hermes 自动触发压缩


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — 上下文容量限制循环长度

### ← 被指向
- [[Prompt Cache（提示词缓存）]] (depends-on) — 缓存前缀必须在窗口内
- [[Memory（持久记忆）]] (depends-on) — Memory 注入占用上下文空间（2200 字符上限）