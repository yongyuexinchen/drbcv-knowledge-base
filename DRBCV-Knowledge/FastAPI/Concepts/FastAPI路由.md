---
name: FastAPI路由
type: procedure
status: core
source: "[[04-FastAPI基础入门-路由_原文]]"
domain: FastAPI
---

# FastAPI路由

## 类型判定
procedure — 三步写路由：装饰器声明请求方法和路径 → 定义异步处理函数 → return 响应结果。

## 类比 ★
### 一句话比喻
FastAPI 路由就像**餐厅菜单**——每个 URL 是一道菜名，装饰器（`@app.get` / `@app.post`）决定了这道菜是"现成的"（GET 查询）还是"现做的"（POST 提交），客人点哪个路径，厨房（服务器）就上哪道菜。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 路由（URL 路径） | 菜单上的菜名——`/hello` 是一道菜，`/user/hello` 是另一道菜 |
| 装饰器 `@app.get("/hello")` | 标注这道菜的做法：GET = 直接端上来，POST = 需要客人给材料 |
| 处理函数（async def） | 后厨炒菜的动作——收到订单后执行什么逻辑 |
| return 响应结果 | 服务员端上桌的菜——客人最终收到的东西 |
| `/docs` Swagger 文档 | 餐厅门口的触摸屏自助点餐机——不用喊服务员就能试每道菜 |

## 是什么
路由是 **URL 地址与处理函数之间的映射关系**。在 FastAPI 中，通过装饰器 `@app.请求方法("路径")` 将特定 URL 绑定到一个异步函数上，当客户端访问该 URL 时，服务器执行该函数并返回结果。

## 输入-输出空间
- **输入**：HTTP 请求（包含请求方法 + URL 路径 + 可选参数）
- **输出**：处理函数的 return 值（Python 对象，FastAPI 自动转为 JSON）
- **前置条件**：已创建 FastAPI 实例 `app = FastAPI()`

## 核心代码
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")                      # 装饰器：GET 方法 + 根路径
async def root():                   # 处理函数（异步）
    return {"message": "Hello World"}  # 响应结果

@app.get("/hello")                  # 另一个路由
async def get_hello():
    return {"msg": "你好，FastAPI"}
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 写装饰器 | `@app.get("/hello")` | 声明请求方法（GET）和路径（`/hello`） |
| ② 定义处理函数 | `async def get_hello():` | 异步函数，函数名自定义 |
| ③ 返回响应 | `return {"msg": "..."}` | 返回 Python 对象，FastAPI 自动转 JSON |

## 正例（≥2 个）
1. **新闻首页**：`@app.get("/news/list")` → 返回新闻列表 JSON 数据。
2. **用户注册**：`@app.post("/register")` → POST 方法，接收表单数据创建用户。
3. **删除文章**：`@app.delete("/article/{id}")` → DELETE 方法，删除指定 ID 的文章。

## 反例/边界（≥1 个）
1. **装饰器写错实例名**：如果 FastAPI 实例叫 `app`，但装饰器写成 `@application.get(...)`——名称不匹配，路由不会注册。
2. **请求方法错误**：接口定义了 `@app.get("/register")` 但前端用 POST 请求——返回 405 Method Not Allowed。

## 详细解释
支持的 HTTP 请求方法：`@app.get()`、`@app.post()`、`@app.put()`、`@app.delete()`、`@app.patch()` 等，覆盖 RESTful API 的全部操作。

装饰器本质是 Python 的语法糖——`@app.get("/hello")` 等价于 `app.get("/hello")(get_hello)`，FastAPI 内部维护了一张路由表，收到请求时查表找到对应函数执行。

## 关系
### → 指向
- [[路径参数与Path注解]] (路径参数定义在路由的 URL 中)
- [[查询参数与Query注解]] (查询参数在处理函数形参中声明)
- [[请求体参数与Field注解]] (请求体参数配合 POST/PUT 路由)
- [[响应类型]] (路由的返回值决定响应类型)

### ← 被指向
- [[FastAPI导学]] (路由是框架基础的核心概念)
- [[依赖注入]] (依赖注入在路由处理函数中使用)
