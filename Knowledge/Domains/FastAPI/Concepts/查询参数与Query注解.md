---
name: 查询参数与Query注解
type: procedure
status: core
source: "[[07-FastAPI基础入门-查询参数和Query类型注解_原文]]"
domain: FastAPI
---

# 查询参数与Query注解

## 类型判定
procedure — 三步流程：处理函数声明形参（自动解释为查询参数）→ 等号赋默认值 → Query() 添加额外校验。

## 类比 ★
### 一句话比喻
查询参数就像**外卖 APP 的筛选器**——URL 主路径是餐馆，`?` 后面的条件就像你勾选的"只看川菜"、"评分 4.5 以上"、"30 分钟内送达"。这些筛选条件都是可选的，不勾也能下单，勾了就更精准。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| URL `?` 后的参数 | 筛选器里勾选的条件——对结果做过滤/排序/分页 |
| `skip=0&limit=10` | "跳过前 0 条，只看 10 条" = 第 1 页 |
| 等号赋默认值 | 筛选器默认"综合排序"——你不改我就用这个 |
| Query() 范围限制 | 筛选器最多勾 100 个条件——防止你乱来 |
| `&` 拼接多个参数 | 多个筛选条件叠加——川菜 + 评分高 + 距离近 |

## 是什么
查询参数是出现在 **URL 问号之后**的键值对参数（`?key=value&key2=value2`），用于对数据进行过滤、排序、分页等操作。在 FastAPI 中，只需在处理函数中声明形参（不在路径中定义），形参自动被解释为查询参数。配合 `Query()` 函数可添加默认值、范围限制、描述等进阶校验。

## 输入-输出空间
- **输入**：URL 问号后的键值对（如 `?skip=10&limit=20`）
- **输出**：处理函数形参自动接收对应的值
- **前置条件**：`from fastapi import Query`（如需进阶校验）

## 核心代码
```python
from fastapi import FastAPI, Query

app = FastAPI()

# 基础查询参数：原生类型注解 + 默认值
@app.get("/news/list")
async def get_news_list(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
# 访问: /news/list?skip=20&limit=5

# Query() 进阶注解：校验 + 描述
@app.get("/news/list2")
async def get_news_list2(
    skip: int = Query(0, ge=0, lt=100, description="跳过的记录数"),
    limit: int = Query(10, le=100, description="返回的记录数")
):
    return {"skip": skip, "limit": limit}
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 声明形参 | `skip: int, limit: int` | 不在路径中定义，直接写在处理函数括号里 |
| ② 赋默认值 | `skip: int = 0` | 查询参数天生允许默认值，不传就用默认值 |
| ③ Query() 进阶校验 | `skip: int = Query(0, ge=0)` | 第一个参数是默认值，后续参数做校验 |
| ④ 添加描述 | `description="跳过的记录数"` | 显示在 Swagger 文档中 |

## 正例（≥2 个）
1. **新闻分页**：`/news/list?skip=20&limit=10` → 跳过前 20 条，返回第 21-30 条新闻。
2. **商品筛选**：`/products?category=electronics&min_price=100&max_price=500` → 筛选电子类 + 100-500 元区间的商品。
3. **搜索排序**：`/search?q=FastAPI&sort=date&order=desc` → 搜索"FastAPI"，按日期降序排列。

## 反例/边界（≥1 个）
1. **skip 传负数**：`?skip=-10` → 不报错但可能返回意外结果，应用 `ge=0` 限制。
2. **limit 过大**：`?limit=10000` → 一次返回 1 万条数据，内存可能爆炸，应用 `le=100` 限制上限。
3. **类型不匹配**：`skip` 注解为 `int`，但传 `?skip=abc` → FastAPI 返回 422 校验错误。

## 详细解释
**查询参数 vs 路径参数的选择**：
| | 路径参数 | 查询参数 |
|---|---|---|
| 出现位置 | URL 路径中 `/book/{id}` | URL 问号后 `?key=value` |
| 是否必填 | 默认必填 | 可选（有默认值即可选） |
| 用途 | 定位资源（"哪一个"） | 筛选/排序/分页（"怎么选"） |
| 示例 | `/user/123` | `/users?page=2&size=20` |

Query() 常用参数与 Path() 基本一致：`gt`/`ge`/`lt`/`le`（数值范围）、`min_length`/`max_length`（字符串长度）、`description`（文档描述）、`...`（标记必填）。

## 关系
### → 指向
- [[路径参数与Path注解]] (同级概念：查询参数 vs 路径参数)
- [[ORM分页查询]] (skip/limit 是分页查询的典型查询参数)
- [[FastAPI路由]] (查询参数在路由处理函数中使用)

### ← 被指向
- [[FastAPI路由]] (路由是查询参数的宿主)
- [[依赖注入]] (依赖项函数也可以接收查询参数)
