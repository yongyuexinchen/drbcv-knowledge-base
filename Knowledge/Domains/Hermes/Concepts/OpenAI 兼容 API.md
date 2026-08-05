---
name: OpenAI 兼容 API
type: system
status: core
source: "[[Hermes教程-模块五-实战篇]]"
domain: hermes
---

# OpenAI 兼容 API

## 类型判定
系统型 — 它是一套完整的协议规范，定义了 LLM 服务端和客户端之间的通信格式。

## 是什么
OpenAI 在 2023 年发布的 Chat Completions API 已成为事实上的行业标准协议。任何实现了 `POST /v1/chat/completions` 端点、接受相同 JSON 请求格式、返回相同响应格式的 API 服务，都称为"OpenAI 兼容 API"。DeepSeek、硅基流动、Together AI、Ollama、vLLM——全都兼容这套协议。

## 输入-输出空间
**输入**：`POST /v1/chat/completions`，JSON body 包含 `model`（模型名）、`messages`（对话历史数组，每条含 role + content）、`temperature`、`max_tokens`、`stream` 等参数。
**输出**：JSON 响应，`choices[0].message.content` 为模型回复文本，`usage` 含 prompt_tokens / completion_tokens / total_tokens。

## 正例（≥2个）
- DeepSeek 官方 API：`https://api.deepseek.com/v1/chat/completions`，完全兼容，开发者在 OpenAI SDK 里改 `base_url` 即可切换
- 硅基流动：`https://api.siliconflow.cn/v1/chat/completions`，承载 DeepSeek/Qwen/GLM 等模型，统一 OpenAI 格式
- Ollama 本地模型：`http://localhost:11434/v1/chat/completions`，本地 Llama 也走同一套协议

## 反例/边界（≥1个）
- Anthropic Messages API（`/v1/messages`）：不是 OpenAI 兼容，请求/响应格式不同，需要专门的 SDK
- Google Gemini API（`generateContent`）：自有一套协议，不走 `/v1/chat/completions`
- 纯 gRPC 推理服务（如 Triton Inference Server）：不兼容，没有 REST 端点

## 详细解释
OpenAI Chat Completions API 定义了三个核心约定：

1. **端点约定**：`/v1/chat/completions`。`/v1` 是版本前缀，`/chat/completions` 是聊天补全资源。
2. **请求格式**：JSON，核心字段是 `messages` 数组——每条消息有 `role`（system/user/assistant/tool）和 `content`。
3. **响应格式**：`choices[0].message.content` 是文本回复。`usage` 报告 token 消耗。

这个协议的威力在于**互操作性**——任何兼容此协议的客户端（OpenAI Python SDK、LangChain、Hermes Agent）可以无缝切换任何兼容此协议的服务端，只需改 `base_url` 和 `api_key`。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| tool_choice 参数 | 控制模型是否强制调用工具：auto（自主）/ required（必须调）/ none（禁止）/ 指定工具名 |
| Function Calling 格式 | 工具定义通过 tools 数组传入，每个含 type:function + name/description/parameters（JSON Schema） |
| response_format | {"type": "json_object"} 强制 JSON 输出；{"type": "json_schema"} 按指定 schema 输出 |

### 使用原则
- 始终用 /v1/chat/completions，不要用旧版 /v1/completions
- /v1 是 URL 路径，不是 HTTP header
- 不同厂商 model 字段格式不同：gpt-5-mini（OpenAI）、deepseek-ai/DeepSeek-V4-Pro（硅基流动/OpenRouter）


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Base URL + Endpoint]] — API 地址由 base_url + 固定端点路径构成
- [[API Key 认证]] — 请求通过 Authorization 头认证

### 实现 (implements)
- [[Provider（模型提供商）]] — 每个 Provider 提供此协议的实现
- [[Custom Provider（自定义提供商）]] — 中转站通过实现此协议接入 Hermes

### ← 被指向
- [[Streaming（流式响应）]] (depends-on) — Streaming 是此协议的可选模式
- [[Token 计费]] (depends-on) — 计费数据来自此协议的 `usage` 字段
- [[Tool／Toolset（工具集）]] (depends-on) — Agent 的工具调用通过此协议的 `tools` 参数传递