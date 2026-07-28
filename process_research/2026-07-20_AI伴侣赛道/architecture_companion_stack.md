---
id: b8d4e2f1-3a6c-4d9e-8b12-c7f5a3d0e9f1
title: AI 伴侣通用技术栈 — 四层架构与选型对比
type: principle
tags: [ai-companion, architecture, tech-stack, memory, personality, local-first]
created: 2026-07-20
updated: 2026-07-20
source: research/2026-07-20_ai-companion-track
relations: []
---

# AI 伴侣通用技术栈 — 四层架构与选型对比

## Problem（问题）

AI 伴侣系统涉及 LLM 推理、长期记忆、人格建模、多模态交互等多个子系统，缺乏统一的架构参考。开发者（尤其是个人开发者）需要知道：各层应该用什么技术？已有开源方案是什么？哪里是空白？

## Background（背景）

通过对 15 个 GitHub 开源项目 + 5 个商业产品的架构拆解，AI 伴侣赛道已沉淀出四层技术栈，每层都有成熟方案和未解决的缺口。2024-2026 年趋势是从「纯 Prompt 人格」走向「状态机 + 记忆联动」的系统化架构。

## Key Insight（关键洞察）

### 四层架构（自下而上）

```
Layer 1: 基座模型层 (Foundation Models)
  职责: LLM 推理、Embedding、TTS/STT
  现状: 成熟，选型丰富
  
Layer 2: 记忆与人格层 (Memory & Personality Engine)  ← 核心战场
  职责: 短期/中期/长期记忆、情绪状态机、关系数值、人格一致性
  现状: 最大空白，无人真正解决
  
Layer 3: 交互界面层 (Interaction Layer)
  职责: Web/App/桌面客户端、Live2D/VRM 渲染、语音管道
  现状: SillyTavern 等前端成熟，可复用
  
Layer 4: 分发与硬件层 (Distribution & Hardware)
  职责: 应用商店、开源社区、ESP32 硬件、AR 眼镜
  现状: 非个人开发者主战场
```

### 各层选型对比

**Layer 1 — 基座模型层：**

| 组件 | 方案 | 适用场景 | Star / 成熟度 |
|------|------|---------|--------------|
| LLM 推理 | Ollama + llama.cpp | 本地部署，隐私优先 | 极成熟 |
| LLM 推理 | OpenAI / DeepSeek API | 云端，低门槛 | 商业成熟 |
| Embedding | text-embedding-3-small / bge-large | 语义检索 | 成熟 |
| TTS | Kokoro-FastAPI (5.2k★) | 本地高质量语音合成 | 推荐首选 |
| STT | Whisper (OpenAI) | 语音识别 | 成熟 |

**Layer 2 — 记忆与人格层（核心战场）：**

| 组件 | 方案 | 优势 | 缺口 |
|------|------|------|------|
| 短期记忆 | 滑动窗口（对话历史） | 简单有效 | 无 |
| 中期记忆 | LLM 摘要 + SQLite | 压缩信息 | 缺少自动化标准 |
| 长期记忆 | FAISS / ChromaDB / Qdrant | 语义检索 | 无跨层融合 |
| 用户画像记忆 | Memobase (2.8k★) | 专为伴侣设计的记忆中间件 | 缺少关系演化 |
| 图结构记忆 | nocturne_memory (1.3k★) | 实体关系图存储 | 早期项目 |
| 情绪状态机 | 无开源成熟方案 | — | **最大空白** |
| 关系数值系统 | 无开源成熟方案 | — | **无人解决** |
| 人格注入算法 | 所有项目都用 Prompt | — | 无动态注入方案 |

**Layer 3 — 交互界面层：**

| 组件 | 方案 | 适用场景 | Star |
|------|------|---------|------|
| 角色扮演前端 | SillyTavern (30.9k★) | 最成熟的 LLM 前端 | 首选复用 |
| LLM 通用前端 | Open WebUI (146k★) | 通用聊天界面 | 可参考 |
| Live2D 渲染 | Airi (42.9k★) | 自托管 Live2D 角色 | 高参考价值 |
| VRM 3D 渲染 | Utsuwa / Soul of Waifu | 3D 角色展示 | 早期 |
| 桌面框架 | Tauri / Electron | 跨平台桌面应用 | 成熟 |
| MCP 协议 | MCP SDK (Anthropic) | 标准化接入 | 推荐 |

### 架构决策树（个人开发者视角）

```
你有 GPU 吗？
├── 有 → Ollama 本地推理（完全隐私）
└── 没有 → DeepSeek API（便宜好用）

你做 LSD（Lore/Story/Dialogue）前端吗？
├── 不做 → 复用 SillyTavern（30k Stars，用户基础雄厚）
└── 要做 → 至少需要 6 个月 + 前端技能

你的核心差异化是什么？
├── 人格系统 → 做 Layer 2（记忆+人格引擎），接 SillyTavern
├── 角色渲染 → 做 Layer 3（Live2D/VRM 前端）
└── 商业模式 → 做 Layer 4（分发/社区）
```

### 核心架构洞察

1. **Layer 1 是 commodity** — 模型层选型丰富、开源成熟，不需要自己造轮子
2. **Layer 2 是蓝海** — 记忆和人格引擎全赛道无人真正解决，是最大的技术机会
3. **Layer 3 可复用** — SillyTavern 已有 30K+ Stars 的社区，作为前端零成本
4. **正交竞争策略** — 不在 Layer 1（大厂碾压）和 Layer 3（已有成熟方案）竞争，聚焦 Layer 2

### 少女项目的架构定位

```
不作为「完整产品」出现，而是作为 Layer 2 中间件：

SillyTavern (Layer 3) ──MCP──→ companion-core (Layer 2) ──API──→ Ollama/DeepSeek (Layer 1)
                                          │
                                    ┌─────┴─────┐
                              情绪状态机    三层记忆系统
                              关系数值      主动交互引擎
                              人格注入      情感动力学
```

技术栈选型：Python + FastAPI + FAISS + SQLite + MCP SDK + Ollama API
完全不依赖自有前端，只做后端引擎。

### 值得借鉴的开源项目

- **Airi** — Engine 适配层设计（统一多 LLM 后端接口）、Live2D 渲染集成、插件架构
- **SillyTavern** — 五层提示词架构（系统→预设→角色卡→世界书→用户输入）、世界书关键词触发机制
- **Memobase** — 专为 AI 伴侣设计的用户画像长期记忆中间件
- **Shikigami Protocol** — 情绪×能量×好感三维状态机 + 主动搭话触发
- **Front Porch AI** — Realism Engine（emotion, trust, needs, memory）本地优先桌面应用

## My Take（我的看法）

> [个人见解空框，留待填充]
