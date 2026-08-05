---
name: CORS跨域解决
type: procedure
status: core
source: "[[36-头条项目-解决跨域问题_原文]]"
domain: FastAPI
---

# CORS跨域解决

## 类型判定
procedure — 添加 CORSMiddleware 中间件两步搞定：导入 → app.add_middleware() 全局配置。

## 类比 ★
### 一句话比喻
CORS 跨域就像小区门禁系统——同住一栋楼的业主（同源）可以自由进出，外来访客（跨域）需要门卫登记授权（CORSMiddleware）才能进。FastAPI 内置的 CORSMiddleware 就是这个门禁系统的总开关。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 同源（协议+域名+端口一致） | 同一栋楼的业主——自由进出，不拦 |
| 跨域（任意一项不同） | 外来访客——门禁拦截，需要授权 |
| CORSMiddleware | 物业管理处的门禁授权系统 |
| allow_origins=["*"] | 开发模式：所有访客都放行（上线要改！） |
| allow_methods=["*"] | 所有通行方式都允许：走路、开车、骑车 |
| allow_headers=["*"] | 随身携带的任何证件都认 |

## 是什么
CORS（Cross-Origin Resource Sharing，跨域资源共享）是浏览器的安全机制：要求前后端"同源"才能正常发请求。同源指协议、域名、端口三者完全一致。当前端 Vue（localhost:5173）和后端 FastAPI（127.0.0.1:8000）域名和端口都不同时，浏览器会拦截请求。解决方式是添加 FastAPI 内置的 `CORSMiddleware` 中间件，全局授权允许跨域访问。

## 输入-输出空间（程序型必填）
- **输入**：CORSMiddleware 配置参数（允许的源、方法、请求头等）
- **输出**：所有接口不再被浏览器 CORS 策略拦截，前端可以正常发请求
- **前置条件**：`from fastapi.middleware.cors import CORSMiddleware`

## 核心代码 + 步骤表
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 第一步：添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # 允许访问的源（开发用 *，上线要改）
    allow_credentials=True,           # 允许携带 Cookie
    allow_methods=["*"],              # 允许的请求方法（GET/POST/PUT/DELETE...）
    allow_headers=["*"],              # 允许的请求头（含 Authorization 放 Token）
)
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 导入 | `from fastapi.middleware.cors import CORSMiddleware` | FastAPI 内置，无需安装 |
| ② 添加中间件 | `app.add_middleware(CORSMiddleware, ...)` | 在 main.py 全局配置即可 |

## 正例（≥2 个）
1. **Vue + FastAPI 前后端分离**：前端 localhost:5173，后端 127.0.0.1:8000——域名和端口都不同，添加 CORS 中间件后新闻分类、列表等所有接口正常访问。
2. **生产环境精确授权**：上线时 `allow_origins=["https://myapp.com"]` 只允许自己的域名——防止其他网站恶意调用接口。
3. **带 Token 的跨域请求**：用户登录后 Token 放在 Authorization 请求头——`allow_headers=["*"]` 确保浏览器不拦截这个自定义头。

## 反例/边界（≥1 个）
1. **开发时没配 CORS 中间件**：前端页面所有接口请求被浏览器拦截，控制台疯狂报 `has been blocked by CORS policy`——添加中间件后立即解决。
2. **上线时 allow_origins 还写 `["*"]`**：任何人都能调用你的 API——安全风险极高。必须替换为实际的前端域名列表。
3. **协议不同也算跨域**：前端 `https://localhost`，后端 `http://localhost`——协议不同，也算跨域。注意协议也需一致。

## 详细解释
**同源的三个条件**（必须同时满足）：
- **协议相同**：都是 http 或都是 https
- **域名相同**：都是 localhost 或都是 127.0.0.1（注意：localhost 和 127.0.0.1 在浏览器眼中是不同的域名！）
- **端口相同**：都是 8000 或都是 5173

**中间件 vs 依赖注入**：
- 中间件：对所有请求自动生效（CORS、日志、全局异常 → 用中间件）
- 依赖注入：由路由按需声明才生效（数据库会话、分页参数、用户认证 → 用 Depends）

CORSMiddleware 四个核心参数：
- `allow_origins`：允许哪些前端域名访问（最重要）
- `allow_credentials`：是否允许携带 Cookie（前后端分离一般需要开）
- `allow_methods`：允许哪些 HTTP 方法
- `allow_headers`：允许哪些自定义请求头

## 关系
### → 指向
- [[头条项目架构]] (CORS 是前后端分离架构的必经之路)
- [[FastAPI框架]] (中间件是 FastAPI 的核心机制)
- [[依赖注入]] (中间件 vs 依赖注入的取舍对比)

### ← 被指向
- [[获取新闻分类]] (分类接口是第一个需要解决跨域才能正常访问的接口)
- [[新闻模块总结]] (新闻模块的功能验证依赖 CORS 配置)
