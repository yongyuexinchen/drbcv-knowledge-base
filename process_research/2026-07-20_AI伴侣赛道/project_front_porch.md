---
id: 018d5a8b-9e6f-6d4c-ad35-bd8f3e4d5e6f
title: Front Porch AI — Realism Engine 与社区驱动角色生态
type: project
tags: [ai-companion, realism-engine, flutter, local-first, community-hub, 2026]
created: 2026-07-20
updated: 2026-07-20
source: research/2026-07-20_ai-companion-track
relations: ["project_shikigami_protocol", "project_memobase"]
---

# Front Porch AI — Realism Engine & Community Hub

## Problem（问题）

AI 陪伴不应该只是"发消息-回消息"。真正的陪伴感需要角色具有内在状态（情绪、信任、需求），且这些状态随互动自然演化。但大多数开源方案缺乏这个层。

## Background（背景）

- Backyard AI（商业 AI 陪伴产品）关闭后，用户群体流散
- Front Porch AI 明确定位为"Backyard AI 难民之家"
- 用 Flutter 实现跨平台桌面应用（Windows/macOS/Linux）

## Key Insight（关键洞察）

**Realism Engine 是 AI 陪伴"人格化"的核心组件。** 它不是简单的 prompt 工程，而是一个运行在后台的状态机：

```
Realism Engine = 情绪(emotion) + 信任(trust) + 需求(needs) + 记忆(memory)
```

角色不只是回复文本——它在每一轮交互中更新内部状态，而这些状态影响回复的语气、内容、甚至是否愿意回复。

第二个关键洞察是 **社区驱动的角色分发**：The Stoop 将角色社区直接内置到应用中——浏览、下载、评价、关注创作者——不需要离开 App 就能获取新角色。这解决了 AI 陪伴产品的冷启动问题。

## Architecture（架构）

- **框架**：Flutter (Dart) — 一次编写，三平台运行
- **LLM 后端**：KoboldCpp (GGUF) 本地 + OpenRouter/Nano-GPT/OpenAI 远程
- **Realism Engine**：独立的状态管理层，驱动角色行为
- **The Stoop**：内置社区中心（角色卡分享、评价、下载）

## Weakness（缺陷）

- Star 只有 50，社区极小
- Flutter 桌面端性能不如原生
- AGPL-3.0 许可证限制
- 快速迭代期，API 不稳定

## My Take（我的看法）

> Realism Engine 的设计理念应该成为任何 AI 陪伴项目的标配——角色必须有内在状态，状态必须随互动演化。The Stoop 社区模式也有启发：与其自己创建所有角色，不如构建一个角色生态。但 Flutter + AGPL-3.0 的技术选型对我的项目不太合适——应该提取 Realism Engine 的设计理念，用 Python 重实现。

## Next Action（下一步）

- [ ] 研究 Realism Engine 的四个维度（emotion, trust, needs, memory）的数学模型
- [ ] 设计自己的角色状态机，融合 Shikigami 的三维 + Front Porch 的四维
- [ ] 考虑角色社区的轻量实现方式（GitHub-based 角色卡仓库？）
