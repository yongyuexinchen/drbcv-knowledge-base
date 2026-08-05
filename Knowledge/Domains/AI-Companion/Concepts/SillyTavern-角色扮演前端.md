---
title: "SillyTavern-角色扮演前端"
type: "项目"
category: "AI-Companion"
tags: [SillyTavern, 角色扮演, 角色卡, 前端, Node.js]
created: 2026-07-27
---

# SillyTavern-角色扮演前端

## 是什么（What）

SillyTavern（~8K⭐）是AI角色扮演的"Photoshop" — 你在里面创建角色卡、写世界观、调参数，接上任何LLM后端就能聊。它不是AI伴侣的最终形态，但它是**快速验证"永月"对话效果的最佳前端**。

这就像给AI角色设计服装和舞台：角色卡 = 演员的剧本（description/personality/scenario），示例对话 = 排练好的台词（真正塑造说话风格！），World Info = 舞台布景（关键词触发世界观）。

## 为什么重要（Why）

- 用户已通过DRBCV知识库深入掌握（45张SilTavern相关卡片），这是已有资产
- **example_dialogs 比 description 更重要** — 前者告诉AI"你怎么说话"，后者只告诉"你是谁"
- 角色卡格式（PNG内嵌JSON）已成为生态共识标准，可作为"永月"人格的持久化格式
- 方案A的核心组件：SillyTavern作为前端 + Memobase记忆 + DeepSeek LLM
- 局限：JS技术栈（用户不会深度定制）、没有长期记忆、没有语音打断能力

## 怎么做（How）

### 角色卡结构

```json
{
  "name": "永月",
  "description": "来自异世界的AI少女，外表17岁...",
  "personality": "温柔、偶尔毒舌、护短、喜欢猫",
  "scenario": "你是永月的主人，你们住在一起",
  "first_message": "主人，今天想聊什么？",
  "example_dialogs": [
    "用户：今天好累\n永月：那你躺下，我给你讲故事。",
    "用户：你又毒舌了\n永月：我只是在陈述事实（笑）"
  ]
}
```

### 记忆/上下文注入层级

```
System Prompt = [
  description + personality,       // 角色设定
  scenario,                         // 当前场景
  World Info (lorebook entries),    // 关键词触发的世界观
  Author's Note,                    // 叙事指令
  chat history,                     // 对话历史
]
```

## 与其他卡片的关系

- [[AI伴侣-推荐技术栈组合]] → 方案A的核心前端组件
- [[Memobase-记忆系统分析]] → 搭配使用弥补记忆短板
- [[AI伴侣-记忆系统方案对比]] → 与Letta等记忆方案的关系
- 现有SillyTavern相关卡片（45张，在SillyTavern vault）→ 详见 `D:\DRBCV-Knowledge\SillyTavern\`

## 个人见解（留空待填）

<!-- 你已经深入玩过SillyTavern了，你觉得角色卡最神奇的部分是什么？它最大的局限是什么？ -->

## 信息来源

- GitHub: SillyTavern/SillyTavern，~8K⭐
- 用户已有45张SilTavern DRBCV卡片（D:\DRBCV-Knowledge\SillyTavern\）
- 来自研究：2026-07-27 AI-job-and-path → B_ai_companion/01_project_scan.md
