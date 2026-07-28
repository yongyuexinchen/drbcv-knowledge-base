---
name: ORM新增数据
type: procedure
status: core
source: "[[26-FastAPI进阶-ORM操作数据-新增数据_原文]]"
domain: FastAPI
---

# ORM新增数据

## 类型判定
procedure — 三步串联：用户输入 → 转 ORM 对象 → `db.add()` + `db.commit()`。

## 类比 ★
### 一句话比喻
ORM 新增数据就像新员工入职登记——你需要先填好个人信息表格（用户输入），HR 把它录入系统生成员工档案（转成 ORM 对象），然后放入"待审批"队列（`db.add()`），最后领导签字确认（`db.commit()`）——信息才正式入库。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 用户输入（请求体） | 新员工填写的入职登记表 |
| Pydantic 模型（请求体类型） | 表格上的必填项和格式要求 |
| ORM 对象（模型类实例） | HR 录入系统后的电子档案 |
| `db.add(obj)` | 放入"待审批"文件夹 |
| `db.commit()` | 领导签字——数据真正写入数据库 |
| `create_time` 的 `default` | 自动填上"今天日期"——不用你手写 |

## 是什么
新增数据是 ORM 的标准写入操作：接收用户输入 → 通过 Pydantic 模型校验 → 用模型类创建 ORM 对象 → `db.add()` 添加到事务 → `db.commit()` 提交到数据库。

## 输入-输出空间（程序型必填）
- **输入**：
  - 请求体：用户提供的字段数据（JSON 格式）
  - Pydantic 类型：校验和类型转换
- **输出**：新插入的记录（可返回给客户端确认）
- **前置条件**：已注入 DB session，表已存在

## 三步法
```
第一步：接收请求体参数（Pydantic 校验）
    class BookCreate(BaseModel):
        book_name: str
        author: str
        price: float
        publisher: str

    @app.post("/books")
    async def add_book(book: BookCreate, db = Depends(get_db)):
        ...

第二步：转为 ORM 对象
    book_obj = Book(**book.model_dump())
    # 等价于：Book(book_name=..., author=..., ...)

第三步：添加 + 提交
    db.add(book_obj)          # 添加到事务（未入库）
    await db.commit()         # 提交事务（真正写入）
    return book_obj
```

## 核心代码
```python
from pydantic import BaseModel

# ① 定义请求体类型（用户要传什么字段）
class BookCreate(BaseModel):
    book_name: str
    author: str
    price: float
    publisher: str

@app.post("/books/")
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    # ② 将 Pydantic 模型转成 ORM 对象
    book_obj = Book(**book.model_dump())

    # ③ 添加到事务 → 提交到数据库
    db.add(book_obj)
    await db.commit()

    return book_obj
```

### 数据转换详解
```python
# book 是 Pydantic 模型对象
book.model_dump()        # → {"book_name": "红楼梦", "author": "曹雪芹", ...}

# ** 展开字典为关键字参数
Book(**book.model_dump()) # → Book(book_name="红楼梦", author="曹雪芹", ...)
```

### add vs commit —— 必须分清
| 操作 | 作用 | 数据在哪 |
|------|------|---------|
| `db.add(obj)` | 添加对象到当前事务（待提交队列） | 只在内存中 |
| `await db.commit()` | 将事务中的所有变更写入数据库 | 真正持久化 |
| `await db.rollback()` | 撤销事务中的所有变更 | 回滚到上一个 commit 点 |

> 💡 `add` 不加 `commit` = 记了小本本但没复印存档，程序一关数据就没了。

## 正例（≥2 个）
1. **用户注册**：前端 POST 提交 `{username, password, email}`，后端 `User(**user_data.dict())` → `db.add()` → `db.commit()`——注册成功，数据入库。
2. **批量导入**：Excel 导入 500 条商品数据，循环创建 ORM 对象并 `db.add()`，最后一次性 `db.commit()`——500 条在一个事务中提交，效率高且保证原子性。
3. **自动时间戳**：模型类定义了 `create_time` 的 `default=func.now()`——新增时不需要客户端传时间，ORM 自动填入服务器当前时间。

## 反例/边界（≥1 个）
1. **忘了 commit**：只调了 `db.add()` 没调 `db.commit()`——代码不报错，但刷新数据库会发现数据没进去（事务未提交）。
2. **add 不是 INSERT**：`db.add()` 只是把对象加入当前会话的待提交列表，不是立即执行 INSERT——在 `commit` 之前，其他连接看不到这条数据。
3. **Pydantic 模型 ≠ ORM 模型**：`book`（请求体参数）是 Pydantic 对象，不能直接 `db.add(book)`——必须先转成 ORM 对象。

## 详细解释
### 为什么需要依赖注入的自动 commit？
注意 `get_db` 依赖项的结构：
```python
async def get_db():
    async with async_session_local() as session:
        try:
            yield session
            await session.commit()   # ← 路由执行完后自动提交！
        except Exception:
            await session.rollback()
        ...
```
这意味着路由处理函数里只需要调 `db.add()`，不需要手动 `await db.commit()`——依赖项在 `yield` 之后会自动提交。但显式调 `commit` 也不会有副作用（幂等）。

## 关系
### → 指向
- [[路由中使用ORM]] (新增在路由中通过 DB session 完成)
- [[ORM更新数据]] (增删改查并列操作)
- [[ORM分页查询]] (新增后列表需刷新分页)

### ← 被指向
- [[ORM总结]] (增删改查四大操作之一)
- [[ORM建表]] (建表后才能新增数据)
