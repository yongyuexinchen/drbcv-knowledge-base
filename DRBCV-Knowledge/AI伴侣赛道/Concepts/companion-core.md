---
name: companion-core
type: procedure
status: core
source: "[[mvp_blueprint]], [[opportunity]]"
domain: AI伴侣赛道
---

# companion-core

## 类型判定
过程型 — 它是少女项目的 v0.1 产品蓝图，有明确的实现路径和模块划分。核心指令：`pip install companion-core` — 开源 AI 伴侣人格记忆引擎。

## 是什么
companion-core 是少女项目的 MVP 产品形态：一个开源的 Python 库，提供 AI 伴侣的三大核心能力 — Persona（角色管理）、Emotion（情绪状态机）、Memory（三层记忆）。设计原则：被集成（不被替代）、模块化（可独立使用）、本地优先（默认本地运行）。

## 输入-输出空间
**输入**：角色配置 + 对话文本 + API 调用
**输出**：人格状态 + 情绪参数 + 记忆查询结果 + 上下文注入

## 正例（≥2个）
- v0.1 三模块（工期 ~3 周，零成本）：
  - Persona：角色定义、多角色管理（YAML/JSON 配置文件）
  - Emotion：情绪维度、衰减曲线、触发规则（Python 状态机）
  - Memory：短期（会话）/ 中期（摘要）/ 长期（画像）（ChromaDB + SQLite）
- 集成目标：SillyTavern 通过 MCP 协议接入 engine
- Pipeline：`用户输入 → Memory 检索 → Emotion 更新 → Persona 检查 → LLM 生成 → Memory 存储`

## 反例/边界（≥1个）
- 不是完整应用：不做前端 UI、不做模型推理、不做移动端、不做硬件
- 不是「GPT 套壳」：核心价值在人格一致性和记忆管理，不是模型能力
- v0.1 故意克制：先做最难但最独立的一层（记忆+人格引擎），而非最显眼的一层（前端/视觉）
- 依赖开源 LLM：无法训练基座模型，只能调用 llama.cpp/Ollama/API

## 详细解释
为什么从「引擎」而非「应用」开始：
1. **最高杠杆**：记忆+人格是 5 大竞品的共同盲区
2. **最匹配技能**：Python 后端 + 数据建模是你的核心能力（不需要前端技能）
3. **最独立**：引擎不依赖 UI/前端/社区，可以独立开发和验证
4. **最可验证**：100 轮对话后人格一致性是否保持？→ 可客观测试

三层验证路径：
1. **原型验证（2-3 个月有效开发时间）**：Python CLI 对话界面 + FAISS/ChromaDB + valence-arousal 状态机
2. **中间件化（3-4 个月）**：FastAPI 服务 + MCP 协议 + SillyTavern 对接
3. **完整应用（6-12 个月）**：Live2D/TTS + Tauri 桌面客户端 + 云备份服务

## 细节备注
- 考察中断风险：9-12 月需暂停开发备考，模块化设计允许停摆后无缝恢复
- MCP 接入：作为 Model Context Protocol 服务端，任何 MCP 客户端都可调用
- 商业模式：开源免费 + 可选云备份订阅（加密记忆同步）

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[独立人格]] — Persona 模块的设计基础
- [[情绪状态机]] — Emotion 模块的实现
- [[三层记忆架构]] — Memory 模块的架构基础
- [[本地优先]] — 默认运行模式

### ← 被指向
- [[开源伴侣引擎]] — companion-core 是开源伴侣引擎的具体实现
- [[正交竞争]] — companion-core 定位在正交竞争维度
