---
name: ORM更新数据
type: procedure
status: core
source: "[[27-FastAPI进阶-ORM操作数据-更新数据_原文]]"
domain: FastAPI
---

# ORM更新数据

## 类型判定
procedure — 三步走流程：先查 → 找到则改属性 → commit 提交。找不到则抛 404。

## 类比 ★
### 一句话比喻
ORM 更新数据就像去派出所修改户口本信息——你不可能凭空改，必须先把户口本翻到你的那一页（`db.get` 查找），拿笔把旧信息划掉写上新的（属性重新赋值），最后警官盖章确认（`db.commit()`）。如果翻遍户口本找不到你这个人——那肯定报错（404）。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| `db.get(Model, id)` | 翻户口本找你的那一页——按身份证号定位 |
| 属性重新赋值 | 拿笔把"张三"划掉改成"张四" |
| `db.commit()` | 警官盖章——修改正式生效 |
| `raise HTTPException(404)` | "查无此人，你是不是走错派出所了" |
| `update_time` 的 `onupdate` | 自动在修改栏填上"今天日期"——不用你手写 |

## 是什么
更新数据遵循"先查后改再提交"的黄金流程。通过路径参数拿到要修改的记录 ID → 用 `get` 或 `select` 查出 ORM 对象 → 将用户提供的新值赋给对象属性 → `commit` 提交。找不到则抛 HTTP 404。

## 输入-输出空间（程序型必填）
- **输入**：
  - 路径参数：要修改的记录 ID（主键）
  - 请求体：新的字段值（Pydantic 模型校验）
- **输出**：修改后的完整记录
- **前置条件**：已注入 DB session

## 三步法
```
第一步：先查
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="查无此书")

第二步：再改（属性重新赋值）
    db_book.book_name = data.book_name
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher

第三步：提交
    await db.commit()
    return db_book
```

## 核心代码
```python
from fastapi import HTTPException

# 请求体：只包含允许用户修改的字段
class BookUpdate(BaseModel):
    book_name: str
    author: str
    price: float
    publisher: str

@app.put("/books/{book_id}")
async def update_book(
    book_id: int,
    data: BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    # ① 先查
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="查无此书")

    # ② 再改
    db_book.book_name = data.book_name
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher

    # ③ 提交
    await db.commit()
    return db_book
```

### 更新 vs 新增 —— 关键区别
| | 新增（Create） | 更新（Update） |
|---|---|---|
| HTTP 方法 | POST | PUT / PATCH |
| 是否有 ID | 无（库自动生成） | 有（路径参数指定） |
| 前置步骤 | 无 | **必须先查询** |
| 写入方式 | `db.add(新对象)` | 属性直接赋值 |
| 找不到时 | N/A（新记录不存在找不到） | 抛 404 |

## 正例（≥2 个）
1. **编辑个人资料**：用户改昵称、头像、简介——`PUT /users/{user_id}`，查出用户对象，只改传入的字段，`commit` 提交。
2. **商品改价**：运营后台修改商品价格——`PUT /products/{id}`，查出商品，`product.price = new_price`，提交——比直接写 SQL UPDATE 更安全（自动防注入）。
3. **部分更新**（PATCH）：用户只改昵称不改密码——可以检查 `data.field is not None` 才赋值，避免把没传的字段覆盖成空值。

## 反例/边界（≥1 个）
1. **不先查直接改**：没有 `get` 先取对象，凭空 new 一个 `Book(id=5)` 然后去改——这个对象不在会话中，`commit` 不会影响数据库（或报 `StaleDataError`）。
2. **赋完值忘了 commit**：属性确实改了（在内存中），但没 `commit`——刷新数据库发现数据根本没变，程序关了修改就丢了。
3. **用 POST 做更新**：虽然技术上可行，但 RESTful 语义约定 POST=新建、PUT=全量更新、PATCH=部分更新——混用会让前后端协作混乱。

## 详细解释
### 为什么"先查"是必须的？
```python
# ❌ 错误做法：直接构造对象
book = Book(id=5, book_name="新书名")  # 这个对象不在会话中
db.add(book)                            # 可能被视为新增，而非更新
await db.commit()                       # 不会更新 id=5 的那条记录

# ✅ 正确做法：从数据库查出真实对象
book = await db.get(Book, 5)           # 查出真实存在的 ORM 对象
book.book_name = "新书名"               # 修改它的属性
await db.commit()                      # SQLAlchemy 自动追踪变更，生成 UPDATE
```
SQLAlchemy 通过**身份映射（Identity Map）**保证同一个会话中相同主键只对应一个对象。你必须拿到那个"活的对象"才能改。

### `update_time` 自动更新原理
```python
class Base(DeclarativeBase):
    update_time: Mapped[datetime] = mapped_column(
        onupdate=func.now()    # ← 任何 UPDATE 操作都自动刷新时间
    )
```
只要对 ORM 对象做了修改并 `commit`，`update_time` 会自动更新为当前时间——无需手动赋值。

## 关系
### → 指向
- [[ORM查询总结]] (更新前必须查询)
- [[ORM删除数据]] (更新和删除都是"先查再操作再提交"模式)
- [[HTTP异常处理]] (找不到资源抛 404)

### ← 被指向
- [[ORM总结]] (增删改查四大操作之一)
- [[ORM条件查询]] (复杂更新前可能需要条件查询定位)
