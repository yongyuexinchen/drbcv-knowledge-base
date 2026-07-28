---
name: 请求体参数与Field注解
type: procedure
status: core
source:
  - "[[08-FastAPI基础入门-请求体参数_原文]]"
  - "[[09-FastAPI基础入门-请求体参数_Field类型注解_原文]]"
domain: FastAPI
---

# 请求体参数与Field注解

## 类型判定
procedure — 三步标准流程：定义 Pydantic 模型（继承 BaseModel）→ 处理函数形参用该模型做类型注解 → Field() 添加字段级校验。

## 类比 ★
### 一句话比喻
请求体参数就像**快递包裹里的物品清单**——路径参数是快递单上的门牌号（运到哪），查询参数是筛选条件（选哪个快递公司），而请求体参数是箱子里面实际装的东西（用户名、密码、订单详情）。这些数据藏在 HTTP 消息体里，不像 URL 那样暴露在外，也更安全。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| BaseModel 鸡肋 | 物品清单的标准模板——固定格式："品名 + 数量 + 规格" |
| 自定义类（继承 BaseModel） | 你填好的清单——用户名、密码、邮箱 |
| `user: User` 类型注解 | 把清单交给快递员——告诉服务器"按这个格式接收" |
| Field() 校验 | 清单上的约束——"密码至少 6 位"、"用户名不能为空" |
| 消息体（Body） | 包裹箱子——数据藏在里面，URL 上看不到 |

## 是什么
请求体参数是客户端通过 HTTP 请求的**消息体（Body）**发送给服务器的数据，用于创建或更新资源（如注册用户、新增图书）。在 FastAPI 中，先基于 Pydantic 的 `BaseModel` 定义数据模型，然后在处理函数中用该模型做类型注解。`Field()` 函数从 `pydantic` 导入，用于添加默认值、长度限制、数值范围和描述等字段级校验。

## 输入-输出空间
- **输入**：HTTP 请求体中的 JSON 数据（`{"username": "张三", "password": "123456"}`）
- **输出**：处理函数中对应形参接收的 Pydantic 模型实例
- **前置条件**：`from pydantic import BaseModel, Field`

## 核心代码
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 第一步：定义数据模型
class User(BaseModel):
    username: str = Field(..., min_length=2, max_length=10, description="用户名")
    password: str = Field(..., min_length=3, max_length=20, description="密码")

class Book(BaseModel):
    title: str = Field(..., min_length=2, max_length=20, description="书名")
    author: str = Field(..., min_length=2, max_length=10)
    publisher: str = Field("黑马出版社", description="出版社")
    price: float = Field(..., gt=0, description="售价")

# 第二步：类型注解
@app.post("/register")
async def register(user: User):           # 用 User 模型做类型注解
    return user                           # 直接返回 Pydantic 对象

@app.post("/book")
async def add_book(book: Book):           # 用 Book 模型做类型注解
    return book
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 定义模型 | `class User(BaseModel):` | 继承 `BaseModel`，声明属性和类型 |
| ② Field() 校验 | `username: str = Field(..., min_length=2)` | `...`=必填，后可跟长度/范围/默认值/描述 |
| ③ 类型注解 | `async def register(user: User):` | 处理函数形参用模型类做类型注解 |
| ④ 发请求 | POST JSON body | 数据藏在消息体（Body）中，不在 URL 里 |

## 正例（≥2 个）
1. **用户注册**：POST `/register` — Body 携带 `{"username": "张三", "password": "123456"}`，服务器创建用户。
2. **新增图书**：POST `/book` — Body 携带 `{"title": "Python入门", "author": "李明", "publisher": "黑马出版社", "price": 59.9}`，录入新书。
3. **修改用户信息**：PUT `/user/123` — Body 携带新资料，路径参数定位用户，请求体提供更新的数据。

## 反例/边界（≥1 个）
1. **字段缺失**：模型定义了 `title: str = Field(...)`（必填），但请求体没传 `title` → 返回 422 校验错误。
2. **字段长度越界**：`min_length=2` 限制下传 `"A"` → 报错 "string too short"，应至少 2 字符。
3. **数值范围越界**：`price: float = Field(gt=0)`，但传 `price: -10` → 报错，因为 `gt=0` 要求大于 0。
4. **GET 请求用了请求体参数**：GET 请求通常不带 Body，如果处理函数声明了 Pydantic 模型形参，FastAPI 可能会将其误解为查询参数，应使用 POST/PUT/PATCH。
5. **Field() 导入错误**：`Field` 来自 `pydantic`（不是 `fastapi`），写错导入路径会报 `ImportError`。

## 详细解释
三种参数对比总结：
| | 路径参数 | 查询参数 | 请求体参数 |
|---|---|---|---|
| 出现位置 | URL 路径中 `/book/{id}` | URL 问号后 `?key=value` | HTTP Body |
| 典型方法 | GET | GET | POST / PUT / PATCH |
| 用途 | 定位资源 | 筛选/排序/分页 | 提供数据 |
| 类型注解函数 | Path() | Query() | Field() |
| 导入来源 | `fastapi` | `fastapi` | `pydantic` |
| 安全性 | 低（暴露在 URL） | 低（暴露在 URL） | 较高（藏在 Body） |

Field() 常用参数：`...`（必填）、`default`（默认值）、`gt`/`ge`/`lt`/`le`（数值范围）、`min_length`/`max_length`（字符串长度）、`description`（字段描述）。

## 关系
### → 指向
- [[路径参数与Path注解]] (同级概念：三种参数对比)
- [[查询参数与Query注解]] (同级概念：三种参数对比)
- [[请求体参数与Field注解]] (Python 类型系统是 Pydantic 的基础)
- [[自定义响应格式]] (响应的 response_model 也基于 Pydantic 模型)

### ← 被指向
- [[FastAPI路由]] (请求体参数配合 POST/PUT 路由使用)
- [[依赖注入]] (依赖项也可用于复用请求体校验逻辑)
