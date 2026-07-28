---
id: 018d5a8b-af70-7e5d-be46-ce9f401a5b6c
title: Soul of Waifu — 桌面端 AI 伴侣完整方案
type: project
tags: [ai-companion, live2d, vrm, voice-interrupt, desktop, local-llm, 2026]
created: 2026-07-20
updated: 2026-07-20
source: research/2026-07-20_ai-companion-track
relations: ["project_sillytavern", "project_shikigami_protocol"]
---

# Soul of Waifu — Desktop AI Companion with Live2D/VRM

## Problem（问题）

大多数 AI 聊天在浏览器里进行——一个文本框、一个发送按钮。真正的"陪伴"需要存在感：一个可见的、会动的、能被听到的"存在"。Soul of Waifu 试图通过在桌面上放置 Live2D/VRM 虚拟形象来解决这个问题。

## Background（背景）

- 传统 AI 聊天：浏览器/App 内纯文本
- Character.AI 的 2D 立绘：静态图片 + 对话
- Soul of Waifu：Live2D（动态 2D）+ VRM（3D 模型）+ LipSync + 语音打断

## Key Insight（关键洞察）

**三感合一创造沉浸感：视觉(会动的形象) + 听觉(语音+打断) + 心智(长期记忆) = 真正的"陪伴"。**

两个技术创新值得特别关注：

1. **语音打断（Interrupt）**：用户可以中途打断 AI 说话，AI 会停下来听——这是真人对话的自然模式。大多数 AI 语音系统不支持这个（只能等 AI 说完）。

2. **LipSync 口型同步**：Live2D/VRM 模型的口型与 TTS 音频同步——虚拟形象不只是"站在那"，而是"在说话"。

## Architecture（架构）

- **核心**：Python
- **虚拟形象**：Live2D Cubism SDK + VRM 加载器
- **LLM**：本地 LLM（Ollama 等），多后端支持
- **语音管线**：ASR（语音识别）→ LLM（生成回复）→ TTS（语音合成）→ LipSync（口型同步）
- **交互模式**：全屏聊天 / Desktop Companion Mode（桌面悬浮窗） / RPG 冒险模式

## Desktop Companion Mode 的价值

角色可以以悬浮窗形式出现在桌面上——你在工作时，它在旁边。这不是功能列表中的一项，而是**交互范式**的转变：从"打开 App 聊天"到"角色一直在这里"。

## Weakness（缺陷）

- GPL-3.0 限制商业使用
- 仅 Windows 桌面端
- Live2D SDK 许可复杂
- 单人开发，bus factor 高
- UI 风格偏向二次元，通用性有限

## My Take（我的看法）

> Soul of Waifu 展示了"完整 AI 伴侣"的体验形态——语音打断 + LipSync + 桌面悬浮窗。这些技术不应该只用于"waifu"场景。但作为参考项目，技术选型需要注意：Live2D SDK 许可问题、Python 性能瓶颈、GPL 传染性。如果要实现类似体验，建议：虚拟形象用更开放的标准（VRM），语音打断用更轻量的实现，桌面悬浮窗用 Electron 或 Tauri。

## Next Action（下一步）

- [ ] 研究语音打断（interrupt）的技术实现
- [ ] 评估 VRM 作为虚拟形象标准的可行性（vs Live2D）
- [ ] 探索桌面悬浮窗（Desktop Companion Mode）的跨平台方案
