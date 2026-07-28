---
name: ORM建表
type: procedure
status: core
source: "[[18-FastAPI进阶-ORM-建表_原文]]"
domain: FastAPI
---

# ORM建表

## 类型判定
procedure — 严格三步流程：创建数据库引擎 → 定义模型类 → 启动时建表。

## 类比 ★
### 一句话比喻
ORM 建表就像盖房子——第一步，把水管电网（数据库引擎）接通；第二步，画好设计蓝图（模型类）；第三步，施工队（`create_all`）按图施工，房子（表）就盖好了。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 异步引擎（AsyncEngine） | 水管电网总闸——接通才能施工 |
| 数据库 URL | 工地的具体地址——告诉施工队往哪儿走 |
| 模型类（Model Class） | 建筑蓝图——定义了房间结构（字段） |
| `Base` 基类 | 标准户型模板——所有房间都有水电表 |
| `Base.metadata.create_all` | 施工队按图建造——蓝图 → 实体 |
| `__tablename__` | 门牌号——给这个房间起个名字 |
| `Mapped` + `mapped_column` | 蓝图上的标注——这个房间做卧室（int），那个做客厅（string） |

## 是什么
ORM 建表是用 Python 类定义数据库表结构，通过 SQLAlchemy 的 `create_all` 方法自动在数据库中创建对应的表。全程不写一行 SQL。

## 输入-输出空间（程序型必填）
- **输入**：
  - 数据库连接 URL（用户名、密码、地址、端口、库名、编码）
  - 模型类定义（字段名、类型、约束）
- **输出**：数据库中自动创建好的表
- **前置条件**：已安装 `sqlalchemy[asyncio]` + `aiomysql`，数据库已存在

## 三步法
```
第一步：创建异步数据库引擎
├── URL 公式：mysql+aiomysql://用户名:密码@地址:端口/数据库名?charset=utf8
├── echo=True（可选，打印 SQL 日志）
├── pool_size=10（连接池活跃连接数）
└── max_overflow=20（额外允许超出的连接数，总上限=10+20=30）

第二步：定义模型类
├── 先定义基类：class Base(DeclarativeBase): ...
│   └── 放所有表共用的字段（如 create_time, update_time）
├── 再定义表模型类：class Book(Base):
│   ├── __tablename__ = "book"  （表名）
│   ├── id: Mapped[int] = mapped_column(primary_key=True)
│   ├── book_name: Mapped[str] = mapped_column(String(255))
│   └── price: Mapped[float] = mapped_column(Float)

第三步：在 FastAPI 启动时建表
├── @app.on_event("startup")
├── async def startup_event():
│       await create_tables()
└── create_tables 内部：
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

## 核心代码
```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float

# 第一步：创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_first?charset=utf8"
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, pool_size=10, max_overflow=20)

# 第二步：定义模型类
class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍ID")
    book_name: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(100), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(100), comment="出版社")

# 第三步：启动时建表
@app.on_event("startup")
async def startup_event():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### 关键注意事项
- `create_all` 后面**不要加括号** `()` —— 不是立即调用，而是传给 `run_sync` 让它调用
- 如果表已经存在，`create_all` 不会重复创建（幂等）
- 修改了模型类增加新字段，`create_all` **不会自动更新已有表**——需要用迁移工具（Alembic）

## 正例（≥2 个）
1. **新项目初始化**：定义好 `Book`、`User` 两个模型类，启动 FastAPI，两张表自动建好——第一次跑项目就搞定所有表。
2. **微服务独立数据库**：每个微服务只定义自己需要的模型类，启动时自行建表——不用人工去每个数据库手动建表。
3. **单元测试**：测试环境用 SQLite 内存数据库（改一下 URL），启动时自动建表，跑完测试销毁——零手动运维。

## 反例/边界（≥1 个）
1. **修改已有字段类型**：把 `book_name` 从 `String(255)` 改成 `String(500)`，再启动项目——`create_all` 不会修改已有表结构，字段还是 255。必须用 Alembic 做数据库迁移。
2. **URL 里密码含特殊字符**：`root:p@ss!word@localhost`——`@` 和 `!` 可能被解析错，需要用 URL 编码。
3. **启动时数据库没准备好**：数据库服务没启动就运行 FastAPI，`create_all` 直接抛连接异常——需要确保数据库先启动。

## 详细解释
### 连接池参数说明
| 参数 | 含义 | 默认值 | 建议 |
|------|------|--------|------|
| `pool_size` | 活跃连接数 | 5 | 开发环境 5-10，生产根据 QPS 调整 |
| `max_overflow` | 超出 pool_size 的额外连接 | 10 | 总上限 = pool_size + max_overflow |
| `echo` | 打印 SQL 日志 | False | 开发时开，生产关 |

### 基类字段示例（通用创建/更新时间）
```python
from datetime import datetime
from sqlalchemy import func

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        default=func.now(),
        comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
        comment="修改时间"
    )
```

## 关系
### → 指向
- [[路由中使用ORM]] (建好表才能在路由中操作)
- [[ORM新增数据]] (表建好了就可以加数据)
- [[ORM简介]] (建表是安装后的下一步)

### ← 被指向
- [[ORM总结]] (三大步中的第二步)
- [[ORM简介]] (装了包下一步就是建表)
