# AI 伴侣/角色扮演/记忆系统 — 开源项目全景扫描

> 评估日期：2026-07-27
> 评估者：vb-researcher
> 用户目标：本地优先、有独立人格的 AI 伴侣系统（"少女/永月"）
> 用户约束：Python+SQL 基础，代码薄弱，存款~25万，不需要训练基础模型

---

## 一、六个项目总览对比

| 项目 | 语言 | 类型 | 核心价值 | Star(约) | 最近更新 | 本地部署 | Python友好 |
|------|------|------|----------|----------|----------|----------|------------|
| **Memobase** | Python | 记忆后端 | 用户画像提取+管理 | ~800 | 活跃 | 服务端源码有 | ⭐⭐⭐⭐⭐ |
| **Letta/MemGPT** | Python | Agent+记忆 | 自主记忆管理+多Agent | ~14K | 非常活跃 | 完整 | ⭐⭐ |
| **SillyTavern** | Node.js | 角色扮演前端 | 角色卡片+对话管理 | ~8K | 非常活跃 | 极简单 | ❌(JS) |
| **KoboldAI** | Python+Lua | AI写作/推理 | 本地模型推理+互动小说 | ~3K | 中等 | 完整 | ⭐(旧架构) |
| **Open-LLM-VTuber** | Python | 虚拟角色+语音 | Live2D+语音交互+Letta集成 | ~4K | 非常活跃 | 完整 | ⭐⭐⭐ |
| **RisuAI** | TypeScript | 角色扮演前端 | 现代ST替代+浏览器LLM | ~1.5K | 活跃 | Web/Tauri | ❌(JS) |

---

## 二、逐项目深度评估

### 2.1 Memobase — "用户画像记忆库"

**一句话总结**：这就像是一个"AI的CRM系统"——它会自动从对话中提取关于你的事实，分类存档，下次对话时按相关性注入回 prompt。

#### 记忆架构
```
用户对话 → Blob(chat) → Memobase Server → LLM提取 → Profile(topic/sub_topic/content)
                                                              ↓
下次对话 ← context() ← 【选出最相关Profile】 ← [向量检索+标签过滤]
```

核心概念拆解（用 Python 初学者能理解的方式）：

```python
# Memobase 的数据模型就像这样：
# 1. Blob = 原始数据块（就像快递包裹）
class ChatBlob(Blob):
    messages: list[Message]  # 一轮对话 {role:"user"/"assistant", content:"..."}

# 2. 服务端处理 → 变成 Profile（就像从快递里提取出关键信息卡片）
# topic = "个人信息", sub_topic = "职业", content = "用户是大数据工程师"

# 3. 下次对话时，context() 检索相关 Profile 注入 prompt
# 就像一个秘书在开会前递给你"关于这个人的备忘条"
```

**关键发现**：
- 源码极简：客户端核心就 3 个依赖（pydantic, httpx, openai）
- 通过 monkey-patch OpenAI client 实现透明记忆注入（`openai_memory()` 函数给 client 挂了额外的钩子）
- 服务端有 `buffer`（缓冲区）→ `flush`（提交处理）→ `context`（检索）的完整流水线
- 支持 `event` 时间线检索 + `event_gist` 摘要 + tag 标签系统
- Profile 的 topic/sub_topic 结构非常适合组织"关于用户的事实"

#### 人格系统
- **不直接提供角色人格**。Memobase 的设计目标是"记住用户是谁"，不是"扮演某个角色"
- Profile extraction 用的是 LLM 从对话里提取用户特征
- 没有 character card、persona prompt 等机制

#### 部署成本
- **云服务为主**（api.memobase.dev），免费额度有限
- 服务端源码在 repo 中（`src/server/`），可以本地部署，但需要自己搭数据库和 LLM
- 客户端 3 个依赖 → pip install 就能用

#### 技术栈
- 语言：纯 Python 3.11+
- 框架：httpx（客户端）、FastAPI（服务端）
- 依赖：pydantic, httpx, openai（就这三个！）
- **Python 初学者友好度：⭐⭐⭐⭐⭐** — 代码量极少，概念清晰

#### 社区活跃度
- GitHub：memodb-io/memobase
- Star：~800（较新项目）
- 更新：活跃（2026年持续更新）
- 文档：有 tutorials 和 quickstart

#### 与用户目标匹配度
- ✅ 记忆管理思路好（profile 结构化提取）
- ✅ Python 源码极简，易学习
- ✅ Blob→Event→Profile 流水线可借鉴
- ❌ 不提供角色人格系统
- ❌ 云服务为主，本地部署需自己搭
- ❌ 只解决"记什么"，不解决"怎么像一个人"

---

### 2.2 Letta/MemGPT — "有记忆的AI Agent操作系统"

**一句话总结**：这就像给 AI 装了"大脑操作系统"——有工作记忆（Core Memory）、长期记忆（Archival Memory）、和自主记忆管理（Agent 自己决定记什么、忘什么、什么时候回忆）。

#### 记忆架构

Letta 的记忆分层（这可能是目前开源界最完整的记忆架构）：

```
┌─────────────────────────────────────────────┐
│             Context Window（上下文窗口）        │
│  ┌───────────────────────────────────────┐  │
│  │  Core Memory（核心记忆块）              │  │
│  │  ├─ human block: "关于用户的事实"        │  │
│  │  ├─ persona block: "Agent的人设"        │  │
│  │  └─ system/* blocks: 其他结构化信息      │  │
│  ├───────────────────────────────────────┤  │
│  │  Messages（当前对话）                    │  │
│  ├───────────────────────────────────────┤  │
│  │  Summary Memory（对话摘要压缩）          │  │
│  └───────────────────────────────────────┘  │
├─────────────────────────────────────────────┤
│  External Memory（外部记忆，不占上下文窗口）    │
│  ├─ Archival Memory: 向量检索的长期记忆        │
│  │   (就像"大脑的搜索引擎"，需要时才调用)      │
│  └─ Recall Memory: 历史对话的元数据索引        │
└─────────────────────────────────────────────┘
```

**关键代码解读**（从 `memory.py` 中提取）：

```python
# Letta 的 Core Memory 用 "Block" 概念组织——这就像大脑里的不同分区
class Memory:
    blocks: List[Block]       # 核心记忆块列表
    # 每个 Block 有：
    # - label: "human" / "persona" / "system/xxx"  ← 就像文件夹路径
    # - value: 实际存储的记忆文本
    # - limit: 字符上限（防止撑爆上下文窗口）
    # - description: 块的用途说明

    # 渲染到系统prompt时，变成这样的XML结构：
    # <memory_blocks>
    #   <human>
    #     <value>用户叫张三，喜欢猫，住北京...</value>
    #   </human>
    #   <persona>
    #     <value>你是永月，一个温柔但有时会毒舌的AI伴侣...</value>
    #   </persona>
    # </memory_blocks>

# git-backed memory（memFS）——这就像给记忆装了版本控制！
# 记忆块作为 Markdown 文件存在 git 仓库里
# agent 可以 git commit / git log 查看记忆的历史版本
# 这解决了"记忆被错误改写后无法恢复"的问题
```

**Agent 类型**（从 `agent.py` 的 AgentType 枚举）：
- `memgpt_agent`：原版 MemGPT，有 heartbeat 机制（Agent 在空闲时主动整理记忆）
- `letta_v1_agent`：简化版，去掉 heartbeat
- `voice_convo_agent`：语音对话专用
- `split_thread_agent`：多线程对话
- 还有 batch agent、workflow agent 等变体

#### 人格系统
- **Block-based persona**：persona 就是 Core Memory 里的一个 Block
- 支持多 Block 组成复杂人设（system/persona, system/rules, system/memories 等）
- git-backed 模式下，人设变更可追溯
- 但 persona 只是静态文本，**没有动态人格向量或情感模型**

#### 部署成本
- **完整本地部署**：PostgreSQL + Letta Server + LLM（Ollama/vLLM 均可）
- Docker Compose 一键启动
- 支持 20+ 种 LLM provider：openai, anthropic, deepseek, ollama, groq, vllm 等
- 免费开源，API 费用取决于你用的 LLM
- 最低硬件：取决于你跑的 LLM（7B 模型需要约 6GB VRAM）

#### 技术栈
- 语言：纯 Python
- 框架：FastAPI + SQLAlchemy + Alembic + WebSocket
- 依赖：非常重！Postgres, Redis, embedding service, 多种 LLM adapter
- **Python 初学者友好度：⭐⭐** — 代码量大，模块多，架构复杂

#### 社区活跃度
- GitHub：letta-ai/letta（原 cpacker/MemGPT）
- Star：~14K（非常热门）
- 更新：非常活跃（几乎每天有 commit）
- 有详细的文档、论文、社区 Discord

#### 与用户目标匹配度
- ✅ 最完整的开源记忆架构（Core + Archival + Recall 三层）
- ✅ 支持本地部署 + 任意 LLM
- ✅ persona block 直接对应"角色人格"
- ✅ git-backed memory 解决了记忆版本管理问题
- ✅ 被 Open-LLM-VTuber 集成为记忆后端
- ❌ 代码极其复杂（25MB源码），Python 初学者很难吃透
- ❌ 依赖重（Postgres + Redis + embedding 服务）
- ❌ 更多是"Agent 框架"而非"AI 伴侣框架"——过度设计

---

### 2.3 SillyTavern — "角色扮演前端之王"

**一句话总结**：这就像"AI角色扮演的Photoshop"——你在里面创建角色卡、写世界观、调参数，然后接上任何 LLM 后端就能聊。

> ℹ️ 用户已通过 DRBCV 知识库（45张卡片）深入了解 SillyTavern，此处只做技术评估。

#### 记忆架构
- **Character Card**：PNG 内嵌 JSON 的角色定义（description, personality, scenario, first_message, example_dialogs）
- **World Info / Lorebook**：关键词触发的世界观条目（类似"当提到 XX 时，注入 YY 信息"）
- **Author's Note**：固定注入的叙事指令
- **Chat History**：对话历史（仅当前会话，无跨会话长期记忆）
- **Summarization**：通过 LLM 压缩长对话为摘要
- **无向量数据库**：不支持语义检索的历史记忆

#### 人格系统
- Character Card 是业内标准格式，包含：
  - `description`：角色外貌+背景
  - `personality`：性格标签+行为模式
  - `scenario`：对话发生的背景场景
  - `first_message`：角色的开场白
  - `example_dialogs`：示例对话（影响最大！）
- 支持 **STscript**（自定义脚本语言）做高级自动化
- 通过 System Prompt 组装所有信息注入 LLM

#### 部署成本
- 极简：`npm install && npm start` 或 Docker
- 免费开源，本地 Web UI（localhost:8000）
- 需要外部 LLM API（OpenAI/Claude/Ollama 等）
- 纯前端，无后端存储

#### 技术栈
- 语言：Node.js（JavaScript）
- 框架：Express + WebSocket + jQuery + CSS
- 依赖：约 170 个 npm 包
- **Python 初学者友好度：❌** — 完全是 JavaScript 生态

#### 与用户目标匹配度
- ✅ 角色卡系统是行业标杆，可直接复用
- ✅ 用户已深入掌握（45 张 DRBCV 卡片）
- ✅ 社区活跃，插件丰富
- ❌ 纯前端，没有记忆后端
- ❌ JavaScript 技术栈，用户不熟悉
- ❌ 跨会话记忆靠 LLM 摘要，容易丢失关键信息

---

### 2.4 KoboldAI — "本地模型推理+互动小说引擎"

**一句话总结**：这就像"自己在家搭了个 AI 文字冒险游戏服务器"——加载本地模型，写故事，玩游戏。

#### 记忆架构
- **上下文窗口内记忆**：对话/故事在 context window 里延续
- **World Info**：类似 SillyTavern 的 Lorebook，关键词触发
- **软提示注入**：可在对话中插入隐藏指令
- **无长期记忆**：关掉会话就没了

#### 人格系统
- 角色定义通过 **Lua 脚本**（`cores/default.lua`）或场景文件
- `aiserver.py` 的主入口，10,364 行代码——**这是一个巨无霸单体文件**
- 主要服务于"AI 文字冒险"而非"AI 伴侣对话"
- 角色设定通过 prompt 工程实现，无结构化角色卡

#### 部署成本
- 需 GPU（模型本地推理），7B 模型约需 6GB VRAM
- 免费开源
- 安装：pip install + 下载模型

#### 技术栈
- 语言：Python + Lua
- 框架：Transformers (HuggingFace), eventlet, PyTorch, lupa (Lua→Python bridge)
- 架构：**单体式**——几乎所有逻辑在一个 10K 行文件里
- **Python 初学者友好度：⭐⭐** — 代码量大，使用 eventlet（非标准异步），Lua 混用

#### 与用户目标匹配度
- ✅ 本地推理能力强
- ✅ 有 World Info 和软提示机制
- ❌ 为 AI 文字冒险设计，不是 AI 伴侣
- ❌ 单体架构，10K 行代码难以维护和理解
- ❌ 长期记忆缺失
- ❌ 用户不熟悉 Lua

---

### 2.5 Open-LLM-VTuber — "会说话、有表情的虚拟角色"

**一句话总结**：这就像"给 AI 装了个虚拟身体"——它能听你说、说话回你、还有 Live2D 表情。

#### 记忆架构
- **本身不提供记忆系统**，但是——
- **依赖了 Letta！**（`letta-client>=0.1.100` 在 pyproject.toml 的依赖里）
- 这意味着它把记忆管理的活外包给了 Letta

#### 人格系统
- **YAML 角色配置**（`characters/zh_米粒.yaml`）：
  ```yaml
  character_config:
    conf_name: "米粒"
    persona_prompt: |
      你是米粒，一个女性AI聊天机器人。你聪明绝顶，过度自信...
  ```
- 支持 Live2D 模型绑定（角色有视觉形象）
- 人格定义较简单——就是一个 persona prompt

#### 关键能力
- **语音交互**：STT（语音转文字）→ LLM → TTS（文字转语音）
- **Live2D**：虚拟角色的面部表情和动作
- **语音打断**：支持在 AI 说话时打断
- **多平台**：Bilibili 直播、桌面独立运行
- **多 TTS 引擎**：sherpa-onnx（本地免费）、edge-tts（免费）、elevenlabs（付费高质量）

#### 部署成本
- 本地完整可运行
- 核心依赖：Python 3.10-3.12, torch, sherpa-onnx, FastAPI
- TTS 可纯本地（sherpa-onnx）→ 零 API 费用
- Live2D 需要模型文件（.moc3 等）
- GPU 可选（TTS 的 sherpa-onnx 需 CUDA 加速）

#### 技术栈
- 语言：纯 Python
- 框架：FastAPI + uvicorn + WebSocket
- 关键依赖：sherpa-onnx（TTS）, torch, openai/anthropic（LLM）, letta-client（记忆）
- **Python 初学者友好度：⭐⭐⭐** — Python 栈但依赖链长

#### 与用户目标匹配度
- ✅ 唯一集成了语音+视觉+记忆（Letta）的方案
- ✅ Python 全栈
- ✅ 纯本地 TTS（sherpa-onnx）零 API 费用
- ✅ Live2D 虚拟形象直接对应"永月"可视化
- ✅ 已集成 Letta → 天然获得记忆能力
- ❌ 角色人格系统较简单（只有 persona_prompt）
- ❌ Live2D 模型制作门槛高（需要 Live2D Cubism Editor，约 ¥200/年）
- ❌ 实时交互对硬件有要求

---

### 2.6 RisuAI — "现代版 SillyTavern"

**一句话总结**：这就像 SillyTavern 的现代化重写版——用上了 Svelte 5、Tailwind CSS，还能在浏览器里直接跑 LLM。

#### 记忆架构
- **Character Card**：使用 `@risuai/ccardlib`（自己的角色卡库），兼容 SillyTavern 格式
- **Lorebook / World Info**：类似 ST
- **Chat History**：当前会话
- **无向量数据库**：同 ST，没有语义检索的长记忆

#### 人格系统
- 兼容 SillyTavern 的角色卡格式（最大的优势）
- 更现代的 UI/UX（Svelte 5 + Tailwind，比 ST 的 jQuery 美观很多）
- 支持 Monaco Editor 编辑 prompt

#### 特殊能力
- **浏览器内 LLM 推理**：`@mlc-ai/web-llm`——在浏览器里用 WebGPU 跑小模型
- **Tauri 桌面应用**：可打包成独立桌面程序
- **Pyodide**：在浏览器里运行 Python（可加载 Python 数据处理脚本）
- **Ollama 集成**：直接连本地 Ollama

#### 部署成本
- 纯前端，Vite dev server 启动
- Docker 支持
- Tauri 可打包为桌面应用
- 免费开源

#### 技术栈
- 语言：TypeScript (Svelte 5)
- 框架：Vite + Tailwind + Svelte
- **Python 初学者友好度：❌** — 纯 TypeScript 生态

#### 与用户目标匹配度
- ✅ 现代 UI，比 ST 美观
- ✅ 兼容 ST 角色卡
- ✅ 浏览器 LLM（创新）
- ❌ JavaScript 生态
- ❌ 同样没有长期记忆后端

---

## 三、关键维度横评

### 3.1 记忆架构对比

| 项目 | 短期记忆 | 长期记忆 | 记忆提取 | 记忆检索 | 记忆压缩 |
|------|----------|----------|----------|----------|----------|
| Memobase | Chat Blob | Profile(topic/sub_topic) | LLM自动提取 | 向量+标签 | Event Gist |
| Letta | Core Memory Block | Archival Memory (向量) | Agent自主 | 向量+语义 | Summary Memory |
| SillyTavern | Chat History | ❌ | LLM摘要 | ❌ | 摘要压缩 |
| KoboldAI | Context Window | ❌ | ❌ | ❌ | ❌ |
| Open-LLM-VTuber | 依赖Letta | 依赖Letta | 依赖Letta | 依赖Letta | 依赖Letta |
| RisuAI | Chat History | ❌ | LLM摘要 | ❌ | 摘要压缩 |

### 3.2 人格系统对比

| 项目 | 人格定义方式 | 一致性保障 | 动态人格 |
|------|-------------|-----------|---------|
| Memobase | ❌（只有用户画像） | ❌ | ❌ |
| Letta | Persona Block（文本） | Core Memory持久化 | Agent可自改写 |
| SillyTavern | Character Card（结构化JSON） | System Prompt固定注入 | ❌（静态） |
| KoboldAI | Lua脚本/Prompt | 上下文窗口 | ❌ |
| Open-LLM-VTuber | YAML persona_prompt | 依赖Letta | 依赖Letta |
| RisuAI | Character Card（兼容ST） | System Prompt | ❌ |

### 3.3 部署成本横评

| 项目 | 最低硬件 | 必须外部API | 月费估算 | 一键本地 |
|------|----------|-------------|----------|---------|
| Memobase | 任意 | 云服务或自建 | $0-50 | ❌（需自搭） |
| Letta | 8GB RAM+GPU | 可选（可用Ollama） | $0-20 | ✅ Docker |
| SillyTavern | 任意 | 是（LLM API） | $0-30 | ✅ |
| KoboldAI | GPU 6GB+ VRAM | 否 | $0 | ✅ |
| Open-LLM-VTuber | GPU 4GB+ VRAM | 可选 | $0 | ✅ pip |
| RisuAI | 任意 | 是（LLM API） | $0-30 | ✅ npm |

### 3.4 Python 初学者友好度排名

1. ⭐⭐⭐⭐⭐ **Memobase** — 3个依赖，代码量极少
2. ⭐⭐⭐ **Open-LLM-VTuber** — Python 全栈但依赖多
3. ⭐⭐ **Letta** — Python 但架构极复杂
4. ⭐⭐ **KoboldAI** — Python 但单体10K行+混Lua
5. ❌ SillyTavern — JavaScript
6. ❌ RisuAI — TypeScript

---

## 四、对"永月"项目的核心启示

### 记忆系统设计启示
从 Memobase 学：用户画像应该结构化提取（不是简单摘要）
从 Letta 学：记忆要分层——核心记忆常驻、长期记忆按需检索
从 SillyTavern 学：角色卡格式已成为事实标准

### 人格系统设计启示
从 Letta 学：人设可以是一个"Block"，Agent 可以慢慢改写自己
从 SillyTavern 学：example_dialogs 比 description 更影响对话风格
从 Open-LLM-VTuber 学：视觉形象+语音让人格"有了身体"

### 技术栈选择启示
- Python 后端（用户主语言）→ Memobase 的简洁风格最适合学习
- 记忆层应与对话层解耦 → Letta 的三层架构思路是对的
- 前端不一定要 Python → 用成熟前端（ST/RisuAI）比自己写更实际

---

*下一篇：`02_architecture_deepdive.md` — Letta + Memobase 深度架构分析*
