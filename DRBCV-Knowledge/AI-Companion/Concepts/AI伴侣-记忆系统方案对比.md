---
title: "AI伴侣-记忆系统方案对比"
type: "概念"
category: "AI-Companion"
tags: [记忆系统, 方案对比, Profile模式, 三层记忆, 角色卡模式]
created: 2026-07-27
---

# AI伴侣-记忆系统方案对比

## 是什么（What）

AI伴侣的记忆不是一个技术问题，而是**信息管理问题**。三种主流模式各有利弊：Memobase的Profile模式（像HR档案）、Letta的三层记忆模式（像人脑）、SillyTavern的角色卡模式（像演员剧本）。AI伴侣的理想记忆应该融合三者。

这就像管理你的私人信息：Profile模式 = Excel表格（结构清晰但冷冰冰），三层记忆 = 大脑（分层管理但太复杂），角色卡 = 名片（一眼知道是谁但没有深度）。

## 为什么重要（Why）

- **记忆决定了AI是"每次重新认识你"还是"记得你的过去"**
- 三种模式各有侧重：Profile管"用户是谁"，Core Memory管"AI是谁"，Archival Memory管"发生过什么"
- 关键洞察：**example_dialogs 塑造说话风格 > personality 形容词标签 > description 外貌描述**
- 对用户："永月"需要的不是其中某一种，而是一个融合三种优点的定制记忆系统

## 怎么做（How）

### 三种模式对比

| 维度 | Profile模式(Memobase) | 三层记忆(Letta) | 角色卡模式(ST) |
|------|---------------------|----------------|---------------|
| 核心理念 | 提取用户事实卡片 | 模拟人脑记忆分层 | 角色=一个JSON文件 |
| 数据结构 | topic/sub_topic/content | Core+Archival+Recall | description+persona+example_dialogs |
| 优势 | 结构清晰、信息密度高 | 分层管理、Agent自主管理 | 格式标准、塑造说话风格 |
| 劣势 | 丢失叙事脉络 | 25MB源码、太重 | 静态、没有长期记忆 |
| 类比 | HR系统员工档案 | 人脑三层记忆 | 演员的剧本 |

### 融合方案：永月的理想记忆架构

```
L1: Persona Block（人格层）
  ← Letta + SillyTavern
  角色卡转为 persona block，Agent可自我改写
  "永月的自我意识"

L2: Profile Store（事实层）
  ← Memobase
  topic/sub_topic/content 结构化用户信息
  "关于主人的档案卡"

L3: Episodic Store（叙事层）
  ← Letta Archival + 优化
  按时间线组织的对话叙事
  "我们之间的故事"

L4: World/Lore（背景层）
  ← SillyTavern Lorebook
  关键词触发的世界观设定
  "这个世界的规则"
```

## 与其他卡片的关系

- [[Memobase-记忆系统分析]] → Profile模式详解
- [[Letta-MemGPT-自主记忆架构]] → 三层记忆详解
- [[SillyTavern-角色扮演前端]] → 角色卡模式详解
- [[AI伴侣-推荐技术栈组合]] → 具体用什么技术实现这个融合方案

## 个人见解（留空待填）

<!-- 你更在意"永月记得你的喜好"还是"永月有独立的自我意识"？这两者冲突吗？ -->

## 信息来源

- 来自研究：2026-07-27 AI-job-and-path → B_ai_companion/04_memory_systems_comparison.md
