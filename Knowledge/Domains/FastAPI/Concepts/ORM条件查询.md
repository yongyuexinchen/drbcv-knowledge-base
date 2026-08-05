---
name: ORM条件查询
type: discriminant
status: core
source: "[[20-FastAPI进阶-ORM操作数据-查询数据_原文]], [[21-FastAPI进阶-ORM操作数据-条件查询-比较判断_原文]], [[22-FastAPI进阶-ORM操作数据-条件查询-模糊&与非&包含_原文]]"
domain: FastAPI
---

# ORM条件查询

## 类型判定
discriminant — 在四种条件查询类型的对比中，明确 when 用哪种、怎么写。

## 类比 ★
### 一句话比喻
ORM 条件查询就像逛超市用筛选器挑商品——你可以按"价格 > 100 元"筛掉便宜的，按"品牌包含'蒙牛'"模糊搜，还可以组合"价格 > 100 且 品牌是蒙牛或伊利"——各种条件随便拼。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| `==` 、`>`、`>=` | 标价签上写"100 元以上"——精确比较大小 |
| `like('%曹%')` | 搜索栏输"曹"——模糊匹配，包含就行 |
| `in_([1,3,5])` | 只逛第 1、3、5 排货架——精确集合筛选 |
| `and_()` / `or_()` | "要牛奶且不要酸奶"——多个条件组合 |



## 是什么
`select(Model).where(...)` 是 ORM 条件查询的标准写法。`where()` 小括号里可以写比较判断、模糊匹配、包含判断、逻辑组合四类条件，返回符合条件的数据。

## 条件类型全景对比

| 条件类型 | 写法 | 作用 | 典型使用场景 | 提取方法 |
|---------|------|------|-------------|---------|
| **比较判断** | `Book.price >= 200` | 大于、小于、等于 | 价格筛选、时间范围 | `scalars().all()` / `scalars().first()` / `scalar_one_or_none()` |
| **模糊查询** | `Book.author.like('%曹%')` | 模糊匹配字符串 | 搜索框输入关键字 | `scalars().all()` |
| **逻辑组合** | `and_(条件1, 条件2)` / `or_(条件1, 条件2)` / `~条件` | 与、或、非 | 多条件叠加筛选 | 同比较判断 |
| **包含判断** | `Book.id.in_([1, 3, 5])` | 判断值是否在列表中 | 批量查询指定 ID | `scalars().all()` |

### 比较判断详解
```python
# 相等
Book.id == book_id                    # 查询 ID=3 的书

# 大于等于
Book.price >= 200                     # 价格 ≥200

# 大于 / 小于 / 小于等于 同理
Book.price > 100                      # 价格 >100
Book.price < 50                       # 价格 <50
Book.price <= 99.9                    # 价格 ≤99.9
```

### 模糊查询详解
```python
# '%曹%'  — 包含"曹"（任意位置）
Book.author.like('%曹%')             # → 曹雪芹、曹操、欧阳曹

# '曹%'   — 以"曹"开头
Book.author.like('曹%')              # → 曹雪芹、曹植

# '曹_'   — 以"曹"开头 + 恰好1个字符
Book.author.like('曹_')              # → 曹植（不包括曹雪芹）
```

### 逻辑组合详解
```python
from sqlalchemy import and_, or_

# AND：同时满足两个条件
Book.author.like('曹%') and_(Book.price > 100)   # 或直接写：Book.price > 100

# OR：满足任一条件
or_(Book.author.like('曹%'), Book.price > 100)   # 或使用竖杠：条件1 | 条件2

# NOT：取反
~(Book.price > 100)                                # 价格 ≤100
```

### 包含判断详解
```python
# 批量查指定 ID 的书
book_ids = [1, 3, 5, 7]
stmt = select(Book).where(Book.id.in_(book_ids))  # → ID 为 1、3、5、7 的书
```

## 四种提取方法对比
| 方法 | 返回值 | 适用场景 | 查不到时 |
|------|--------|---------|---------|
| `scalars().all()` | `list[Model]` | 可能多条 | 空列表 `[]` |
| `scalars().first()` | `Model` 或 `None` | 只要第一条 | `None` |
| `scalar_one_or_none()` | `Model` 或 `None` | 期望至多一条 | `None` |
| `scalar_one()` | `Model` | 必须是唯一一条 | 抛异常 |

## 正例（≥2 个）
1. **搜索功能**：用户输"三国"，后端用 `Book.book_name.like('%三国%')` 模糊匹配——无论用户搜"三国演义"还是"三国志"都能命中。
2. **价格区间筛选**：前端传 `min_price=50, max_price=200`，后端写 `and_(Book.price >= 50, Book.price <= 200)`——圈定价格范围。
3. **批量操作**：用户勾选 5 本书删除，前端传 `ids=[1,3,5,7,9]`，后端用 `Book.id.in_(ids)` 一次性查出——比循环 5 次 `get` 高效。

## 反例/边界（≥1 个）
1. **`like` 忘了加百分号**：`Book.author.like('曹')` 只匹配作者恰好叫"曹"一个字的——大概率查不到，因为作者名通常是 2-3 个字。
2. **`in_` 传空列表**：`Book.id.in_([])`——SQL 会报错或返回空结果，应在前端校验列表非空。
3. **`and_` 写成 `and`**：Python 关键字 `and` 不能用于 SQLAlchemy 条件组合——必须用 `and_()` 或直接用逗号隔开多个条件。

## 详细解释
### 多条件 where 的三种等价写法
```python
# 写法一：逗号隔开（自动 AND）
stmt = select(Book).where(Book.price > 100, Book.author.like('曹%'))

# 写法二：显式 and_()
stmt = select(Book).where(and_(Book.price > 100, Book.author.like('曹%')))

# 写法三：链式调用（不推荐，只有最后一个 where 生效）
❌ stmt = select(Book).where(Book.price > 100).where(Book.author.like('曹%'))  # SQLAlchemy 2.0 中会覆盖！
```

## 关系
### → 指向
- [[ORM查询数据]] (条件查询是 select 查询的子集)
- [[ORM聚合查询]] (条件 + 聚合可以统计满足条件的数据)
- [[ORM分页查询]] (条件 + 分页实现筛选后翻页)

### ← 被指向
- [[ORM查询总结]] (条件查询是五种查询模式的重要分支)
- [[路由中使用ORM]] (条件查询在路由处理函数中使用)
