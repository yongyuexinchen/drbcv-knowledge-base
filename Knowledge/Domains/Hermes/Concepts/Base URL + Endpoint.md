---
name: Base URL + Endpoint
type: connection
status: core
source: "[[Hermes教程-模块一-入门篇]]"
domain: hermes
---

# Base URL + Endpoint

## 类型判定
连接型 — 它描述了 API 地址的两个组成部分如何拼接成完整请求路径，是协议寻址的核心机制。

## 是什么
Base URL 是 API 服务的"门牌号"（如 `https://api.deepseek.com`），Endpoint 是"房门"（如 `/v1/chat/completions`）。两者拼接 = 完整的 API 调用地址。所有 OpenAI 兼容的 API 服务共享相同的 endpoint 路径，只在 base_url 上有区别。

## 输入-输出空间
**输入**：base_url（服务根地址）+ endpoint（功能路径）+ HTTP 方法（GET/POST）+ 请求体。
**输出**：HTTP 响应。endpoint 决定了返回什么——`/v1/chat/completions` 返回文本，`/v1/embeddings` 返回向量。

## 正例（≥2个）
- DeepSeek：`https://api.deepseek.com` + `/v1/chat/completions` = `https://api.deepseek.com/v1/chat/completions`
- 硅基流动：`https://api.siliconflow.cn` + `/v1/chat/completions` = `https://api.siliconflow.cn/v1/chat/completions`
- 中转站切换只需改 base_url，endpoint 不变——这是 OpenAI 兼容协议的核心价值

## 反例/边界（≥1个）
- Anthropic API 的 endpoint 是 `/v1/messages` 而非 `/v1/chat/completions`，不能直接替换 base_url
- Google Gemini 不用 `/v1/` 前缀，而是 `/{model}:generateContent`，完全不兼容此寻址模式
- WebSocket 端点（如 `wss://`）不走 REST 路径拼接规则

## 详细解释
Base URL + Endpoint 的模式来自 RESTful API 设计：

```
https://{host}          /{version}      /{resource}
https://api.deepseek.com  /v1             /chat/completions
       ↑ base_url              ↑ endpoint
```

`/v1` 是 API 版本号——大版本升级时变成 `/v2`，保证向后兼容。`/chat/completions` 是具体功能。OpenAI 还定义了 `/v1/embeddings`（文本向量化）、`/v1/models`（列出可用模型）等端点。

在 Hermes 配置中，`model.base_url` 只填根地址，endpoint 由代码自动拼接。Custom Provider 就是通过指定不同的 base_url 来接入任何 OpenAI 兼容服务。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 其他常用端点 | /v1/models（列出可用模型）、/v1/embeddings（文本向量化） |
| 中转站路径变体 | 部分中转站在 /v1 前加厂商前缀——不是标准 OpenAI 兼容 |
| trailing slash | base_url 末尾有无 / 差异——Hermes 自动拼接，不要自己带 /chat/completions |

### 使用原则
- base_url 只写到 /v1 或根地址，不要带 endpoint
- 切换中转站 = 改 base_url + key_env，其余代码不变


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[OpenAI 兼容 API]] — endpoint 路径定义来自此协议

### 组成 (part-of)
- [[Provider（模型提供商）]] — base_url 是每个 Provider 的核心配置项
- [[Custom Provider（自定义提供商）]] — 通过自定义 base_url 接入中转站

### ← 被指向
- [[API Key 认证]] (depends-on) — 认证信息在同一个 HTTP 请求中发送到此地址