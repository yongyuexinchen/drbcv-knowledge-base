---
name: SillyTavern
type: discriminant
status: core
source: "[[github_analysis]], [[competitor]]"
domain: AI伴侣赛道
---

# SillyTavern（酒馆）

## 类型判定
判别型 — 它是目前最成熟的开源 AI 角色扮演前端。与少女项目是互补关系（前端借力），而非竞争关系。

## 是什么
SillyTavern（酒馆）是一个开源的 LLM 前端总控台，30.9k GitHub Stars。支持几乎所有主流 LLM API（OpenAI、Claude、本地 Ollama 等）、角色卡系统（Character Card v2 格式）、多角色群聊、世界书（World Info/Lorebook）、插件扩展。它是开源角色扮演社区的基础设施。

## 输入-输出空间
**输入**：角色卡 + LLM API/本地模型配置
**输出**：Web 聊天界面 + 角色扮演会话

## 正例（≥2个）
- 支持 50+ LLM 后端：OpenAI、Claude、KoboldAI、Ollama、TextGen 等
- 角色卡生态：社区大量分享角色卡，Character Card v2 格式成为事实标准
- 世界书/Lorebook：为角色添加可动态注入的世界观设定

## 反例/边界（≥1个）
- SillyTavern 是前端工具，不提供人格引擎/记忆系统 — 这是少女项目的互补点
- 不提供「AI 朋友」体验：它是角色扮演工具，不是 AI 伴侣 — 没有关系持续性
- 学习曲线陡峭：配置复杂（API、模型、角色卡），非技术用户难以使用

## 详细解释
SillyTavern 与少女项目的关系：
- **互补 > 竞争**：SillyTavern 做前端 UI，companion-core 做后端引擎
- **集成目标**：companion-core 通过 MCP 协议接入 SillyTavern，增强其长期记忆和独立人格能力
- **市场验证**：SillyTavern 的 30k⭐ 证明了开源角色扮演社区的需求真实且庞大

五层开源生态中的 SillyTavern：
```
硬件载体 → 前端 UI (SillyTavern 30k⭐) → 角色引擎 (少女项目) → 记忆系统 (Memobase) → LLM 推理 (Ollama)
```
SillyTavern 在前端层是王者，但在引擎层完全缺失 — 这就是 companion-core 的切入点。

## 细节备注
- 许可证：AGPL-3.0，需要注意集成时的许可证兼容性
- 社区：Discord + Reddit，是 AI 角色扮演社区的中心枢纽
- 少女项目策略：不是 fork 或替代 SillyTavern，而是增强它

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### ← 被指向
- [[companion-core]] — companion-core 的目标集成平台
- [[AI伴侣]] — SillyTavern 是开源 AI 伴侣生态的前端基础设施
- [[开源伴侣引擎]] — 引擎层是 SillyTavern 缺失的能力
