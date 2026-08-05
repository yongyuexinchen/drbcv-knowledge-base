---
name: APIRouter模块化路由
type: procedure
status: core
source: "[[32-头条项目-模块化路由_原文]]"
domain: FastAPI
---

# APIRouter模块化路由

## 类型判定
procedure — 三步标准流程：创建 APIRouter 实例 → 写路由装饰器 → 在 main.py 注册挂载。

## 类比 ★
### 一句话比喻
模块化路由就像一个大公司分部门——news 部门管新闻接口，user 部门管用户接口，每个部门有自己的前台（APIRouter），互不干扰。客户（前端）来办事，先看门牌前缀（prefix），API/news 找新闻部，API/user 找用户部。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| APIRouter 实例 | 部门前台——该部门所有请求的第一个接待点 |
| prefix 前缀 | 部门门牌号——API/news、API/user 一眼就知道去哪个部门 |
| tags 分组 | 交互式文档里的折叠标签——点一下展开/收起该部门所有接口 |
| app.include_router() | 总公司花名册——把各部门正式注册，对外生效 |
| @router.get("/xxx") | 部门内部的具体工位——处理具体业务 |

## 是什么
模块化路由是 FastAPI 提供的路由拆分机制：用 `APIRouter` 代替 `app` 定义路由，按功能模块拆分到不同文件，最后在 main.py 中通过 `app.include_router()` 统一注册。解决了"所有路由堆在一个文件里又长又乱"的问题。

## 输入-输出空间（程序型必填）
- **输入**：各模块路由文件（如 routers/news.py），每个文件有一个 APIRouter 实例
- **输出**：main.py 通过 include_router 整合后，所有路由全局生效
- **前置条件**：`from fastapi import APIRouter`

## 核心代码 + 步骤表
```python
# ===== routers/news.py =====
from fastapi import APIRouter

# 第一步：创建 APIRouter 实例
router = APIRouter(
    prefix="/api/news",   # 路由前缀：该模块所有路径的前半部分
    tags=["news"]         # 分组名：交互式文档中可折叠
)

# 第二步：写路由（用 router 代替 app）
@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100):
    return {"code": 200, "message": "成功", "data": "新闻分类列表"}

@router.get("/list")
async def get_news_list():
    return {"code": 200, "message": "成功", "data": []}

# ===== main.py =====
from fastapi import FastAPI
from routers import news

app = FastAPI()

# 第三步：注册挂载
app.include_router(news.router)  # 注册新闻模块的路由
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 创建实例 | `router = APIRouter(prefix="/api/news", tags=["news"])` | prefix 是公共路径前缀，tags 是文档分组 |
| ② 写路由 | `@router.get("/categories")` | 用 router 代替 app，路径只写不同部分 |
| ③ 注册挂载 | `app.include_router(news.router)` | 在 main.py 中导入并注册，路由才生效 |

## 正例（≥2 个）
1. **新闻模块 + 用户模块**：routers/news.py 管理 `/api/news/*` 下所有接口，routers/users.py 管理 `/api/user/*` 下所有接口——各模块独立开发，互不影响。
2. **大型项目拆 10+ 模块**：电商项目按"商品、订单、支付、物流"拆成 4 个路由文件——每个文件只关注自己的业务逻辑。
3. **交互式文档自动分组**：加了 tags 后，Swagger 文档中每个模块的接口被折叠到一个组名下，点击展开/收起，找接口效率翻倍。

## 反例/边界（≥1 个）
1. **所有路由写在一个文件**：接口数量少（<5 个）时可以接受，但 20+ 接口堆在一个文件里，找路由改路由都像大海捞针——必须拆分。
2. **忘记 include_router**：路由文件写好了，装饰器也写了，但没在 main.py 注册——接口 404 找不到。这是最常见的"为什么路由不生效"原因。
3. **prefix 与路径重复**：prefix="/api/news"，装饰器又写 @router.get("/api/news/list")，最终路径变成 /api/news/api/news/list——重复了。

## 详细解释
`APIRouter` 实例的三个关键参数：
- **prefix**：路由前缀，该模块所有接口共有的路径开头。写法是 `prefix="/api/news"`，之后装饰器只需写 `/list`，最终路径自动拼接为 `/api/news/list`。
- **tags**：Swagger 交互式文档中的分组名，值为列表 `["news"]`，可写多个标签。
- **routes**：（通常在内部使用）存储该 router 下所有路由信息。

`app.include_router()` 本质是把 APIRouter 实例下所有路由"挂载"到 FastAPI 应用上，相当于告诉框架："这些路由现在可以接收请求了"。

## 关系
### → 指向
- [[FastAPI框架]] (APIRouter 是 FastAPI 的路由拆分工具)
- [[头条项目架构]] (模块化路由是项目架构中 routers/ 层的实现)
- [[获取新闻分类]] (新闻模块使用模块化路由定义接口)

### ← 被指向
- [[用户登录]] (使用模块化路由在 routers/users.py 中定义)
- [[获取用户信息]] (使用模块化路由在 routers/users.py 中定义)
