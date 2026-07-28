---
name: ASGI协议与前后端分离架构
type: discriminant
status: core
source: "[[ASGI协议和服务_原文]] / [[Web开发模式相关概念_原文]]"
domain: FastAPI
---

# ASGI协议与前后端分离架构

## 类型判定
discriminant — 核心区分：WSGI 是同步快递员（一次只能送一单），ASGI 是异步快递员（等签收时还能送别的）；前后端分离是把"做菜"和"端盘子"拆成两个团队。

## 类比 ★
### 一句话比喻
WSGI 就像**老式银行柜台**——一个柜员一次只能服务一个客户，后面的全排队干等。ASGI 则是**自助餐厅+叫号系统**——柜员递完单号就去服务下一个人（异步非阻塞），客户等叫号时还能玩手机（不阻塞）。前后端分离就像**把厨房和餐厅拆开**：后厨（后端 API）只管按菜单做菜并递出窗口，至于菜是端到堂食（网页）、外卖（APP）还是打包（小程序），后厨一概不管——谁拿到菜、在哪摆盘，那是前端的事。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| WSGI（同步网关） | 老式银行柜台——一个柜员 = 一个客户，后面的全排队 |
| ASGI（异步网关） | 自助叫号系统——发号就走，等叫号时不占柜员 |
| Uvicorn（ASGI 服务器） | 叫号机硬件——负责高效派号（处理请求分发） |
| Nginx（Web 服务器） | 银行大堂经理——先接待客户，决定转给柜台还是直接给宣传册 |
| 前后端分离 | 厨房和餐厅分开——后厨只管做菜（API），餐厅只管摆盘（前端） |
| RESTful API | 标准化菜单——GET=看菜单，POST=下单，PUT=改单，DELETE=退单 |
| 静态文件服务器 | 自助取餐柜——CSS/JS/图片放那儿，谁要自己取 |

## 是什么
**ASGI**（Asynchronous Server Gateway Interface）是 Python Web 应用与服务器之间的**异步通信协议**，是 WSGI 的异步升级版。FastAPI 天生基于 ASGI，配合 Uvicorn 服务器实现高并发。**前后端分离**是现代 Web 开发的主流模式：后端只负责提供数据（通过 API 返回 JSON），前端独立负责界面渲染（HTML/CSS/JS），两者通过 HTTP 协议通信，可独立开发、独立部署。

## 正例（≥2 个）
1. **高并发场景**：新闻 APP 每日百万级请求，FastAPI + ASGI + Uvicorn 的异步架构在等待数据库查询时不阻塞其他请求，吞吐量远超同步框架。
2. **多端复用后端**：同一套 FastAPI 接口同时服务 Web 网页、iOS APP、Android APP、微信小程序——后端只返回 JSON，各端自行渲染界面。
3. **团队并行开发**：前端团队和后端团队只要约定好 API 接口格式（JSON 结构），就可以同时开工，不需要等对方完成。

## 反例/边界（≥1 个）
1. **前后端不分离项目中用 FastAPI**：FastAPI 虽然也能做模板渲染（通过 Jinja2），但这并非它的设计初衷——如果项目需要大量服务端渲染 HTML 页面，Django 更合适。
2. **把 Uvicorn 直接暴露到公网**：Uvicorn 不应直接作为面向公网的服务器，前面应加 Nginx 做反向代理、负载均衡和静态文件服务。
3. **CPU 密集型任务误用异步**：异步收益来自 IO 等待，纯计算任务（如图片处理）不会因为加了 async 就变快。

## 详细解释

### ASGI vs WSGI
| | WSGI | ASGI |
|---|---|---|
| 全称 | Web Server Gateway Interface | Asynchronous Server Gateway Interface |
| 模型 | 同步（一个请求 = 一个线程） | 异步（async/await 协程） |
| 并发能力 | 受线程数限制 | 可处理数千并发连接 |
| 代表框架 | Flask, Django（默认） | FastAPI, Django 3.2+ |
| 服务器 | Gunicorn, uWSGI | **Uvicorn**, Hypercorn, Daphne |

### 前后端分离的核心架构
```
浏览器 ──→ Nginx（端口 80/443）
              ├──→ 静态文件（前端 HTML/CSS/JS）
              └──→ Uvicorn（FastAPI 后端，端口 8000）
                        └──→ 数据库
```

### RESTful API 的五个核心动作
| HTTP 方法 | 操作 | URL 示例 | 含义 |
|-----------|------|---------|------|
| GET | 查询 | `/students` | 获取所有学生 |
| GET | 查询 | `/students/5` | 获取 ID=5 的学生 |
| POST | 新增 | `/students` | 添加一个学生 |
| PUT | 修改 | `/students/5` | 修改 ID=5 的学生 |
| DELETE | 删除 | `/students/5` | 删除 ID=5 的学生 |

## 关系
### → 指向
- [[FastAPI框架]] (FastAPI 是 ASGI 框架的代表实现)
- [[路由装饰器元数据与启动方式]] (uvicorn 是 ASGI 服务器，用于启动 FastAPI)
- [[FastAPI路由]] (RESTful 风格通过路由的 HTTP 方法实现)

### ← 被指向
- [[FastAPI框架]] (ASGI 是 FastAPI 的底层协议依赖)
