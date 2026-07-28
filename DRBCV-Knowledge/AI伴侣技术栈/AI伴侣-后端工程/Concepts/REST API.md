---
name: REST API
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-后端工程
---

# REST API

## 类型判定
判别型 — 基于 HTTP 的请求-响应式接口设计规范，客户端和服务器之间的「合同」。

## 类比 ★
### 一句话比喻
REST API 像自动售货机——你按一个按钮（GET /drinks/coke），机器吐一罐可乐给你（JSON 响应）。每次交互都是你发起、机器响应，交易完即结束，机器不会主动找你聊天。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| GET 请求 | 你按饮料按钮——只看看/读取，不改变机器里的存货 |
| POST 请求 | 你投币买饮料——创建了新资源（一笔交易记录） |
| PUT / DELETE | 管理员打开机器补货（更新）或撤掉过期饮料（删除） |

## 是什么
REST（Representational State Transfer）是一套 API 设计风格，核心原则：资源由 URL 标识、操作由 HTTP 方法表达（GET/POST/PUT/DELETE）、无状态（每个请求自包含）、响应通常为 JSON。在 AI 伴侣中，REST API 用于用户管理、模型配置、历史记录查询等无需实时双向通信的场景。

## 输入-输出空间
- **输入**: HTTP 请求（方法 + URL + Headers + Body）
- **输出**: HTTP 响应（状态码 + Headers + Body，通常 JSON）
- **方法语义**: GET=读取、POST=创建、PUT=全量更新、PATCH=部分更新、DELETE=删除

## 正例（≥2 个）
1. **获取用户配置**: `GET /users/me/profile` → 返回用户昵称、头像、偏好设置
2. **创建新对话**: `POST /conversations` with `{"title": "新对话"}` → 返回对话 ID 和创建时间

## 反例/边界（≥1 个）
1. **WebSocket 实时推送**: LLM 流式输出要求服务端主动推数据——REST 的请求-响应模型做不到，必须用 WebSocket 或 SSE
2. **边界 — 长轮询**: 有人用 REST + 长轮询模拟实时推送——能做到但浪费连接，不如直接用 WebSocket

## 详细解释
REST API 的核心是 **资源导向**。在 AI 伴侣系统中，典型资源包括：
- `/users` — 用户
- `/conversations` — 对话
- `/messages` — 消息
- `/memories` — 记忆
- `/agents` — Agent 配置

每个资源支持标准的 CRUD 操作，状态码表达结果（200=成功、201=创建成功、400=请求错误、401=未认证、404=未找到、500=服务端错误）。

与 WebSocket 的分工：REST 处理「查询/管理类」请求，WebSocket 处理「实时对话流」。

## 关系
### → 指向
- [[FastAPI]] — FastAPI 是构建 REST API 的 Python 框架
- [[Token认证 / JWT]] — REST API 的无状态特性依赖 Token 做身份验证

### ← 被指向
- [[RAG]] — RAG 服务通过 REST API 暴露检索端点
- [[AI Agent]] — Agent 管理接口（创建/配置/启停）通过 REST API
