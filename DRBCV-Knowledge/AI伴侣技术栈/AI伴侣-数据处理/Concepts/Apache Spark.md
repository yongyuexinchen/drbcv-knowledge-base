---
name: Apache Spark
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-数据处理
---

# Apache Spark

## 类型判定
判别型 — 分布式计算引擎，AI 伴侣大数据处理的「超级工厂」，擅长在成百上千台机器上并行分析海量数据。

## 类比 ★
### 一句话比喻
Spark 像一个拥有十万个「数据分析师」的巨型办公大楼——你下达一个分析任务（「统计过去一年所有用户的说早安次数」），它把任务撕成十万份，每份交给一个分析师同时干活，最后一个人把结果汇总交给你。一个人干一年的事，Spark 一分钟干完。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 分布式并行计算 | 巨型办公大楼——把大任务撕碎，每个办公间同时干活 |
| RDD / DataFrame | 标准化的分析表格——所有分析师用同一套表格格式 |
| Lazy Evaluation | 项目经理先画流程图不执行——规划好全部步骤，最后一口气跑 |

## 是什么
Apache Spark 是一个开源的分布式计算框架，由 UC Berkeley AMPLab 于 2009 年创建。核心创新：基于内存的计算引擎（比 Hadoop MapReduce 快 100 倍）+ 统一的批处理/流处理/ML/图计算 API。在 AI 伴侣技术栈中，Spark 负责离线数据处理的「重活」——分析 PB 级用户行为日志、训练用户画像模型、生成推荐特征等。

## 输入-输出空间
- **输入**: 分布式存储中的数据（HDFS、S3、数据库），支持结构化（DataFrame）、半结构化（JSON）、非结构化
- **输出**: 转换后的数据集、聚合统计结果、模型参数
- **编程模型**: RDD（低级弹性分布式数据集）→ DataFrame（结构化）→ Spark SQL → MLlib

## 正例（≥2 个）
1. **用户行为分析**: 分析百万用户过去 90 天的对话日志——统计聊天频率、情感趋势、话题分布 → Spark 批处理
2. **用户画像特征工程**: 从原始行为日志中提取特征（活跃时段、话题偏好、情绪曲线）→ MLlib 训练聚类模型

## 反例/边界（≥1 个）
1. **单机 Pandas**: 数据量 < 1GB 时，Pandas 比 Spark 快且简单——杀鸡不用牛刀，Spark 的分布式启动开销可能超过计算本身
2. **边界 — 实时交互查询**: Spark 不是 OLTP 引擎——不能像 Redis/PostgreSQL 那样毫秒级响应用户的实时查询，Spark 适合离线批处理和分析型查询

## 详细解释
Spark 的核心抽象：
```
RDD (Resilient Distributed Dataset)
 ├─ 不可变、可分区的数据集合
 ├─ 容错：通过 Lineage（血统）在失败时重建
 └─ 操作类型：Transformation（lazy）+ Action（触发计算）

DataFrame / Dataset ── 在 RDD 上加了 Schema，支持 SQL 查询
```
在 AI 伴侣数据处理管线中：
```
原始日志（Kafka）→ Spark Streaming（实时聚合）→ Spark SQL（离线分析）
                              ↓
                        用户画像（User Profile）→ 存回数据库
```
典型部署：Spark on Kubernetes / YARN，数据存储在 HDFS 或 S3 兼容存储。

## 关系
### → 指向
- [[ETL]] — Spark 是 ETL 工作流的核心执行引擎
- [[Data Pipeline]] — Spark 是数据流水线中最常用的分布式计算节点
- [[Kafka]] — Spark Streaming 消费 Kafka 中的实时事件流

### ← 被指向
- [[User Profiling]] — 用户画像依赖 Spark 完成大规模特征工程和模型训练
- [[Event Stream]] — 事件流数据通过 Spark 进行聚合和模式挖掘
