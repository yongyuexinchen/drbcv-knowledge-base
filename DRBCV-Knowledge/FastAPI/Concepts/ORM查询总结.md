---
name: ORM查询总结
type: discriminant
status: core
source: "[[25-FastAPI进阶-ORM操作数据-查询总结_原文]]"
domain: FastAPI
---

# ORM查询总结

## 类型判定
discriminant — 一张全景图对比五种查询模式：select 基本查询、条件查询、聚合查询、分页查询、get 主键查询。

## 类比 ★
### 一句话比喻
ORM 的五种查询模式就像图书馆的五种找书方式——你可以按分类浏览所有书架（`select`），也可以按"作者是曹雪芹"的条件检索（`where`），还能统计馆藏总数（聚合），或者指定"第 3 页每页 20 本"翻着看（分页），当然也能直接报索书号精准取一本（`get`）。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| `select(Model)` | 把所有书架看一遍——全表扫描 |
| `where(...)` | 只逛"中国古典文学"区——条件过滤 |
| `func.count()` | 数一数这个区有多少本书——统计 |
| `.offset().limit()` | 从第 3 层第 5 本书开始取 10 本——分页 |
| `db.get(Model, id)` | 直接报索书号 I247.5/5514——精准定位 |

## 是什么
ORM 查询（基于 SQLAlchemy 2.0）提供了五种查询模式来覆盖从简单到复杂的所有数据检索场景。核心入口是 `select()` + `db.execute()`，提取数据用 `scalars()` 系列方法。

## 五种查询模式全景图

| # | 查询模式 | 核心写法 | 典型场景 | 返回类型 |
|---|---------|---------|---------|---------|
| ① | **基本查询** | `select(Model)` | 查全部、查第一条 | ORM 对象列表 / 单个对象 |
| ② | **条件查询** | `select(Model).where(...)` | 筛选、搜索、过滤 | ORM 对象列表 |
| ③ | **聚合查询** | `select(func.方法(Model.attr))` | 统计：总数、总额、均价 | 单个数字（标量） |
| ④ | **分页查询** | `select(Model).offset(n).limit(m)` | 列表翻页、无限滚动 | ORM 对象列表 |
| ⑤ | **主键查询** | `db.get(Model, id)` | 详情页、单条精确查找 | 单个 ORM 对象或 None |

## 统一执行流程
```
select(...)        →  构建 ORM 查询语句（不执行）
db.execute(stmt)   →  异步执行，返回 Result 对象
result.scalars()   →  从 Result 中提取 ORM 对象（或 scalar 提取标量）
return data        →  响应给客户端
```

## 提取方法速查表

| 提取方法 | 返回 | 适用场景 | 空结果 |
|---------|------|---------|--------|
| `.scalars().all()` | `list[Model]` | 查询多条 | `[]` |
| `.scalars().first()` | `Model \| None` | 只要第一条 | `None` |
| `.scalar_one_or_none()` | `Model \| None` | 期望至多一条 | `None` |
| `.scalar_one()` | `Model` | 必须唯一 | 抛异常 |
| `.scalar()` | 单个值 | 聚合查询结果 | `None` |

## 正例（≥2 个）
1. **新闻列表**：用分页查询 + 条件查询组合——`select(News).where(News.category_id == 5).offset(skip).limit(20)`，既按分类筛选，又支持翻页。
2. **用户详情**：直接用 `db.get(User, user_id)`——一行代码精准取一条，比 `select().where()` 更简洁。
3. **仪表盘**：`func.count(User.id)` + `func.sum(Order.amount)`——多条聚合查询并行，一次性拿到所有统计数字。

## 反例/边界（≥1 个）
1. **查所有不做分页**：`select(Product).where(...)` 不加 offset/limit——表里有 10 万条商品，一次全查出来内存爆炸。
2. **用 scalars() 取聚合查询结果**：聚合返回的是数字不是 ORM 对象，用 `scalars().all()` 提取会得到 `[(6,)]` 这样的列表套元组——应该用 `scalar()`。
3. **`get()` 只能按主键查**：如果要按用户名查用户，`get` 做不到——必须用 `select().where()`。

## 详细解释
### 为什么 select 比 get 更常用？
- `get` 只能按主键查一条——场景单一（详情页）
- `select` 可以搭配 `.where()` `.offset()` `.limit()` `.order_by()` `.join()` 等，组合出无限查询——覆盖 90% 的业务场景

### 扩展：order_by 排序
```python
# 按价格降序排列
stmt = select(Book).order_by(Book.price.desc())
# 按创建时间升序
stmt = select(Book).order_by(Book.create_time.asc())
```

## 关系
### → 指向
- [[ORM条件查询]] (查询模式②)
- [[ORM聚合查询]] (查询模式③)
- [[ORM分页查询]] (查询模式④)
- [[ORM新增数据]] (查完才能增删改)
- [[ORM更新数据]] (更新前要查询)
- [[ORM删除数据]] (删除前要查询)

### ← 被指向
- [[ORM总结]] (查询是增删改查四大操作之首)
- [[路由中使用ORM]] (查询在路由中执行)
