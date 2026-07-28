---
id: 018d5a8b-7c4f-4e2a-8f13-9b6e1d2f3a4b
title: Memobase — User Profile-Based LLM 长期记忆系统
type: project
tags: [ai-companion, memory, llm, profile-based, infrastructure, 2026]
created: 2026-07-20
updated: 2026-07-20
source: research/2026-07-20_ai-companion-track
relations: ["project_shikigami_protocol", "project_roleplay_chatbot"]
---

# Memobase — User Profile-Based Long-Term Memory

## Problem（问题）

LLM 对话每次都是从零开始。即使加了 RAG，也只是检索相似文本——它不理解"用户是什么样的人"。AI 陪伴需要的不只是记住说了什么，而是理解用户是谁、偏好什么、关系如何演化。

## Background（背景）

- 传统方案：LangChain ConversationBufferMemory（保留最近 N 条消息）或向量 RAG（语义检索历史）
- 问题：RAG 返回的是原始对话片段，不是结构化的"用户画像"
- Memobase 的方案：从对话中提取结构化 profile（用户偏好、习惯、关系状态），动态更新，按需注入 LLM 上下文

## Key Insight（关键洞察）

**Profile-based memory 优于 chunk-based memory。** 将记忆组织为"用户画像字段"而非对话片段，可以让 LLM 真正理解"面对的是怎样的人"，而不仅是"之前聊过什么"。

## Architecture（架构）

```
对话 → Profile Extractor → User Profile DB
                                ↓ 注入
                           LLM Context
```

- Profile 是动态的：每次对话后更新
- 支持 MCP (Model Context Protocol) 原生集成
- 多语言 SDK：Python / JS / Go

## Comparison with Alternatives（替代方案对比）

| 方案 | 特点 | 局限 |
|------|------|------|
| RAG + Vector DB | 检索相似历史 | 返回片段，不形成用户理解 |
| Conversation Summary | 压缩对话为摘要 | 丢失细节，无结构化字段 |
| Memobase Profile | 用户画像字段 | 过度结构化可能丢失 nuance |

## My Take（我的看法）

> Memobase 是 AI 陪伴记忆基础设施的最佳候选。profile-based 方法更适合"长期关系"场景（用户偏好不会天天变）。但需要补充：profile 应该和对话摘要/向量检索共存——profile 提供用户画像，RAG 提供具体记忆，Summary 提供近期上下文。三者互补而非互斥。

## Next Action（下一步）

- [ ] 实验 Memobase Python SDK
- [ ] 对比 profile-based vs 三层记忆（roleplay_chatbot）的实际效果
- [ ] 设计混合记忆架构：Profile + RAG + Summary + Graph
