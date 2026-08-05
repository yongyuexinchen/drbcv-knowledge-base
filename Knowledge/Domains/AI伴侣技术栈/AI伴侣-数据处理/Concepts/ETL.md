---
name: ETL
type: procedure
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-数据处理
---

# ETL（Extract, Transform, Load）

## 类型判定
过程型 — 数据世界的「物流系统」：从各处取货（Extract）→ 统一包装加工（Transform）→ 送入仓库（Load）。

## 类比 ★
### 一句话比喻
ETL 像一个跨国物流中心——原材料从全世界各地运来（Extract：阿根廷的皮革、日本的芯片、德国的螺丝），在中心统一质检、分包、贴上标准标签（Transform），最后装进自己的仓库货架（Load）。没有统一物流，每个工厂只能对着自己门口那堆杂货干瞪眼。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| Extract（抽取） | 从全球供应商收货——每个来源格式不同（纸箱/木箱/散装） |
| Transform（转换） | 统一质检+分包+贴标——规范化才能上货架 |
| Load（加载） | 货品入库——按分类存入指定仓库区域 |

## 是什么
ETL 是数据处理的核心范式，定义了数据从源头到目的地的标准流程：① Extract——从多个异构数据源（数据库、API、日志文件、消息队列）抽取原始数据；② Transform——清洗、去重、格式转换、聚合、特征工程，将杂乱的原始数据转化为结构化、可用的数据；③ Load——将处理后的数据写入目标系统（数据仓库、数据库、向量库）。在 AI 伴侣场景中，ETL 贯穿始终：从用户行为日志到用户画像、从对话数据到记忆库，都依赖 ETL 流水线。

## 输入-输出空间
- **输入**: 异构数据源——关系型数据库、NoSQL、日志文件、API 响应、事件流
- **输出**: 清洗、转换、聚合后的结构化数据——写入数据仓库、特征存储或模型训练集
- **调度**: 通常由 Airflow / Dagster 等编排工具按 Cron 或事件触发

## 正例（≥2 个）
1. **用户行为日志 → 用户画像**: Extract（从 Kafka 读取事件）→ Transform（按用户 ID 聚合、计算特征）→ Load（写入用户画像数据库）
2. **对话数据 → 长期记忆库**: Extract（从 PostgreSQL 读取对话）→ Transform（切片、向量化、提取摘要）→ Load（写入向量数据库）

## 反例/边界（≥1 个）
1. **ELT（Extract-Load-Transform）**: 另一种范式——先加载原始数据到目标系统（如 Snowflake），再在目标系统内做 Transform。现代数据栈倾向于 ELT，但 AI 伴侣场景中数据量适中、转换逻辑重，ETL 更可控
2. **边界 — 实时 vs 批处理**: ETL 传统上按批次运行（如每小时/每天），实时场景（如用户发消息立刻更新记忆）需要 Streaming ETL（如 Flink/Kafka Streams）

## 详细解释
ETL 在 AI 伴侣数据处理中的典型管线：
```
[数据源层]
├─ 用户对话日志 (PostgreSQL)
├─ 行为事件流 (Kafka)
├─ 外部知识库 (API/文件)
└─ 语音交互日志 (对象存储)
        ↓ Extract
[Transform 层：Spark / Python]
├─ 数据清洗（去噪、去重、格式统一）
├─ 特征工程（行为统计、情感分析、话题提取）
└─ 向量化（Embedding）
        ↓ Load
[目标层]
├─ 用户画像库 (PostgreSQL / HBase)
├─ 向量记忆库 (Milvus / Qdrant)
└─ 分析数据仓库 (ClickHouse)
```

## 关系
### → 指向
- [[Apache Spark]] — Spark 是 ETL 的 Transform 阶段最常用的分布式执行引擎
- [[Data Pipeline]] — ETL 是 Data Pipeline 中最经典的设计模式
- [[Kafka]] — Kafka 是 ETL 中常用的数据源（Extract 阶段）

### ← 被指向
- [[User Profiling]] — 用户画像的构建依赖 ETL 流水线从原始行为到结构化特征
- [[Event Stream]] — 事件流数据通过 ETL 转化为可分析的结构化数据
