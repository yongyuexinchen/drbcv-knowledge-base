# 推荐技术组合方案：AI 伴侣"永月"系统

> 基于 6 个项目的深度调研，面向 Python 初学者，给出 3 套可行方案
> 核心原则：本地优先、开箱即用、渐进式学习

---

## 方案总览

| 方案 | 代号 | 难度 | 首版时间 | 月成本 | 适用场景 |
|------|------|------|----------|--------|----------|
| A | 搭积木 | ⭐⭐ | 1周 | ¥0-30 | 快速原型验证 |
| B | 魔改精英 | ⭐⭐⭐ | 1-2月 | ¥0-50 | 功能完整版 |
| C | 从零造轮子 | ⭐⭐⭐⭐⭐ | 6-12月 | ¥0 | 终极控制权 |

---

## 方案A：【搭积木】— 快速原型验证

**一句话**：用现成开源项目拼出一个能跑的原型，验证"永月"的可行性。

### 技术栈

```
┌─────────────────────────────────────┐
│         方案A：搭积木                 │
│                                     │
│  前端/交互：SillyTavern              │
│  (角色卡 + 对话UI + 多API支持)       │
│              │                      │
│  记忆后端：Memobase                  │
│  (Profile提取 + 结构化记忆)          │
│              │                      │
│  LLM：DeepSeek API                  │
│  (你已在用的，¥1/百万token)          │
│              │                      │
│  语音：edge-tts (免费)               │
│  + sherpa-onnx (本地STT)            │
└─────────────────────────────────────┘
```

### 具体步骤

```bash
# 第1步：启动 SillyTavern（你已熟悉）
cd SillyTavern
npm install && npm start
# → 访问 http://localhost:8000

# 第2步：部署 Memobase 服务端
cd memobase
pip install -r requirements.txt
# 启动 FastAPI 服务
python -m uvicorn api.api:app --host 0.0.0.0 --port 8001

# 第3步：写一个简单的桥接脚本（这就是你要学的核心！）
# bridge.py — 约 50 行代码
from memobase import MemoBaseClient
from openai import OpenAI
import requests

# 连接 Memobase
mb = MemoBaseClient(api_key="your_key", project_url="http://localhost:8001")

# 当 SillyTavern 发来消息时：
def on_message(user_id, user_message, ai_response):
    # 1. 提取记忆
    mb.get_user(user_id).insert(ChatBlob(messages=[
        {"role":"user","content":user_message},
        {"role":"assistant","content":ai_response}
    ]))
    # 2. 获取上下文（下次对话前注入）
    context = mb.get_user(user_id).context(max_token_size=500)
    return context
```

### 成本估算

| 项目 | 月费 |
|------|------|
| DeepSeek API | ¥10-30（日常对话量） |
| edge-tts | ¥0（微软免费） |
| Memobase 本地 | ¥0 |
| SillyTavern | ¥0 |
| **合计** | **¥10-30/月** |

### 优势
- ✅ **1 周内可跑起来** — 所有组件都是现成的
- ✅ SillyTavern 你已深入掌握（45张DRBCV卡片）
- ✅ Memobase 代码极简（3个依赖），适合学习
- ✅ 成本极低（几乎只有 LLM API 费用）

### 劣势
- ❌ SillyTavern 是 JS，你无法深度定制
- ❌ Memobase 的记忆是"用户画像"不是"角色记忆"
- ❌ 没有语音打断、Live2D 等高级功能
- ❌ 桥接脚本需要你自己维护

### 学习曲线
```
Week 1: 搭环境，跑通 SillyTavern + Memobase
Week 2: 写桥接脚本，理解 Blob→Profile→Context 流水线
Week 3: 调优角色卡和记忆提取 prompt
Week 4: 添加 TTS 语音输出
```

**推荐指数：⭐⭐⭐⭐⭐ 最适合现在开始！**

---

## 方案B：【魔改精英】— 功能完整版

**一句话**：基于 Open-LLM-VTuber 改造，加上 Letta 的完整记忆能力。

### 技术栈

```
┌─────────────────────────────────────┐
│         方案B：魔改精英               │
│                                     │
│  前端/交互：Open-LLM-VTuber (改造)    │
│  (语音对话 + Live2D + 实时打断)       │
│              │                      │
│  记忆后端：Letta/MemGPT              │
│  (Core+Archival+Recall三层记忆)      │
│              │                      │
│  人格引擎：SillyTavern 角色卡格式     │
│  (导入到 Letta 的 persona block)     │
│              │                      │
│  LLM：DeepSeek API + 本地备用        │
│              │                      │
│  TTS：sherpa-onnx (本地免费)         │
│  STT：sherpa-onnx (本地免费)         │
│  Live2D：现成模型或购买              │
└─────────────────────────────────────┘
```

### 关键改造点

1. **Open-LLM-VTuber 的角色系统太薄**
   - 改造：让它支持 SillyTavern 格式的角色卡（PNG/JSON）
   - 把角色卡的 personality + example_dialogs 注入到 Letta 的 persona block

2. **记忆从 Memobase 换到 Letta**
   - Open-LLM-VTuber 已经依赖 letta-client
   - 只需配置 Letta Server + 写好 persona block
   - Letta 的 Archival Memory 可以提供"语义搜索记忆"能力

3. **Live2D 模型**
   - 现有免费模型可选（如 Mashiro）
   - 也可购买/定制"永月"专属模型
   - Live2D Cubism Editor 订阅：约 ¥200/年

### 成本估算

| 项目 | 初始投入 | 月费 |
|------|----------|------|
| 硬件（建议 RTX 4060 8GB） | ¥3,000-5,000 | ¥0 |
| DeepSeek API | ¥0 | ¥10-30 |
| Live2D Editor（可选） | ¥200/年 | ¥17 |
| sherpa-onnx TTS/STT | ¥0 | ¥0 |
| **合计** | **¥3,200-5,200** | **¥10-50/月** |

### 优势
- ✅ 语音+视觉+记忆完整方案
- ✅ Open-LLM-VTuber 已集成 Letta（依赖即路线）
- ✅ 本地 TTS/STT 零费用
- ✅ Live2D 让"永月"有视觉形象

### 劣势
- ❌ Letta 代码极其复杂（25MB），学习曲线陡峭
- ❌ 需要改造 Open-LLM-VTuber 的角色系统
- ❌ Live2D 模型制作门槛高
- ❌ 硬件要求：建议有独立 GPU

### 学习曲线
```
Month 1: 部署 Letta Server + Open-LLM-VTuber，跑通基础流程
Month 2: 理解 Letta Core Memory / Archival Memory
Month 2: 改造角色系统，导入 ST 角色卡
Month 3: 调优记忆、TTS、Live2D
```

**推荐指数：⭐⭐⭐⭐ 中长期目标**

---

## 方案C：【从零造轮子】— 终极控制权

**一句话**：吸收所有项目的设计精华，用 Python 从零搭建"永月"专属系统。

### 技术栈

```
┌─────────────────────────────────────┐
│         方案C：从零造轮子              │
│                                     │
│  后端框架：FastAPI + WebSocket       │
│                                     │
│  记忆系统（自建三层）：               │
│  ├─ Core Memory: SQLite/JSON        │
│  ├─ Profile 提取: LLM结构化输出      │
│  └─ Archival Memory: ChromaDB向量库  │
│                                     │
│  人格系统：                          │
│  ├─ 角色卡（兼容ST格式）             │
│  └─ 人格向量（可选，进阶）            │
│                                     │
│  前端：可选（渐进式）                 │
│  ├─ Phase 1: 终端/TUI               │
│  ├─ Phase 2: Web (Gradio/Streamlit) │
│  └─ Phase 3: Live2D集成             │
│                                     │
│  LLM：DeepSeek API / Ollama本地     │
│  TTS：edge-tts / sherpa-onnx        │
└─────────────────────────────────────┘
```

### 核心设计理念

```python
# 从 Memobase 学到的：Profile 提取模式
# 从 Letta 学到的：三层记忆架构
# 从 SillyTavern 学到的：角色卡格式

# "永月"的核心数据结构：
class YongYue:
    # === 第1层：人格（角色卡） ===
    persona: CharacterCard  # 兼容 ST 格式

    # === 第2层：记忆 ===
    core_memory: dict       # 工作记忆（当前会话上下文）
    profiles: list[Profile] # 用户画像（Memobase模式）
    long_term: ChromaDB     # 长期记忆（向量检索）

    # === 第3层：交互 ===
    tts: TTSEngine          # 语音合成
    stt: STTEngine          # 语音识别
    avatar: Live2DModel     # 可选：虚拟形象

    # === 引擎 ===
    llm: LLMClient          # LLM API / 本地模型
```

### 为什么值得从零造？

1. **Letta 是"过度设计"**：它是通用 Agent 平台，90% 的功能你的 AI 伴侣不需要
2. **Memobase 太薄**：只有用户画像，没有角色人格
3. **SillyTavern 是 JS**：你无法深度定制
4. **从零造 = 完全掌控**：每个字节都是你懂的 Python

### 从零造的"梯子"（渐进路线）

```
Phase 1: 终端对话 (2周)
├─ FastAPI server
├─ DeepSeek API 调用
├─ 基础角色 system prompt
└─ SQLite 存储对话历史

Phase 2: 记忆系统 (4周)
├─ 实现 Memobase 风格的 Profile 提取
├─ ChromaDB 向量库做长期记忆
├─ 记忆压缩（摘要生成）
└─ 记忆注入 prompt 的流水线

Phase 3: 人格系统 (2周)
├─ 兼容 ST 角色卡格式
├─ Example dialogs 注入
├─ 人格一致性校验
└─ 动态人格调整

Phase 4: 语音交互 (2周)
├─ edge-tts 文字转语音
├─ sherpa-onnx 语音转文字
└─ WebSocket 实时对话

Phase 5: 前端 (渐进)
├─ Gradio Web UI (最快)
├─ 或 Streamlit
└─ 或 Svelte 前端（需学 JS）
```

### 成本估算

| 项目 | 初始投入 | 月费 |
|------|----------|------|
| DeepSeek API | ¥0 | ¥10-50 |
| ChromaDB（本地） | ¥0 | ¥0 |
| edge-tts | ¥0 | ¥0 |
| 服务器（本地PC） | ¥0 | ¥0 |
| **合计** | **¥0** | **¥10-50/月** |

### 优势
- ✅ 每个字节都是 Python 且你懂
- ✅ 完全契合"永月"的需求（不过度设计）
- ✅ 学习价值最大（从中学到 FastAPI/向量库/记忆系统/TTS 全栈）
- ✅ 天然可扩展
- ✅ 面试时可以拿出来作为作品

### 劣势
- ❌ 时间最长（6-12 个月）
- ❌ 初期没有 UI（终端/命令行对话）
- ❌ 需要持续投入
- ❌ 6 个月内不能用

### 学习曲线
```
Month 1-2: FastAPI + SQLite + ChromaDB 基础
Month 3-4: 记忆系统（Profile提取 + 向量检索 + 摘要）
Month 5-6: 人格系统 + TTS/STT
Month 7-9: 优化打磨
Month 10+: 可选前端
```

**推荐指数：⭐⭐⭐⭐⭐ 终极目标，但不是现在**

---

## 三套方案的路径建议

```
现在 ──方案A──▶ 1周原型 ──方案A+B──▶ 1个月MVP ──方案C──▶ 6-12月完整版
                   │                        │
                   ▼                        ▼
             验证可行性                 积累技术能力
             理解记忆系统              面试作品
             低成本试错               完全自主
```

### 我的推荐：A → C 的渐进路线

1. **现在**：用方案A跑通原型（1周），验证"AI有记忆的对话"是什么体验
2. **1个月内**：在方案A基础上，把 Memobase 换成自己手写的简化版（学习方案C的第一步）
3. **3个月内**：把 SillyTavern 前端换成 Gradio Web UI（Python 全栈）
4. **6个月内**：完成方案C的核心——记忆系统 + 人格引擎
5. **12个月内**："永月"完整版

---

## 为什么不推荐直接上方案B？

Letta 的问题不是它不好——它太好了，好到复杂。对于你的目标：
- 你需要的只是它的 10%（Core Memory + Archival）
- 但你要理解另外 90% 才能用好那 10%
- 而且它的架构是为"AI Agent 平台"设计的，不是为"AI 伴侣"设计的

**类比**：
- 方案A = 买乐高套装拼个城堡（快速但有边框）
- 方案B = 改造一个真的城堡做酒店（宏伟但要懂建筑学）
- 方案C = 自己画设计图、烧砖、盖城堡（最慢但最自由）

---

*下一篇：`04_memory_systems_comparison.md` — 记忆架构专项对比*
