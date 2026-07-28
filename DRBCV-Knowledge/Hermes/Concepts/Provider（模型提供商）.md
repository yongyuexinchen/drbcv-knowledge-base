---
name: Provider（模型提供商）
type: connection
status: core
source: "[[Hermes教程-模块一-入门篇]]"
domain: hermes
---

# Provider（模型提供商）

## 类型判定
连接型 — Provider 是模型和 Agent 之间的桥梁，不同的 Provider 通过统一的内部接口连接到 Agent。

## 是什么
Provider 是 Hermes Agent 对模型来源的抽象层。一个 Provider 封装了：API 端点地址、认证方式、可用模型列表、计费方式。Hermes 通过 Provider 层实现了**不被任何单一模型厂商锁定**——改一行配置就能从 DeepSeek 切换到 Claude 再到本地模型。

## 输入-输出空间
**输入**：messages 数组 + 模型参数（temperature、max_tokens 等），由 Agent Loop 构造。
**输出**：LLM 文本响应 + token 使用统计。无论底层是哪个厂商，输出格式被统一。

## 正例（≥2个）
- **官方直连**：DeepSeek Provider → `api.deepseek.com`，用 DeepSeek 官方 API Key
- **中转聚合**：OpenRouter Provider → `openrouter.ai`，一个 Key 调 200+ 模型
- **本地模型**：Ollama Provider → `localhost:11434`，跑本地 Llama
- **OAuth 无 Key**：Nous Portal Provider，OAuth 登录后直接使用，无需管理 API Key

## 反例/边界（≥1个）
- 直接在代码里写死 `requests.post("https://api.deepseek.com/...")`——跳过了 Provider 抽象层，无法利用 Hermes 的 Key 池化、自动切换、余额检测
- 把不同厂商的 API Key 混在同一个 Provider 里用——Provider 只认一个 base_url，混用会 401

## 详细解释
Hermes 支持 20+ 内置 Provider：Anthropic、OpenAI、DeepSeek、xAI、Google Gemini、GitHub Copilot、MiniMax、Kimi、GLM、Hugging Face 等。每个 Provider 有自己的 `key_env`（API Key 环境变量名）和解析逻辑。

Provider 的核心价值：
1. **统一接口**：不管你后面是 DeepSeek 还是 Claude，Agent Loop 的代码不变
2. **凭证池化**：同一个 Provider 可以配多个 API Key，自动轮转，余额不足跳过
3. **热切换**：`hermes config set model.provider deepseek`，无需重启

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 凭证池化 | 同一 Provider 可配多个 API Key → 自动轮转 → 余额不足跳过 |
| 回退链 | model.default + fallback_models → 主模型挂了自动切换备用 |
| 模型退役检测 | xAI Provider 内置：旧模型下线时自动切换到替代模型 |

### Hermes 内置 Provider（20+）
OpenRouter · Anthropic · Nous Portal · OpenAI API · GitHub Copilot · Google Gemini · DeepSeek · xAI/Grok · Hugging Face · GLM · MiniMax · Kimi/Moonshot · DashScope · AWS Bedrock · LM Studio · NVIDIA NIM · Custom endpoint

### 使用原则
- 不要硬编码 Provider——通过 hermes config set model.provider xxx 热切换


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 实现 (implements)
- [[OpenAI 兼容 API]] — 大多数 Provider 实现了此协议

### 依赖 (depends-on)
- [[API Key 认证]] — Provider 需要通过 API Key / OAuth 认证
- [[Base URL + Endpoint]] — 每个 Provider 有自己的 base_url

### ← 被指向
- [[Custom Provider（自定义提供商）]] (is-a) — Custom Provider 是一种特殊的 Provider
- [[Agent Loop（Agent 循环）]] (depends-on) — Agent Loop 依赖 Provider 获取 LLM 响应