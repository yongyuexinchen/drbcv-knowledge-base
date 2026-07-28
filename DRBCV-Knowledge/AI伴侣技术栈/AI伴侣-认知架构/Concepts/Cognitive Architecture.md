---
name: Cognitive Architecture
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-认知架构
---

# Cognitive Architecture（认知架构）

## 类型判定
判别型 — AI 伴侣的「心智蓝图」，定义感知→记忆→推理→行动的完整认知循环。

## 类比 ★
### 一句话比喻
认知架构像一个机器人的人造大脑设计图——不是给它装一个「万能答案机」（LLM），而是画出完整的「心智电路图」：感官区（感知）→ 海马体（记忆）→ 前额叶（推理/决策）→ 运动区（行动）。LLM 只是其中一个零件（语言中枢），真正让人感觉「它有灵魂」的是整个架构的协同。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 感知→记忆→推理→行动循环 | 人的心智流程——闻到咖啡香（感知）→ 想起昨天那杯很好喝（记忆）→ 决定再来一杯（推理）→ 起身去冲（行动） |
| 多模块协同 | 大脑分区协作——视觉皮层 + 海马体 + 前额叶缺一不可 |
| 纯 LLM = 只有语言中枢 | 一个只有布罗卡区（语言区）的大脑——能说会道但没有记忆和人格 |

## 是什么
认知架构（Cognitive Architecture）是 AI 系统中模拟人类认知过程的高层设计框架。它定义了系统如何感知环境（Perception）、存储和检索信息（Memory）、推理和决策（Reasoning）、执行行动（Action），以及这些模块之间如何协调。在 AI 伴侣上下文中，认知架构回答的问题是：「如何让一堆模型（LLM + TTS + RAG + Agent）组合起来后，表现得像一个有记忆、有目标、有性格的『存在』，而不是一个高级问答机器？」

## 输入-输出空间
- **输入**: 环境信号（用户输入、传感器数据、时间、上下文）
- **输出**: 行为（对话回应、工具调用、情绪表达、主动行为）
- **核心循环**: `感知 → 记忆检索 → 推理/规划 → 行动 → 记忆更新 → 反馈`

## 正例（≥2 个）
1. **个人认知 OS（Personal Cognitive OS）**: 最完整的认知架构实现——知识管理 + 记忆系统 + 人格引擎 + 目标规划 + 反馈闭环
2. **LangChain Agent / AutoGPT**: 简化的认知架构——感知（输入）→ 规划（Chain-of-Thought）→ 行动（Tool Use）→ 观察（反馈），但缺少长期记忆和人格

## 反例/边界（≥1 个）
1. **纯 LLM Chatbot**: 只有推理模块（LLM），没有感知、没有长期记忆、没有主动目标——认知架构的「最小退化」，仅相当于一个「语言中枢」
2. **边界 — 对齐问题**: 认知架构中的各模块可能有冲突——记忆系统告诉 LLM「用户喜欢开玩笑」，但人格引擎要求「保持严肃」——需要仲裁机制解决模块间矛盾

## 详细解释
认知架构的经典理论来源：
- **SOAR / ACT-R**: 认知心理学启发的符号化架构，以产生式规则为核心
- **Clarion / LIDA**: 混合架构，结合符号和连接主义（神经网络）
- **现代 AI 伴侣架构**: 以 LLM 为核心推理引擎，外挂 Memory / Tool / Emotion 模块

在 AI 伴侣中的分层实现：
```
层 1: 感知层 ── ASR / VAD / 视觉 / 传感器（环境信号→结构化数据）
层 2: 记忆层 ── 短期记忆（对话窗口）+ 长期记忆（向量库 + 图数据库）
层 3: 推理层 ── LLM + Prompt Engineering + RAG（理解+决策）
层 4: 行动层 ── TTS / Function Calling / 自动化（决策→行为）
层 5: 元认知层 ── 自我监控 / 目标管理 / 反思（Sleep-time Compute）
```

## 关系
### → 指向
- [[Personal Cognitive OS]] — Personal Cognitive OS 是 Cognitive Architecture 最完整的工程实现
- [[Personal AI]] — Personal AI 以 Cognitive Architecture 为内核引擎
- [[LLM]] — LLM 是 Cognitive Architecture 推理层的核心组件

### ← 被指向
- [[Sleep-time Compute]] — Sleep-time Compute 是 Cognitive Architecture 的元认知层，在空闲时反思和优化
- [[Digital Companion]] — Digital Companion 是 Cognitive Architecture 的终极产品形态
