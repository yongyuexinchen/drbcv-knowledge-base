---
name: 数据库ORM配置
type: procedure
status: core
source: "[[33-头条项目-数据库和ORM配置_原文]]"
domain: FastAPI
---

# 数据库ORM配置

## 类型判定
procedure — 三步配置法：异步引擎 → 会话工厂 → 依赖项，配好后即可通过 Depends 注入获取数据库会话。

## 类比 ★
### 一句话比喻
ORM 配置就像配钥匙三件套——引擎（create_async_engine）是钥匙坯子，会话工厂（async_sessionmaker）是开锁工具，依赖项（get_db）是随身携带的钥匙链，需要时掏出就能开数据库的门。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 异步引擎（create_async_engine） | 钥匙坯——定义了钥匙的形状和开哪把锁 |
| 会话工厂（async_sessionmaker） | 开锁工具——用钥匙坯批量生产能开锁的工具 |
| 依赖项（get_db） | 随身钥匙链——需要时掏出来用，用完自动收回 |
| 数据库 URL | 门牌号——告诉钥匙配哪扇门（哪个数据库） |
| 连接池（pool_size） | 备用钥匙数量——提前配好几把，随用随取 |

## 是什么
数据库 ORM 配置是将 FastAPI 与 MySQL 数据库通过 SQLAlchemy 异步引擎连接的三步流程。配置完以后，路由处理函数通过 `Depends(get_db)` 注入数据库会话，即可执行 ORM 增删改查操作。配置代码通常放在 `config/db_config.py`。

## 输入-输出空间（程序型必填）
- **输入**：数据库 URL（含用户名、密码、地址、端口、数据库名）、连接池参数
- **输出**：一个可注入的 `get_db` 依赖项，返回 `AsyncSession` 类型的数据库会话
- **前置条件**：已安装 `sqlalchemy[asyncio]` 和 `asyncmy`（异步 MySQL 驱动）

## 核心代码 + 步骤表
```python
# config/db_config.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

# 第一步：数据库 URL（改自己的用户名密码）
DATABASE_URL = "mysql+asyncmy://root:123456@localhost:3306/news_app?charset=utf8mb4"

# 第二步：创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,        # 连接池大小
    max_overflow=20,     # 允许溢出的额外连接数
    echo=False           # 是否打印 SQL（调试时可开 True）
)

# 第三步：创建会话工厂
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 第四步：创建依赖项（每个请求获取一个会话，用完关闭）
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()    # 正常结束提交事务
        except Exception:
            await session.rollback()  # 异常回滚
            raise
        finally:
            await session.close()     # 关闭会话
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 数据库 URL | `DATABASE_URL = "mysql+asyncmy://root:pwd@localhost/news_app"` | 指定数据库类型、账号密码、地址和库名 |
| ② 异步引擎 | `engine = create_async_engine(DATABASE_URL)` | 创建引擎，配置连接池 |
| ③ 会话工厂 | `async_session = async_sessionmaker(engine)` | 用引擎生产数据库会话 |
| ④ 依赖项 | `async def get_db(): async with async_session() as session: yield session` | 封装成可注入的依赖项 |

## 正例（≥2 个）
1. **新闻列表接口注入会话**：`async def get_news_list(db: AsyncSession = Depends(get_db))`——需要查数据库时注入，不需要时不注入，节省资源。
2. **用户注册接口注入会话**：注册需要查库（检查用户名是否存在）+ 写库（新增用户），注入 get_db 即可完成所有数据库操作。
3. **连接池复用**：pool_size=10 意味着同时最多 10 个数据库连接复用——100 个并发请求也不会反复建立/断开连接。

## 反例/边界（≥1 个）
1. **数据库 URL 写错**：用户名密码不对、数据库名写错——引擎创建不报错，但第一次查询时抛连接错误。务必先在 Navicat/DBeaver 中验证连接。
2. **忘记 commit**：在依赖项中写了 `yield session` 但没写 `await session.commit()`——增删改操作不会真正写入数据库，看起来"成功了"但刷新后数据没变。
3. **账号密码写死暴露**：数据库密码直接硬编码在代码中上传 GitHub——用环境变量 `os.getenv("DB_PASSWORD")` 代替。

## 详细解释
**异步引擎 vs 同步引擎**：FastAPI 是异步框架，必须用 `create_async_engine`（而非 `create_engine`），搭配异步驱动 `asyncmy`。如果用同步引擎，FastAPI 的异步优势荡然无存——每个数据库查询都会阻塞整个事件循环。

**依赖项的 yield 模式**：`get_db` 是一个生成器函数，`yield session` 将会话"借"给路由处理函数，处理完后回到 `finally` 块关闭会话。这确保了无论请求成功还是失败，会话一定被关闭，不会泄露连接。

**connector URL 格式**：`mysql+asyncmy://用户名:密码@主机:端口/数据库名?charset=utf8mb4`

## 关系
### → 指向
- [[依赖注入]] (get_db 是典型的依赖注入场景)
- [[ORM分页查询]] (配置好 ORM 后才能做分页查询)
- [[头条项目架构]] (db_config.py 属于 config/ 配置层)

### ← 被指向
- [[获取新闻分类]] (通过 Depends(get_db) 注入数据库会话)
- [[用户注册]] (通过 Depends(get_db) 写入数据库)
