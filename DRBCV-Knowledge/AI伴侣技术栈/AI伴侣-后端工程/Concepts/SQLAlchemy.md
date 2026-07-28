---
name: SQLAlchemy
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-后端工程
---

# SQLAlchemy

## 类型判定
判别型 — Python 的 ORM 框架，Python 对象和数据库表之间的「翻译官」。

## 类比 ★
### 一句话比喻
SQLAlchemy 像自动翻译机——你说「帮我把这个用户对象存起来」（Python），它翻译成 `INSERT INTO users VALUES (...)`（SQL），数据库执行完再把结果翻译回 Python 对象给你。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| ORM（对象关系映射） | 翻译机——Python 话 ↔ SQL 话双向互译 |
| Model 类（User, Message） | 表格模板——定义了表长什么样、每列什么类型 |
| Session（会话） | 一次对话的上下文——「我要改这几条记录，确认后一次性提交」 |

## 是什么
SQLAlchemy 是 Python 最流行的 ORM（Object-Relational Mapping）框架。它将数据库表映射为 Python 类，表的行映射为类的实例，SQL 查询映射为 Python 方法调用。开发者可以用面向对象的方式操作数据库，而不用手写 SQL 拼接。在 AI 伴侣中，它管理用户、对话、消息、记忆等所有持久化数据。

## 输入-输出空间
- **输入**: Python 对象操作（`user.name = "永月"`，`session.add(user)`）
- **输出**: 自动生成的 SQL 语句，以及对数据库的 CRUD 操作
- **核心组件**: Engine（连接池）、Session（事务单位）、Model（表映射）

## 正例（≥2 个）
1. **查询用户对话**: `session.query(Conversation).filter_by(user_id=uid).all()` — 不用写 `SELECT * FROM conversations WHERE user_id = ?`
2. **创建消息记录**: `msg = Message(role="user", content="你好"); session.add(msg); session.commit()` — 对象操作自动转 INSERT

## 反例/边界（≥1 个）
1. **复杂报表查询**: 多表 JOIN + 聚合 + 子查询——ORM 生成的 SQL 可能不如手写的高效，此时用 SQLAlchemy Core 或原生 SQL 更好
2. **边界 — N+1 查询问题**: 查 100 个用户然后循环访问每个人的 `user.conversations`——如果不配置 `joinedload`，会执行 1+100=101 条 SQL

## 详细解释
SQLAlchemy 分两层：
- **Core**: 接近 SQL 的表达式语言，灵活但需懂 SQL
- **ORM**: 高层抽象，对象操作自动转 SQL

AI 伴侣的典型模型：
```python
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
```

与 AsyncIO 的配合：SQLAlchemy 1.4+ 支持 `asyncpg` 驱动 + `AsyncSession`，可以在 FastAPI 的 `async def` 中异步操作数据库。

## 关系
### → 指向
- [[AsyncIO]] — SQLAlchemy 的 AsyncSession 依赖 AsyncIO 实现异步数据库操作
- [[FastAPI]] — FastAPI 路由中通过 Depends 注入数据库 Session

### ← 被指向
- [[Token认证 / JWT]] — 用户表（users）由 SQLAlchemy 管理，认证时查询用户
- [[pgvector]] — pgvector 是 PostgreSQL 扩展，SQLAlchemy 可通过 ORM 操作向量字段
