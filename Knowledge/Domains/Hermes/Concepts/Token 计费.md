---
name: Token 计费
type: connection
status: core
source: "[[Hermes教程-模块一-入门篇]]"
domain: hermes
---

# Token 计费

## 类型判定
连接型 — Token 计费连接了「模型调用」和「成本控制」，是企业采购 AI 服务时的核心决策依据。

## 是什么
Token 是大语言模型处理和计费的最小单位。一个 token ≈ 0.75 个英文单词 ≈ 0.5 个中文字。API 调用后返回 `usage` 对象，包含 `prompt_tokens`（输入消耗）和 `completion_tokens`（输出消耗），分别乘以各自的单价得出本次调用费用。

## 输入-输出空间
**输入**：input text + output text + 模型定价表
**输出**：费用 = prompt_tokens × 输入单价 + completion_tokens × 输出单价

## 正例（≥2个）
- DeepSeek V4-Pro：输入 ¥1/百万 tokens，输出 ¥4/百万 tokens。一篇 2000 字文章（约 4000 tokens 输入 + 3000 tokens 输出）只需几分钱
- Claude Sonnet 4：输入 $3/百万 tokens，输出 $15/百万 tokens。同样的文章贵 10-15 倍
- 中转站通常加价 50%-200%：硅基流动 DeepSeek V4 比官方贵约 1.5-2 倍

## 反例/边界（≥1个）
- API 返回的 `usage.total_tokens` 不等于 `prompt + completion`（有些厂商把 tool call 的 tokens 单独计）
- 缓存命中时的计费：prompt_tokens 正常计数但**单价打折**（90% off），不是 tokens 数减少
- 流式响应的 token 计数和非流式**可能不同**（碎片化导致略多）

## 详细解释
Token 计费的三个关键数字：

| 模型等级 | 输入单价（$/MTok） | 输出单价（$/MTok） | 2000 字文章费用 |
|---------|-------------------|-------------------|---------------|
| DeepSeek V4 | ¥1 | ¥4 | ¥0.02 |
| GPT-5-mini | $0.15 | $0.60 | $0.003 |
| Claude Sonnet 4 | $3 | $15 | $0.06 |
| Gemini 3 Flash | $0.10 | $0.40 | $0.002 |

**省钱策略**：便宜模型调研（DeepSeek）→ 贵模型写作（Claude）→ 便宜模型审核（DeepSeek）。这就是 Hermes 实战篇里「researcher 用 DeepSeek，writer 用 Claude」的原因。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| thinking tokens | 推理模型的思考 token 单独计价（通常和 output 同价） |
| Batch API 半价 | OpenAI/Anthropic batch 模式 24h 完成 → 五折 |
| 图像 token 计费 | 视觉模型按图像分辨率折算 token（约 85 tokens/512x512 图块） |
| cached tokens | 缓存命中的 input tokens 正常计数但费用打一折 |

### 省钱策略
| 场景 | 策略 |
|------|------|
| 调研/搜索 | DeepSeek（便宜） |
| 写作/创意 | Claude/GPT（贵但质量高） |
| 批量分析 | Batch API（半价） |
| 重复调用 | 稳定 system prompt → 缓存命中 → 省 90% |


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[OpenAI 兼容 API]] — 计费数据来自 API 响应的 usage 字段
- [[Prompt Cache（提示词缓存）]] — 缓存命中可降低 90% 输入费用

### ← 被指向
- [[Provider（模型提供商）]] (depends-on) — 不同 Provider 定价不同
- [[Agent Loop（Agent 循环）]] (depends-on) — Agent 每次循环都有 token 消耗