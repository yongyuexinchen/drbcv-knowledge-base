---
title: "Memobase-记忆系统分析"
type: "项目"
category: "AI-Companion"
tags: [记忆系统, Memobase, 用户画像, Python, 开源]
created: 2026-07-27
---

# Memobase-记忆系统分析

## 是什么（What）

Memobase 是一个 Python 开源记忆后端（~800⭐），核心思路是「AI的CRM系统」— 从对话中自动提取用户特征，分类存档为 `topic → sub_topic → content` 的 Profile 结构，下次对话时按相关性注入 prompt。

这就像你有一个私人秘书：每次你和别人聊天后，秘书在旁边记笔记"他说喜欢猫、讨厌香菜、上个月面试了百度"。下次你再见那个人，秘书递给你一张小抄——你立刻就能接上话题。

## 为什么重要（Why）

- 对用户的意义：Memobase 是所有记忆系统里**代码最简单的**——客户端只有 3 个依赖（pydantic, httpx, openai），Python 初学者能读懂
- 核心流水线：`Blob(对话) → Memobase Server → LLM提取 → Profile(topic/sub_topic/content) → context()检索`
- 优势：结构清晰、信息密度高、可控制注入量（`max_token_size=500`）
- 劣势：丢失叙事脉络（不知道"面试失败"是因为"之前被裁员"）、只能记用户事实不能记角色经历、依赖LLM提取质量

## 怎么做（How）

### 数据模型（Python 视角）

```python
# 这就像把对话切成了"信息卡片"
# 1. Blob = 原始数据（快递包裹）
class ChatBlob:
    messages: list[Message]  # {role, content}

# 2. 服务端处理后 → Profile（从快递中提取的"关于这个人的便签"）
# topic/sub_topic/content 三级分类
# 例: topic="职业", sub_topic="面试", content="2026年7月面试了百度AI岗位"

# 3. 下次对话时 context() 检索相关 Profile 注入 prompt
# 就像秘书递过来的"关于这个人的备忘条"
```

### 部署

- 云服务为主（api.memobase.dev），免费额度有限
- 可本地部署服务端（FastAPI），需自搭数据库和LLM
- 客户端：`pip install memobase` 即可

## 与其他卡片的关系

- [[Letta-MemGPT-自主记忆架构]] ↔ 记忆架构的更复杂替代方案
- [[AI伴侣-记忆系统方案对比]] → 在AI伴侣场景中与其他方案的全面对比
- [[AI伴侣-推荐技术栈组合]] → 方案A中使用 Memobase 作为记忆后端

## 个人见解（留空待填）

<!-- 你觉得"用户画像式记忆"和"日记式记忆"哪种更好？永月应该用哪种？ -->

## 信息来源

- GitHub: memodb-io/memobase
- 来自研究：2026-07-27 AI-job-and-path → B_ai_companion/01_project_scan.md
