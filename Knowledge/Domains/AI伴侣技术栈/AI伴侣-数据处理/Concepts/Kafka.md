---
name: Kafka
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-数据处理
---

# Kafka（Apache Kafka）

## 类型判定
判别型 — 分布式消息队列，AI 伴侣数据系统的「中央神经系统」——所有事件信号在这里汇流、分发、持久化。

## 类比 ★
### 一句话比喻
Kafka 像邮政系统的超级分拣中心——每天有上亿封信（事件）涌进来，Kafka 按收件人地址（Topic）分类，确保每封信不丢、顺序不乱，而且任何想读信的部门（消费者）都可以随时调阅，读完的信不销毁（可重放）。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| Topic（主题） | 邮政分类格——所有「北京的信」进一个格子，「上海的信」进另一个 |
| Consumer Group（消费组） | 流水线上的分拣工——多人协同分拣同一堆信，每人负责一部分 |
| 消息持久化 + 重放 | 信件存档室——所有信都留着，新部门随时可调阅历史信件 |

## 是什么
Apache Kafka 是 LinkedIn 于 2011 年开源的分布式流处理平台。核心是「发布-订阅」模式的消息队列：Producer 将消息写入 Topic，Consumer 从 Topic 中拉取消息。Kafka 的独特性在于：① 消息写入磁盘（不是内存），持久化 + 高吞吐（百万条/秒）；② 消费者可独立控制消费位点（offset），支持历史回放；③ 天然分布式，易于水平扩展。在 AI 伴侣中，Kafka 是所有事件流的「中央通道」。

## 输入-输出空间
- **输入**: Producer（任何服务/应用）向 Topic 写入消息
- **输出**: Consumer（数据处理服务）从 Topic 拉取消息
- **核心概念**: Topic（主题）、Partition（分区，并行单位）、Consumer Group（消费组，负载均衡）

## 正例（≥2 个）
1. **AI 伴侣事件总线**: 用户发消息 → API Server 写入 `chat_events` Topic → Memory Service / Analytics Service / Agent 各自消费
2. **日志采集**: 所有微服务的日志 → Kafka → ELK（Elasticsearch + Logstash + Kibana）→ 实时监控大盘

## 反例/边界（≥1 个）
1. **RabbitMQ**: 传统消息队列，单条消息确认+删除模式——吞吐量远低于 Kafka，不支持历史消息回放——适合「任务队列」而非「事件流」
2. **边界 — 运维复杂度**: Kafka 需要 ZooKeeper/KRaft 集群管理、Partition 规划、Consumer Lag 监控——小规模场景（< 10 万条/天）用 Redis Pub/Sub 更简单

## 详细解释
Kafka 的核心架构：
```
Producer → Broker Cluster → Consumer
              │
          ZooKeeper / KRaft（集群协调）
```
一条消息的生命周期：
```
1. Producer 选择 Partition（按 key hash 或 round-robin）
2. 写入 Leader Broker 的 Partition Log（顺序追加到磁盘）
3. Follower Broker 同步复制（ISR 机制）
4. Consumer 按 offset 顺序拉取 → 处理 → 提交 offset
```
在 AI 伴侣中典型的使用拓扑：
```
[前端 App] → [API Gateway] → Kafka
                                  ├─ Topic: raw_events → Spark → User Profile
                                  ├─ Topic: chat_messages → Memory Service → 向量库
                                  └─ Topic: voice_events → ASR Pipeline → Whisper
```

## 关系
### → 指向
- [[Event Stream]] — Kafka 是 Event Stream 的传输和持久化基础设施
- [[Data Pipeline]] — Kafka 是 Data Pipeline 中连接各个节点的数据总线
- [[Apache Spark]] — Spark Streaming 消费 Kafka Topic 做实时数据处理

### ← 被指向
- [[ETL]] — ETL 从 Kafka 中 Extract 原始事件数据
- [[User Profiling]] — 用户画像系统从 Kafka 消费行为事件来更新特征
