---
name: Redis
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-后端工程
---

# Redis

## 类型判定
判别型 — 内存数据存储，AI 伴侣的「速记便签」和「消息中转站」。

## 类比 ★
### 一句话比喻
Redis 像你桌上的便签纸——随手写、随手看、速度极快，但别指望便签纸能永久存档。真正重要的东西还得抄到笔记本（PostgreSQL）上。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| Redis 缓存 | 便签纸——把常用信息贴在眼前，一瞥即得，不用翻档案柜 |
| Redis Pub/Sub | 办公室广播喇叭——「张三的订单好了」，所有相关的人同时听到 |
| Redis 过期（TTL） | 便签上的便利贴过了今天自动掉——临时数据自动清理 |

## 是什么
Redis 是开源的**内存键值数据库**，数据存在 RAM 中读写极快（微秒级），同时支持持久化到磁盘。它远不止缓存——提供多种数据结构（String、Hash、List、Set、Sorted Set、Stream）和高级功能（发布订阅、Lua 脚本、事务）。在 AI 伴侣中，Redis 用于会话缓存、限流、消息队列、对话状态管理等高频读写场景。

## 输入-输出空间
- **输入**: 键值命令（GET/SET/DEL/EXPIRE 等）
- **输出**: 对应的值或操作结果
- **数据结构**: Strings（缓存）、Hashes（对象）、Lists（队列）、Sets（去重集合）、Sorted Sets（排行榜）

## 正例（≥2 个）
1. **对话上下文缓存**: 用户最近 50 条消息的摘要存 Redis，打开对话时秒加载——不用每次都查 PostgreSQL
2. **LLM 调用限流**: Redis 记录用户每分钟 API 调用次数，超出限额返回 429——比数据库计数器快 100 倍

## 反例/边界（≥1 个）
1. **长期持久化存储**: 用户资料、对话历史等需要永久保存的数据——Redis 是内存为主，重启/宕机可能丢数据（取决于持久化配置），应用 PostgreSQL 做 source of truth
2. **边界 — 内存成本**: Redis 数据全在内存里，存 10GB 对话历史比 PostgreSQL 贵得多——只缓存热点数据

## 详细解释
Redis 在 AI 伴侣中的典型用法：
```
用户请求 → FastAPI
  ├→ Redis: 检查限流 & 加载会话缓存（微秒级）
  ├→ LLM: 推理（秒级）
  ├→ PostgreSQL: 持久化消息（毫秒级）
  └→ Redis: 更新缓存（微秒级）
```

Pub/Sub 的妙用：当用户 A 的 AI 伴侣「想起一件事」需要通知前端时，FastAPI 可以 pub 到 `user:A:notifications` 频道，WebSocket 连接层 sub 这个频道推给前端。

## 关系
### → 指向
- [[AsyncIO]] — Redis 的异步客户端（redis-py asyncio）依赖 AsyncIO，配合 FastAPI
- [[Token认证 / JWT]] — JWT 的黑名单/白名单常存 Redis 实现即时失效

### ← 被指向
- [[FastAPI]] — FastAPI 路由通过 Redis 做缓存和限流
- [[RAG]] — RAG 的检索结果缓存到 Redis，避免重复查询向量库
