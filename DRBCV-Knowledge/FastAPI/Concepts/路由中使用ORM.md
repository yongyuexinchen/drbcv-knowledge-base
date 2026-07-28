---
name: 路由中使用ORM
type: procedure
status: core
source: "[[19-FastAPI进阶-ORM-在路由中使用ORM_原文]]"
domain: FastAPI
---

# 路由中使用ORM

## 类型判定
procedure — 先创建数据库会话依赖项，再通过 Depends 注入到需要操作数据库的路由处理函数中。

## 类比 ★
### 一句话比喻
路由中使用 ORM 就像去银行柜台办业务——你到了柜台（路由），柜员不会让你直接进金库（数据库），而是通过"取号-叫号-递单子"这一套流程（依赖注入）拿到一个临时的业务窗口（DB session），办完即关。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 数据库 | 银行金库——不能随便进 |
| `sessionmaker` 会话工厂 | 叫号机——每次取一个新号 |
| `get_db` 依赖项 | 柜员的标准工作流程——取号→办业务→关窗 |
| `Depends(get_db)` | 你走到柜台上说"我要办业务" |
| `try...commit` | 业务办成→确认签字 |
| `except...rollback` | 出错了→撤销操作，恢复原样 |
| `finally...close` | 不管办成没办成→关闭窗口，归还号码 |

## 是什么
在路由中使用 ORM 的核心机制是**依赖注入数据库会话**。通过创建 `async_sessionmaker` 会话工厂 → 定义 `get_db` 依赖项（封装获取会话+提交/回滚/关闭逻辑）→ 在路由处理函数中通过 `Depends(get_db)` 注入——路由函数就能用面向对象的方式操作数据库了。

## 输入-输出空间（程序型必填）
- **输入**：
  - 异步引擎（`async_engine`，建表时已创建）
  - 路由处理函数中声明 `db: AsyncSession = Depends(get_db)`
- **输出**：一个可用的数据库会话对象（`AsyncSession`），用于增删改查
- **前置条件**：已安装 SQLAlchemy 异步包、已定义异步引擎、已建表

## 三步法
```
第一步：创建异步会话工厂
    async_session_local = async_sessionmaker(
        bind=async_engine,           # 绑定数据库引擎
        class_=AsyncSession,          # 指定异步会话类
        expire_on_commit=False        # 提交后不过期，避免重复查库
    )

第二步：定义数据库会话依赖项
    async def get_db():
        async with async_session_local() as session:
            try:
                yield session           # 返回会话给路由
                await session.commit()  # 无异常则提交
            except Exception:
                await session.rollback() # 有异常则回滚
                raise
            finally:
                await session.close()   # 最终关闭，防连接泄漏

第三步：在路由中注入使用
    @app.get("/books/")
    async def get_books(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book))
        books = result.scalars().all()
        return books
```

## 核心代码
```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from fastapi import Depends

# 第一步：创建会话工厂（bind 到已有的异步引擎）
async_session_local = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False    # 提交后会话不过期，性能更好
)

# 第二步：依赖项——封装会话获取 + 提交/回滚/关闭
async def get_db():
    async with async_session_local() as session:
        try:
            yield session                # 注入到路由
            await session.commit()       # 自动提交
        except Exception:
            await session.rollback()     # 异常回滚，保证数据一致性
            raise
        finally:
            await session.close()        # 关闭会话，防止连接泄漏

# 第三步：路由中注入
@app.get("/books/")
async def get_books(db: AsyncSession = Depends(get_db)):
    stmt = select(Book)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books
```

## 正例（≥2 个）
1. **查询接口**：`GET /books/` 注入 `db`，执行 `select(Book)` 查所有图书，无需手动打开关闭连接。
2. **注册接口**：`POST /register` 注入 `db`，创建用户对象、`db.add()`、事务自动提交——出错了自动回滚，不会产生脏数据。
3. **按需注入**：只有 5 个需要查库的接口注入 `Depends(get_db)`，另外 20 个纯计算接口不注入——不创建不必要的数据库连接，节省连接池资源。

## 反例/边界（≥1 个）
1. **忘了 `expire_on_commit=False`**：默认提交后会话过期，再次访问 ORM 对象的属性时会重新查询数据库——性能浪费，而且过期后对象属性可能变成 `None`。
2. **`Depends(get_db)` 写成 `Depends(get_db())`**：加了括号就是调用函数而非传函数引用——FastAPI 不认识，di 机制失效。
3. **会话不关闭导致连接泄漏**：如果没有 `finally close`，异常发生时连接不回池——连接池很快耗尽，新请求直接报错。

## 详细解释
### 依赖项中的 try/except/finally 三层保护
```python
try:
    yield session          # ← 正常：返回会话给路由
    await session.commit() # ← 路由执行完无异常，自动提交
except Exception:
    await session.rollback() # ← 路由报错，回滚所有更改
    raise                    # ← 把异常继续往外抛，让 FastAPI 处理
finally:
    await session.close()  # ← 不管成败，必须关闭会话
```
- **`yield` 后面的代码**在路由函数执行完毕后执行（类似 `with` 的 `__exit__`）
- 正常路径：路由跑完 → `commit` → `close`
- 异常路径：路由报错 → `rollback` → `raise` → `close`

## 关系
### → 指向
- [[依赖注入]] (这是依赖注入在 ORM 场景的标准用法)
- [[ORM查询数据]] (有了 DB session 才能查询)
- [[ORM新增数据]] (增删改查都依赖注入的 session)

### ← 被指向
- [[ORM建表]] (建表后需要在路由中访问)
- [[ORM总结]] (增删改查的前置步骤)
