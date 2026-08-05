---
name: FastAPI
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-后端工程
---

# FastAPI

## 类型判定
判别型 — Python 现代异步 Web 框架，AI 伴侣后端的「门面和调度中心」。

## 类比 ★
### 一句话比喻
FastAPI 像餐厅的前台经理——客人（前端）点什么菜（API 请求），经理立刻把任务分给厨房各个工位（LLM、Memory、数据库），做完后端回客人面前，全程不等不堵。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| FastAPI 路由（Router） | 前台经理手里的菜单——客人按菜单点，经理知道每个菜找哪个厨师 |
| AsyncIO 异步处理 | 经理不等一道菜做完再接下一位客人——同时处理 50 桌点单 |
| Pydantic 数据校验 | 经理看一眼点单就知道「这个菜没有」——在进厨房前拦住错误请求 |

## 是什么
FastAPI 是基于 Starlette 和 Pydantic 的 Python Web 框架，主打异步、自动文档生成（OpenAPI/Swagger）、类型安全。在 AI 伴侣架构中，它是后端服务的统一入口——接收前端请求、校验数据、调度模型推理、连接数据库和缓存，最后返回结果。

## 输入-输出空间
- **输入**: HTTP/WebSocket 请求（JSON body、路径参数、查询参数）
- **输出**: JSON 响应或流式数据（StreamingResponse / WebSocket）
- **核心特性**: 依赖注入（Depends）、中间件、后台任务（BackgroundTasks）

## 正例（≥2 个）
1. **AI 聊天接口**: `/chat` 接收用户消息 → 调用 LLM 服务 → 流式返回 SSE 或 WebSocket
2. **模型管理 API**: `/models` 列出可用模型、`/models/switch` 切换模型——FastAPI 做 RESTful 路由

## 反例/边界（≥1 个）
1. **Flask / Django 同步模式**: 传统同步框架高并发下容易阻塞——FastAPI 的 AsyncIO 才是 AI 应用的正确姿势
2. **边界 — CPU 密集型任务**: FastAPI 异步擅长 IO 等待，但图像处理/模型推理本身是 CPU 密集的，需要用 `run_in_executor` 丢到线程池或用 Celery 等任务队列

## 详细解释
FastAPI 的核心优势在 AI 场景中体现为三点：

1. **异步天然适配 AI 调用**: LLM API 调用是典型的 IO 等待（请求→等推理→收结果），FastAPI 用 `async def` + `await` 让一个线程能同时处理数百个请求
2. **自动文档**: 只要写好 Pydantic 模型和路由，Swagger UI 自动生成——前端开发者直接看文档对接
3. **WebSocket 原生支持**: 流式对话和实时通信不需要额外引入 Socket.IO

```python
@app.post("/chat")
async def chat(req: ChatRequest):
    # Pydantic 自动校验 req
    llm_response = await call_llm(req.messages)
    return StreamingResponse(llm_response, media_type="text/event-stream")
```

## 关系
### → 指向
- [[REST API]] — FastAPI 是实现 RESTful 接口的首选框架
- [[WebSocket]] — FastAPI 原生支持 WebSocket，承载流式对话
- [[SSE（Server-Sent Events）]] — StreamingResponse 实现 SSE 推送 LLM 输出
- [[AsyncIO]] — FastAPI 的异步能力建立在 AsyncIO 之上

### ← 被指向
- [[RAG]] — RAG 管道的在线阶段通过 FastAPI 接口暴露
- [[AI Agent]] — Agent 的工具调用和对话接口通过 FastAPI 路由
