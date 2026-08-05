---
name: ORM简介
type: discriminant
status: core
source: "[[17-FastAPI进阶-ORM简介及安装_原文]]"
domain: FastAPI
---

# ORM简介

## 类型判定
discriminant — 区分"手写 SQL"和"面向对象操作数据库"两种范式，明确 ORM 的本质价值。

## 类比 ★
### 一句话比喻
ORM 就像一个随身翻译官——你只需要用中文（Python）说"把这条数据存起来"，翻译官自动帮你翻译成法语（SQL）告诉数据库，你完全不需要学外语（手写 SQL）。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| ORM 工具 | 随身翻译官——你讲 Python，它帮你翻成 SQL |
| 手写 SQL | 自己去背法语单词、学语法——费时费力还容易出错 |
| 模型类（Model Class） | 你的中文剧本——用 Python class 描述数据长什么样 |
| SQL 注入攻击 | 坏人故意说一句有歧义的话让翻译官犯错——ORM 自动防注入 |
| 数据库连接/事务 | 翻译官帮你预约会议室、开门锁门——你不用操心这些杂务 |

## 是什么
ORM（Object-Relational Mapping，对象关系映射）是一种**用面向对象方式操作数据库**的编程技术。程序员不再手写 SQL 语句，而是通过 Python 类（模型类）来建表、通过对象方法来增删改查数据。SQLAlchemy 是 Python 生态中企业使用最多、社区最活跃的 ORM 工具。

## 正例（≥2 个）
1. **快速建表**：写一个 Python 类，定义几个属性，运行项目时自动创建数据库表——不用打开 Navicat 手写 `CREATE TABLE`。
2. **防 SQL 注入**：ORM 自动对参数做转义处理，`user_input = "1; DROP TABLE users;"` 这样的恶意输入不会被执行——比手动拼接 SQL 字符串安全得多。
3. **数据库切换**：从 MySQL 换到 PostgreSQL，只需改一行连接地址——ORM 屏蔽了不同数据库的方言差异，业务代码不用动。

## 反例/边界（≥1 个）
1. **不是所有 SQL 都能完美替代**：极其复杂的多表联查、存储过程、递归查询——ORM 写起来可能比手写 SQL 还绕，这时可以考虑混合使用（ORM + 原生 SQL）。
2. **ORM 不是银弹**：每条 ORM 语句背后还是 SQL——如果 N+1 查询问题不注意，性能照样翻车。
3. **需要安装两个包**：`sqlalchemy[asyncio]` + `aiomysql`（异步驱动），FastAPI 异步项目缺一不可。

## 详细解释
### 安装命令
```bash
pip install "sqlalchemy[asyncio]" aiomysql
```

### SQLAlchemy 为什么是首选？
- **企业使用最多**：Python ORM 三巨头（SQLAlchemy、Django ORM、Peewee）中排第一
- **社区最完善**：文档全、教程多、遇到问题搜得到
- **支持异步**：`sqlalchemy[asyncio]` 天生支持 `async/await`，与 FastAPI 异步架构无缝配合
- **功能最强**：既有 ORM（面向对象），也有 Core（接近 SQL 的底层 API），能应付简单到复杂的所有场景

### ORM vs 手写 SQL
| | ORM | 手写 SQL |
|---|---|---|
| 写法 | `select(Book)` | `SELECT * FROM book` |
| 防注入 | 自动 | 需手动处理 |
| 可读性 | Python 对象风格 | 字符串拼接 |
| 数据库切换 | 改连接串 | 可能要改大量 SQL 方言 |
| 学习成本 | 学 ORM API | 学 SQL 语法 |

## 关系
### → 指向
- [[ORM建表]] (装了 SQLAlchemy 就要建表)
- [[ORM新增数据]] (增删改查是 ORM 的核心能力)
- [[路由中使用ORM]] (ORM 通过依赖注入接入路由)

### ← 被指向
- [[ORM总结]] (全流程回顾的起点)
