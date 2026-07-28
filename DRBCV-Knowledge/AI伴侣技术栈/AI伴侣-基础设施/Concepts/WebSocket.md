---
name: WebSocket
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-基础设施
---

# WebSocket

## 类型判定
判别型 — 实时双向通信协议，AI 伴侣的「神经系统」。

## 类比 ★
### 一句话比喻
HTTP 像寄信——你寄一封，对方回一封，每次都要重新写地址。WebSocket 像打电话——拨通之后，双方可以随时说话，直到挂断。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| WebSocket 全双工 | 打电话——双方同时能说能听，一条线路持续通话 |
| HTTP 请求-响应 | 寄挂号信——每次都要重新写地址等回信 |
| Handshake（握手） | 拨号接通的那一瞬间——之后就是持续通话 |

## 是什么
WebSocket 是建立在 TCP 之上的全双工通信协议。它通过一次 HTTP 握手升级为 WS 协议，之后客户端和服务端可以在**同一条连接**上互相推送消息，无需像 HTTP 那样每次都发起新请求。延迟从 HTTP 的几百毫秒（含连接建立）降到 WebSocket 的几毫秒。

## 输入-输出空间
- **输入**: 客户端发起的 HTTP Upgrade 请求（握手阶段）；之后是二进制或文本消息帧
- **输出**: 服务端同意升级返回 101 Switching Protocols（握手阶段）；之后是双向持续的消息流
- **生命周期**: 握手 → 连接保持（可心跳保活）→ 任一端关闭

## 正例（≥2 个）
1. **AI 聊天应用**: 用户发消息 → WebSocket 推给 FastAPI → LLM 流式返回 → WebSocket 逐 token 推给前端
2. **在线协作**: 多人同时编辑文档，每个操作通过 WebSocket 实时广播给其他用户

## 反例/边界（≥1 个）
1. **REST API 查询**: 客户端请求一次、服务端响应一次就结束——WebSocket 是杀鸡用牛刀，HTTP 更合适
2. **SSE（Server-Sent Events）**: SSE 也能做服务端推送，但它只支持单向（Server→Client），客户端发消息仍需 HTTP——如果只需要推送（如 ChatGPT 流式输出），SSE 更简单
3. **边界 — 连接断开**: WebSocket 不像 HTTP 天然无状态，断开后需要客户端重连 + 服务端恢复状态

## 详细解释
WebSocket 协议握手：
```
客户端: GET /chat HTTP/1.1
        Upgrade: websocket
        Connection: Upgrade

服务端: HTTP/1.1 101 Switching Protocols
        Upgrade: websocket
        Connection: Upgrade
```
握手之后，同一条 TCP 连接切换为 WebSocket 帧协议，双方可以随时发送消息。

在 AI 伴侣架构中，WebSocket 是前端和后端之间的「实时通道」：
```
[前端 Chat UI] ←→ WebSocket ←→ [FastAPI 服务] ←→ [LLM / Memory / Agent]
```
它承载流式对话（LLM 逐 token 输出）、语音实时交互、状态同步等核心场景。

## 关系
### → 指向
- [[SSE（Server-Sent Events）]] — SSE 是 WebSocket 的轻量替代，适合纯服务端推送场景
- [[FastAPI]] — FastAPI 原生支持 WebSocket，是 AI 伴侣后端的常见选择

### ← 被指向
- [[AI Agent]] — Agent 的实时交互依赖 WebSocket 通道
- [[Streaming TTS]] — 流式语音合成通过 WebSocket 推送音频帧
