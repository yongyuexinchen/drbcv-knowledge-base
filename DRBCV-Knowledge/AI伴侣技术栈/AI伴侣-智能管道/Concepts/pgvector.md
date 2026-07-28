---
name: pgvector
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-智能管道
---

# pgvector

## 类型判定
判别型 — PostgreSQL 的向量扩展，让关系数据库同时支持语义搜索。

## 类比 ★
### 一句话比喻
pgvector 像在传统图书馆里加装了一套智能导航——图书馆还是那个图书馆（PostgreSQL），书架还是那些书架（表），但你现在可以不说书名，直接说「帮我找关于旅行的书」，导航系统（向量索引）带你找到它们。一套建筑，两种找法。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| PostgreSQL（关系数据库） | 传统图书馆——按目录精确查找 |
| pgvector 扩展 | 在传统图书馆里装了语义导航——目录查找+语义搜索二合一 |
| 向量 + 元数据同库 | 书和它的 GPS 坐标放在同一个架子上——查书时一次拿到书+位置 |

## 是什么
pgvector 是 PostgreSQL 的开源扩展，为 PostgreSQL 添加了 `vector` 数据类型和 IVFFlat / HNSW 索引。它的核心价值是**统一存储**：关系数据（用户、订单、消息）和向量数据（Embedding）在同一个数据库中，用一条 SQL 即可完成「查找用户 X 的所有记忆中与当前查询最相似的前 5 条」。不需要再维护一个独立的向量数据库。

## 输入-输出空间
- **输入**: 与 PostgreSQL 相同的 SQL 接口，新增 `vector` 列类型和 `<=>` 余弦距离运算符
- **输出**: 标准 SQL 结果集，可 JOIN 其他表
- **索引**: IVFFlat（倒排，适合精搜）和 HNSW（图索引，适合快搜），pgvector 0.5+ 支持两者

## 正例（≥2 个）
1. **AI 伴侣记忆检索一体**: `SELECT memory_text FROM memories WHERE user_id=123 ORDER BY embedding <=> query_embedding LIMIT 5` — 一条 SQL 过滤用户 + 语义搜索
2. **混合搜索**: `WHERE category='技术' ORDER BY embedding <=> query_vec LIMIT 10` — 精确过滤 + 语义排序，不用跨库拼接

## 反例/边界（≥1 个）
1. **十亿级向量规模**: pgvector 受限于 PostgreSQL 的单机架构，千万级向量还行，十亿级需要 Milvus/Qdrant 等分布式向量数据库
2. **边界 — 索引构建耗资源**: 在已有大量数据上创建 HNSW 索引会长时间锁表，需要在低峰期操作

## 详细解释
pgvector 的使用流程：

```sql
-- 1. 启用扩展
CREATE EXTENSION vector;

-- 2. 创建带向量列的表
CREATE TABLE memories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    content TEXT,
    embedding vector(1536)  -- 存储 1536 维向量
);

-- 3. 创建索引（加速检索）
CREATE INDEX ON memories USING hnsw (embedding vector_cosine_ops);

-- 4. 语义搜索
SELECT content, 1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM memories
WHERE user_id = 123
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

`<=>` 返回余弦距离（0=完全相同，2=完全不同），`1 - 余弦距离` = 余弦相似度。

pgvector vs 专用向量数据库的取舍：
| 选 pgvector | 选专用向量库 |
|------------|-------------|
| 已在用 PG，不想多维护一个库 | 向量规模超千万 |
| 需要关系过滤 + 向量搜索在一句中 | 需要极致检索性能 |
| 团队不熟向量库运维 | 需要多副本/分布式 |

## 关系
### → 指向
- [[Embedding]] — Embedding 生成的向量存入 pgvector 的 vector 列
- [[Similarity Search]] — pgvector 的 `<=>` 运算符执行余弦相似度计算
- [[SQLAlchemy]] — SQLAlchemy 可通过 pgvector 的 ORM 适配器操作向量字段

### ← 被指向
- [[Vector Database]] — pgvector 是向量数据库的一种实现（基于 PG 的轻量方案）
- [[RAG]] — RAG 若用 PostgreSQL 做知识存储，pgvector 提供向量检索能力
