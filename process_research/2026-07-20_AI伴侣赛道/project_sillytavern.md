---
id: f8a3e9d1-2b4c-5d6e-7f8a-9b0c1d2e3f4a
title: SillyTavern — LLM 角色扮演前端的工业级最佳实践
type: project
tags: [ai-companion, role-play, frontend, llm, prompt-engineering, open-source, 2026]
created: 2026-07-20
updated: 2026-07-20
source: research/2026-07-20_ai-companion-track
relations: ["project_shikigami_protocol", "project_soul_of_waifu", "industry_ai_companion"]
---

# SillyTavern — LLM 角色扮演前端标杆

## Problem（问题）

LLM 角色扮演需要精细的提示词工程和记忆注入，但大多数前端只提供一个裸文本框。如何让角色在长对话中保持一致性？如何让用户在不写代码的情况下管理复杂的角色设定和世界观？SillyTavern 给出了最工业化的答案。

## Background（背景）

- 始于 2023 年初，最初是 TavernAI 的分支
- 快速成为 LLM 角色扮演社区的事实标准前端
- 30,909 GitHub Stars（2026.07），是 AI 伴侣前端类别中最大的开源项目
- 用户（你）已有本地 DRBCV 知识库 (`D:\DRBCV-Knowledge\SillyTavern\`)，共 45 张卡片

## Key Insight（关键洞察）

**五层提示词系统是 SillyTavern 真正的护城河。** 系统提示 → 预设 → 角色卡 → 世界书(Lorebook) → 用户输入，每一层独立配置、按优先级叠加。这不是「一个好用的 UI」，而是一套完整的角色人格编排流水线。

世界书 (Lorebook) 的「关键词触发式记忆注入」是被低估的设计：不依赖向量检索，而是用户显式定义「当提到 X → 注入 Y 条记忆」。这种白盒式记忆管理虽然手动维护成本高，但**完全可控、无幻觉**——对「少女」项目的结构化记忆系统有重要参考价值。

## Architecture（架构）

```
┌────────────────────────────────────────────┐
│  SillyTavern 浏览器前端 (纯 HTML/CSS/JS)     │
├────────────────────────────────────────────┤
│  Express 后端 (Node.js, server.js)          │
│  ┌──────────────────────────────────────┐   │
│  │  五层提示词引擎                        │   │
│  │  系统提示 → 预设 → 角色卡 → 世界书 → 输入│   │
│  ├──────────────────────────────────────┤   │
│  │  多 API 适配层                        │   │
│  │  OpenAI/Claude/KoboldAI/Ooba/本地...  │   │
│  ├──────────────────────────────────────┤   │
│  │  扩展插件系统 (TTS/图片生成/翻译)      │   │
│  └──────────────────────────────────────┘   │
│  数据层: data/ (角色卡/世界书/聊天记录 JSON)  │
└────────────────────────────────────────────┘
```

**值得学习的三个设计：**

1. **世界书 (Lorebook)** — 上下文触发式记忆注入：关键词匹配 → 检索相关条目 → 注入当前提示词。这是「可编程记忆」而非「自动记忆」。
2. **角色卡 (Character Card)** — JSON + PNG embedding 的角色定义标准。v2 规范支持多角色、语气定义、示例对话。
3. **扩展插件系统** — 最小化核心 + 插件扩展：SillyTavern 的核心只做会话管理，TTS、图像生成、翻译全部由插件实现。

## Weakness（缺陷）

- **AGPL-3.0 许可证** — 如果复用代码，你的项目也必须 AGPL
- **纯前端定位** — 不内置 LLM 推理、不内置记忆持久化（依赖第三方）
- **无情感引擎** — 角色没有内在状态机，只靠 prompt 维持一致性
- **技术栈老旧** — jQuery 级别的 JS，部署简单但架构可维护性差
- **手动记忆管理** — 世界书需要用户手写，无法自动演化

## My Take（我的看法）

> SillyTavern 是这个赛道最被低估的学习对象。它的五层提示词架构和世界书设计揭示了「角色人格管理的本质是信息编排（orchestration）问题」。但「少女」项目不能仅做另一个前端——关键是补充 SillyTavern 缺失的「情感引擎 + 记忆自动演化」层。

> 短期策略：用 SillyTavern 作为对话前端 + 「少女」的 Python 后端（人格引擎 + 记忆管线）通过 API 或 MCP 接入。这比从零写前端聪明得多。

## Next Action（下一步）

- [ ] 为 SillyTavern 写一个 MCP 插件，接入 companion-core 人格引擎
- [ ] 将 DRBCV 知识库中 45 张 SillyTavern 卡片与本次研究知识卡片建立关系链接
- [ ] 研究世界书 JSON 格式，设计「自动生成世界书条目」的人格引擎输出格式
