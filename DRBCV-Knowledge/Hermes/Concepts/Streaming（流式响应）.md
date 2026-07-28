---
name: Streaming（流式响应）
type: discriminant
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
---

# Streaming（流式响应）

## 类型判定
判别型 — 它分开了两种根本不同的用户体验模式：一个字一个字蹦出来 vs 等几秒全出来。

## 是什么
Streaming 是 LLM API 的一种响应模式。请求中传 `stream: true` 时，服务端通过 **SSE（Server-Sent Events）** 协议逐 token 推送生成结果，每个 token 到达时客户端立即渲染。非流式模式下，服务端生成完所有 token 后一次性返回。

## 输入-输出空间
**输入**：`stream: true/false` 开关
**输出**：
- `stream=true`：SSE 事件流，每个 `data:` 行带一个 `delta`（增量 token），最终以 `[DONE]` 结束
- `stream=false`：一个完整 JSON 响应，`choices[0].message.content` 为全部文本

## 正例（≥2个）
- ChatGPT 的逐字输出：典型的 SSE 流式渲染，用户体验好（不用等）
- Hermes Desktop 的流式对话：每产生一个 token 就显示，包括推理过程（`show_reasoning: true`）
- 命令行 `hermes chat -q "..."` 也是流式：终端逐字打印

## 反例/边界（≥1个）
- 非流式更适合批量/脚本场景：`hermes chat -q "翻译这段文本"` 脚本调用时不需要流式，等一个完整结果更简单
- 中转站可能不支持流式：有些廉价中转站只支持非流式
- 流式下 `usage` 统计可能不完整或延迟：部分厂商在流式最后一个 chunk 才补 `usage`

## 详细解释
SSE 协议格式：
```
data: {"choices":[{"delta":{"content":"你"}}]}
data: {"choices":[{"delta":{"content":"好"}}]}
data: [DONE]
```

Hermes 的 `/verbose` 命令可以控制工具执行和推理过程是否显示——这在流式模式下决定你能看到多少细节。

流式 vs 非流式的选择：
| 场景 | 推荐 |
|------|------|
| 用户聊天界面 | stream=true |
| 脚本/批量处理 | stream=false |
| 需要精确 token 统计 | stream=false |
| 中转站不支持 | stream=false |

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| SSE 格式 | data: {"choices":[{"delta":{"content":"好"}}]}\n\n |
| stream_options | {"include_usage": true} → 流式最后一个 chunk 包含 usage |
| tool call streaming | 工具调用参数可流式返回——delta.tool_calls[0].function.arguments |
| [DONE] 终止符 | 流式结束标志，非 JSON，客户端需特殊处理 |

### 使用原则
- 聊天界面始终用 stream=true
- 脚本/批量用 stream=false（一次拿完整结果）
- 有些廉价中转站不支持流式 → 先测试


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[OpenAI 兼容 API]] — SSE 流式是此协议的扩展模式

### ← 被指向
- [[Gateway（消息网关）]] (depends-on) — 消息平台需要流式转发给用户