---
id: 018d5a8b-8d5e-5f3b-9c24-ac7f2e3d4c5d
title: Shikigami Protocol — 架构优先的 AI 角色伴侣框架
type: project
tags: [ai-companion, state-machine, memory-pipeline, local-first, persona-engine, 2026]
created: 2026-07-20
updated: 2026-07-20
source: research/2026-07-20_ai-companion-track
relations: ["project_memobase", "project_front_porch", "project_roleplay_chatbot"]
---

# Shikigami Protocol — Architecture-First AI Character Companion

## Problem（问题）

大多数 AI 聊天工具"关闭标签页就归零"——没有持久人格、没有情绪演化、没有主动性。角色只是 prompt 的产物，不是"有内在状态的存在"。

## Background（背景）

- SillyTavern 等前端通过 prompt engineering 维持角色一致性
- 但 prompt 只能描述角色——无法让角色"感受"和"演化"
- 真正的人格需要：情绪状态、能量水平、对用户的态度、记忆积累、主动行为意愿

## Key Insight（关键洞察）

**人格不是 prompt，是状态机。** Shikigami 的三维状态机（情绪 × 能量 × 亲和力）给出了 AI 人格的数学骨架。情绪是瞬时震荡，能量是衰减曲线，亲和力是长期累积信号——三者组合决定了角色在任意时刻的"感受"和"行为倾向"。

## Architecture（架构）

```
┌──────────────────────────────────────┐
│  前端: Electron + Vue                 │
├──────────────────────────────────────┤
│  后端: FastAPI (Python 3.10+)         │
│  ┌────────────────────────────────┐  │
│  │  Personality State Machine     │  │
│  │  情绪(±1) × 能量(0-100) × 亲和力 │  │
│  ├────────────────────────────────┤  │
│  │  Memory Pipeline               │  │
│  │  事实提取 → 向量存储 → 每日摘要  │  │
│  ├────────────────────────────────┤  │
│  │  Proactive Engine              │  │
│  │  后台反思 + 主动搭话            │  │
│  └────────────────────────────────┘  │
│  LLM: Ollama / LM Studio / API       │
└──────────────────────────────────────┘
```

**三个突破性设计：**

1. **Proactive Speech（主动搭话）**：沉默一段时间后，角色主动发起对话。这打破了"AI 只能响应"的范式。
2. **Background Reflection（后台反思）**：角色在空闲时回顾对话，形成新的"想法"。
3. **Energy Decay（能量衰减）**：角色有"精力"概念，长时间对话会导致疲劳。

## Weakness（缺陷）

- Star 极少（3），未经验证
- Electron + Python 双进程部署复杂
- AGPL-3.0 许可证
- Beta 阶段，稳定性和性能未知

## My Take（我的看法）

> 这是整个 GitHub 扫描中**与我的目标最契合**的项目。三维状态机 + 记忆管线 + 主动行为——恰好就是我要构建的"有独立人格的 AI 伴侣"的核心。但项目太小、太新，不能直接作为基础——应该深入研究其设计理念，用自己的技术栈重新实现核心机制（状态机、记忆管线、主动行为），结合 memobase 的记忆层和更成熟的前端。

## Next Action（下一步）

- [ ] 阅读 Shikigami-Protocol 源码，提取状态机实现
- [ ] 设计自己的三维（或更多维度）人格状态机
- [ ] 评估：用 Python 重写核心引擎（FastAPI），前端用更轻量的方案
