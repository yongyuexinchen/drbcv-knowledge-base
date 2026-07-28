---
title: "Letta-MemGPT-自主记忆架构"
type: "项目"
category: "AI-Companion"
tags: [记忆系统, Letta, MemGPT, Agent, Core Memory, 开源]
created: 2026-07-27
---

# Letta-MemGPT-自主记忆架构

## 是什么（What）

Letta（原MemGPT，~14K⭐）是给AI装的"大脑操作系统" — 有工作记忆（Core Memory）、长期记忆（Archival Memory）、和自主记忆管理（Agent自己决定记什么、忘什么、什么时候回忆）。它是最完整的开源记忆架构，但也因为过度设计（25MB源码）对初学者不友好。

这就像给AI装了三层记忆：Core Memory = 你脑子里正在想的事（"等下要去买菜"），Archival Memory = 你的相册和备忘录（需要时翻出来），Recall Memory = 记忆索引（"好像去年秋天发生过..."）。

## 为什么重要（Why）

- 三层记忆架构是**AI伴侣记忆系统设计的理论天花板**，即使不直接用Letta，它的分层设计也值得借鉴
- **Core Memory 的 persona block** 最关键：Agent可以自己改写"自我认知"——初始是"你是永月，喜欢猫"，100次对话后可能变成"你发现主人心情不好时会说反话，但你不吃这一套"
- git-backed memory（memFS）：记忆存为Markdown文件在git仓库里，支持版本控制和回滚
- 已被 Open-LLM-VTuber 集成为记忆后端
- 对用户的建议：**不推荐直接用**，但必须理解它的三层设计——这是后续自建记忆系统的理论基础

## 怎么做（How）

### 三层记忆架构

```
┌─────────────────────────────────────┐
│  Core Memory（核心记忆 - 常驻）       │
│  ├─ human block: "关于用户的事实"      │
│  ├─ persona block: "AI的人设" ★最关键  │
│  └─ system/*: 规则和知识              │
│  容量：~2000 tokens                  │
├─────────────────────────────────────┤
│  Archival Memory（档案记忆 - 按需）    │
│  对话→embedding→向量数据库→语义检索    │
│  容量：理论上无限                     │
├─────────────────────────────────────┤
│  Recall Memory（回忆记忆 - 索引）      │
│  对话摘要 + 元数据                    │
└─────────────────────────────────────┘
```

### 部署要求

- Postgres + Redis + Embedding 服务
- 支持 20+ LLM provider（OpenAI/Anthropic/DeepSeek/Ollama/vLLM）
- Docker Compose 一键启动
- 最低硬件：取决于跑的LLM（7B约需6GB VRAM）

## 与其他卡片的关系

- [[Memobase-记忆系统分析]] ↔ 更简单的记忆方案对比
- [[AI伴侣-记忆系统方案对比]] → 与其他记忆方案的全面对比
- [[AI伴侣-推荐技术栈组合]] → 方案B中使用Letta作为记忆后端

## 个人见解（留空待填）

<!-- 你觉得"AI能改写自己的人格"是恐怖还是有趣？你希望永月拥有这个能力吗？ -->

## 信息来源

- GitHub: letta-ai/letta（原cpacker/MemGPT），14K⭐
- 来自研究：2026-07-27 AI-job-and-path → B_ai_companion/01_project_scan.md + 04_memory_systems_comparison.md
