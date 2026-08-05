---
name: FastAPI框架
type: discriminant
status: core
source: "[[02-FastAPI基础入门-FastAPI框架简介_原文]]"
domain: FastAPI
---

# FastAPI框架

## 类型判定
discriminant — 定义 FastAPI 是什么、它和同类框架的根本差异在哪。

## 类比 ★
### 一句话比喻
FastAPI 就像一个装了涡轮增压的快递站——别人的快递员一次只能送一个包裹（同步阻塞），FastAPI 的快递员能在等一个客户签收的同时，扭头去送下一个包裹（异步非阻塞），所以同样的时间送出 1000 倍的货。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 同步请求 | 快递员等客户签收完才送下一单——堵在门口干等 |
| 异步请求 | 快递员把包裹放下就走，同时接 1000 单——不等签收 |
| Uvicorn 服务器 | 快递站的调度中心，高性能派单引擎 |
| Swagger 交互式文档 | 快递站门口的自动查询机，不用人工问就能试 |
| Pydantic 类型校验 | 自动分拣机——包裹不合规格当场退回，不用人工检查 |

## 是什么
FastAPI 是一个基于 Python 的**高性能异步 Web 框架**，用于快速构建 API 接口服务。核心卖点：天生异步（基于 ASGI）、自动类型校验（Pydantic）、自动生成可交互式 API 文档（Swagger UI）。

## 正例（≥2 个）
1. **高并发 API 服务**：新闻资讯类接口每天百万级请求，FastAPI 异步非阻塞天然适合。
2. **AI 模型部署**：大模型推理是典型 IO 密集型任务，FastAPI 可以在等待模型返回时处理其他请求，不会阻塞。
3. **前后端分离项目**：前端只需调 API，FastAPI 自动生成的 `/docs` 文档让前后端联调无需 Postman。

## 反例/边界（≥1 个）
1. **纯 CPU 密集型计算**：异步的优势在于 IO 等待，如果是纯数学计算（如循环一万次浮点运算），异步不会加速——因为 CPU 一直在忙，没有"等待"可切换。
2. **不是 Django 替代品**：FastAPI 没有自带 ORM、后台管理、模板引擎——它只做 API，全栈项目需要搭配 SQLAlchemy 等。

## 详细解释
FastAPI 的两个核心差异：
- **异步（Async）**：基于 Python `async/await` + ASGI 协议（Uvicorn 服务器）。遇到 IO 等待时不阻塞，切换到其他请求。对比 Flask/Django 的同步 WSGI，高并发场景性能差距可达 10-100 倍。
- **Pydantic 类型系统**：定义数据模型后，FastAPI 自动完成请求参数的校验、类型转换、文档生成。程序员不用手写 `if not isinstance(...)` 判空判类型的代码。

## 关系
### → 指向
- [[Uvicorn服务器]] (FastAPI 的运行载体)
- [[Pydantic类型校验]] (FastAPI 的数据验证引擎)
- [[ASGI协议]] (FastAPI 的底层通信协议)

### ← 被指向
- [[FastAPI路由]] (路由定义在 FastAPI 实例上)
- [[FastAPI项目创建与运行]] (创建的就是 FastAPI 应用实例)
