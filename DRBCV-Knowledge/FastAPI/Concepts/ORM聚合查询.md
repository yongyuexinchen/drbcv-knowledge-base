---
name: ORM聚合查询
type: procedure
status: core
source: "[[23-FastAPI进阶-ORM操作数据-聚合查询_原文]]"
domain: FastAPI
---

# ORM聚合查询

## 类型判定
procedure — 唯一写法：`select(func.方法(模型类.属性))`，执行后用 `scalar()`（无 s）提取单个数值。

## 类比 ★
### 一句话比喻
ORM 聚合查询就像超市收银台的小票汇总——`count` 是你买了几件商品，`sum` 是总价多少钱，`avg` 是平均每件多少钱，`max` 是最贵那件的价格，`min` 是最便宜那件的价格——全部自动算好。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| `func.count()` | 小票上"共 N 件商品"——统计总数 |
| `func.sum()` | 小票底部"总金额：¥910"——全部加总 |
| `func.avg()` | "平均每件 151.67 元"——算术平均 |
| `func.max()` | "最贵一件 201 元"——找最大值 |
| `func.min()` | "最便宜一件 50 元"——找最小值 |
| `scalar()`（无 s） | 只看小票汇总那个数字——不关心具体买了啥 |

## 是什么
聚合查询是对数据库某一列的数值做**统计计算**，返回单个标量值（数字）。SQLAlchemy 通过 `func.方法名(模型类.属性)` 实现，写在 `select()` 的小括号里，执行后用 `.scalar()`（注意没有 s）提取结果。

## 输入-输出空间（程序型必填）
- **输入**：
  - 聚合方法：`count` / `sum` / `avg` / `max` / `min`
  - 统计目标字段：`模型类.属性`
- **输出**：一个数字（标量值）
- **前置条件**：已有 DB session 注入路由

## 五合一公式
```python
# 通用模板：select(func.方法(模型类.属性))
# 执行：await db.execute(stmt)
# 提取：result.scalar()  ← 注意：没有 s！不是 scalars()

# 1. 统计总行数
stmt = select(func.count(Book.id))
total = (await db.execute(stmt)).scalar()      # → 6

# 2. 求和
stmt = select(func.sum(Book.price))
total_price = (await db.execute(stmt)).scalar() # → 910

# 3. 求平均值
stmt = select(func.avg(Book.price))
avg_price = (await db.execute(stmt)).scalar()   # → 151.67

# 4. 求最大值
stmt = select(func.max(Book.price))
max_price = (await db.execute(stmt)).scalar()   # → 201

# 5. 求最小值
stmt = select(func.min(Book.price))
min_price = (await db.execute(stmt)).scalar()   # → 50
```

## 核心代码（完整接口示例）
```python
from sqlalchemy import func, select

@app.get("/books/stats")
async def book_stats(db: AsyncSession = Depends(get_db)):
    # 统计总数量
    count_stmt = select(func.count(Book.id))
    total = (await db.execute(count_stmt)).scalar()

    # 求平均价格
    avg_stmt = select(func.avg(Book.price))
    avg_price = (await db.execute(avg_stmt)).scalar()

    return {
        "total": total,
        "avg_price": round(float(avg_price), 2)
    }
```

## 正例（≥2 个）
1. **仪表盘统计**：后台首页显示"总用户数 `count`、今日订单总额 `sum`、平均客单价 `avg`"——一条聚合查询替代查全部数据再 Python 计算。
2. **价格筛选器**：电商筛选页顶部显示"最高价 9999 元、最低价 9.9 元"——`func.max(Product.price)` + `func.min(Product.price)` 两个聚合搞定。
3. **数据校验**：注册时检查用户名是否被占用，用 `func.count()` 比用 `scalars().all()` 查所有再数更高效——聚合查询在数据库层面计算，不传输原始数据。

## 反例/边界（≥1 个）
1. **聚合查询不要用 `scalars()`（带 s）提取**：`scalar()` 提取单个值，`scalars()` 提取 ORM 对象列表——用 `scalars().all()` 去取一个数字会报错或返回奇怪的结果。
2. **`func.count()` 不传属性**：`func.count()` 空括号统计整行，`func.count(Book.id)` 统计某列非 NULL 值——两者在大部分情况结果一样，但语义不同。
3. **空表聚合**：表里没有数据时，`func.avg()` 返回 `None` 而非 0——需要做 `or 0` 处理，否则前端显示 `null`。

## 详细解释
### `scalar()` vs `scalars()` —— 一字之差，天壤之别
| 方法 | 返回值 | 使用场景 |
|------|--------|---------|
| `result.scalar()` | 单个标量值（数字、字符串等） | 聚合查询、取单个值 |
| `result.scalars().all()` | ORM 对象列表 | 查询返回多行数据 |
| `result.scalars().first()` | 单个 ORM 对象或 None | 取第一条数据 |

### 聚合查询的本质
聚合查询在数据库层面由 SQL 的聚合函数完成：
```sql
SELECT COUNT(id) FROM book;    -- func.count(Book.id)
SELECT AVG(price) FROM book;   -- func.avg(Book.price)
SELECT MAX(price) FROM book;   -- func.max(Book.price)
```
ORM 的优势：不写字符串 SQL，Python 里就有语法检查和自动补全。

## 关系
### → 指向
- [[ORM条件查询]] (聚合 + where 可统计满足条件的数据)
- [[ORM查询总结]] (聚合是 select 查询的四种模式之一)

### ← 被指向
- [[ORM查询总结]] (聚合查询是查询全景图的统计分支)
