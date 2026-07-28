---
name: Token
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-认知层
---

# Token

## 类型判定
判别型 — LLM 处理文本的最小单位，AI 世界的「计价筹码」。

## 类比 ★
### 一句话比喻
Token 像出租车计价器的跳动——不是按公里（字数）计，而是按「词块」计。「我喜欢AI伴侣」在司机（LLM）眼里不是 6 个字，可能是「我/喜欢/AI/伴侣」4 下跳动，每跳一下都是钱。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| Token | 出租车计价器的每次跳动——LLM 按这个收费，每跳一下算一份钱 |
| Tokenizer（分词器） | 计价器的计数规则——中文按字跳、英文按词块跳、代码按符号跳 |
| Context Window（以 Token 为单位） | 计价器最多跳 128000 下——跳满了就不能再上车 |

## 是什么
Token 是 LLM 处理文本的基本单位，不是字符也不是单词。Tokenizer 将文本切分为 token 序列：英文中 1 token ≈ 0.75 个单词，中文 1 token ≈ 1-2 个汉字。LLM 按 token 计费（Input Token + Output Token），模型的能力边界（Context Window）也以 token 衡量。Token 直接决定使用成本和上下文容量。

## 输入-输出空间
- **输入**: 文本 → Tokenizer → Token ID 序列（整数）
- **输出**: Token ID 序列 → Detokenizer → 文本
- **中文**: 1 汉字 ≈ 1-1.5 token；英文: 1 单词 ≈ 1.3 token

## 正例（≥2 个）
1. **成本估算**: 一段 500 字的用户消息 + 系统 Prompt 共 2000 input tokens，GPT-4 $0.03/1K → 本次调用 $0.06
2. **窗口预算**: 128K 窗口想放 100 轮对话——每轮约 200 tokens → 100×200=20K tokens → 还能放很多上下文

## 反例/边界（≥1 个）
1. **「一个字 = 一个 token」的误解**: 中文里「𪚥」（生僻字）可能是 2-3 个 token——不是简单按字计数
2. **边界 — 不同模型 token 不同**: GPT 的 Tokenizer 和 DeepSeek 的 Tokenizer 对同一段文字的 token 数不同——迁移模型时成本预估会变

## 详细解释
Token 的生命周期：
```
文本 "你好世界"
  → Tokenizer 编码 → [123, 456, 789]（3 个 token ID）
  → Embedding → 3 个向量
  → Transformer 计算
  → 输出 token ID → Detokenizer → "你好，世界！"
```

API 计费结构：
- **Input tokens**: System Prompt + 对话历史 + RAG 结果 + 用户消息 → 计费便宜
- **Output tokens**: LLM 生成的内容 → 计费贵（通常是 Input 的 3-5 倍）

在 AI 伴侣中，优化 Token 使用 = 省钱 + 省延迟：
- 精简 System Prompt（能 500 字说清就别写 2000 字）
- 旧对话压缩成摘要（10 轮对话压成 2 行）
- 输出设 max_tokens 上限（别让 LLM 写小作文）

## 关系
### → 指向
- [[Context Window]] — 上下文窗口的大小以 Token 计量
- [[LLM]] — LLM 输入输出都通过 Token 进行

### ← 被指向
- [[Prompt Engineering]] — 优化 Prompt 的核心指标之一就是减少 Token 浪费
- [[Embedding]] — Embedding 模型也有 Token 限制，长文本需要截断
