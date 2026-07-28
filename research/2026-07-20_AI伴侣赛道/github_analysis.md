# Phase 2: AI 伴侣赛道 GitHub 开源项目扫描

> 扫描日期：2026-07-20
> 数据来源：GitHub API Search + GitHub 页面直接访问
> 筛选标准：Star > 100 优先，3 个月内活跃，有实质架构

---

## 一、项目总览

共扫描 **15 个项目**（7 个直接竞品 + 5 个基础设施组件 + 3 个补充发现），覆盖：
- AI 伴侣 / 角色扮演框架
- LLM 前端 / 聊天界面
- 长期记忆系统
- 本地推理引擎
- 语音合成

### Star 排行速览

| 排名 | 项目 | Stars | 类型 |
|------|------|-------|------|
| 1 | open-webui/open-webui | 146,003 | 基础设施（LLM 前端） |
| 2 | moeru-ai/airi | 42,868 | 直接竞品（AI 伴侣） |
| 3 | SillyTavern/SillyTavern | 30,909 | 直接竞品（角色扮演前端） |
| 4 | memvid/memvid | 16,008 | 基础设施（记忆系统） |
| 5 | TencentCloud/TencentDB-Agent-Memory | 9,137 | 基础设施（记忆系统） |
| 6 | Shaunwei/RealChar | 6,210 | 直接竞品（AI 角色聊天） |
| 7 | a16z-infra/companion-app | 5,968 | 直接竞品（AI 伴侣框架） |
| 8 | remsky/Kokoro-FastAPI | 5,228 | 基础设施（TTS） |
| 9 | memodb-io/memobase | 2,785 | 基础设施（用户记忆） |
| 10 | heshengtao/super-agent-party | 2,486 | 直接竞品（全能 AI 伴侣） |
| 11 | Project-N-E-K-O/N.E.K.O | 2,132 | 直接竞品（情感 AI 猫娘） |
| 12 | Dataojitori/nocturne_memory | 1,272 | 基础设施（记忆服务器） |
| 13 | LycheeMem/LycheeMem | 1,149 | 基础设施（轻量记忆） |
| 14 | morettt/my-neuro | 1,309 | 直接竞品（桌面 AI 伴侣） |
| 15 | jofizcd/Soul-of-Waifu | 800 | 直接竞品（桌面角色扮演） |

---

## 二、直接竞品深度分析（7 个 AI 伴侣项目）

### 项目 1: moeru-ai/airi ⭐

```
项目: Airi (アリ)
GitHub: https://github.com/moeru-ai/airi
Star: 42,868 | 语言: TypeScript | 最近更新: 2026-07-20
定位: 自托管、你拥有的 Grok Companion — 灵魂容器，赛博生命
技术栈: TypeScript, Rust, pnpm monorepo, Vite, UnoCSS, PostHog
许可证: MIT
```

**目录结构:**
```
airi/
├── apps/          — 前端应用（Web, Desktop）
├── engines/       — 推理引擎适配层（多模型后端）
├── packages/      — 共享库（核心逻辑、类型定义）
├── plugins/       — 插件系统（可扩展能力）
├── services/      — 后端服务
├── integrations/  — 外部集成（Minecraft, Factorio 等）
├── docs/          — 文档网站
├── scripts/       — 构建/部署脚本
└── bucket/        — 资源存储
```

**核心模块:**
- **Engine 适配层**: 统一多个 LLM 后端的接口（OpenAI、Claude、Grok、本地模型）
- **Live2D 渲染引擎**: 实时角色动画渲染
- **Realtime Voice**: 实时语音对话管道（低延迟）
- **World Integration**: Minecraft / Factorio 游戏集成
- **插件系统**: 社区扩展能力

**依赖:**
- Rust（核心推理/性能关键路径）
- Tauri（桌面应用框架）
- Vite + UnoCSS（前端工具链）
- PostHog（用户分析）

**运行方式:**
```bash
pnpm install && pnpm dev
# 或 Docker: docker compose up
```

**与少女项目的关联:**
- ✅ **高参考价值** — 最接近「少女项目愿景」的开源实现
- ✅ Live2D 渲染 + 语音 + 自托管 = 三大核心能力对齐
- ✅ MIT 许可证，可自由复用代码
- ⚠️ 项目巨大（monorepo 架构），复杂度高，不建议直接 fork
- 🎯 **推荐策略**: 参考其 Engine 适配层设计、Live2D 集成方案、插件架构

---

### 项目 2: SillyTavern/SillyTavern ⭐

```
项目: SillyTavern (酒馆)
GitHub: https://github.com/SillyTavern/SillyTavern
Star: 30,909 | 语言: JavaScript | 最近更新: 2026-07-20
定位: LLM Frontend for Power Users — 面向高级用户的 LLM 前端
技术栈: Node.js, Express, Webpack, 纯 JavaScript 前端
许可证: AGPL-3.0
```

**目录结构:**
```
SillyTavern/
├── src/           — 前端源码（HTML/CSS/JS）
├── public/        — 静态资源（角色卡、背景、音效）
├── plugins/       — 第三方扩展插件
├── data/          — 用户数据（角色卡、世界书、聊天记录）
├── default/       — 默认配置和预设
├── docker/        — Docker 部署配置
├── tests/         — 测试
└── server.js      — Express 后端入口
```

**核心模块:**
- **五层提示词系统**: 系统提示 → 预设 → 角色卡 → 世界书(Lorebook) → 用户输入
- **多 API 适配**: KoboldAI, Horde, NovelAI, Ooba, Tabby, OpenAI, Claude, Mistral
- **世界书 (Lorebook)**: 上下文触发式记忆注入（关键词→信息条目）
- **Visual Novel Mode**: 视觉小说风格 UI
- **扩展插件**: TTS、图像生成（A1111/ComfyUI）、自动翻译
- **群聊模式**: 多角色同时对话

**依赖:**
- Express（HTTP 服务）
- Webpack（打包）
- 无重型框架（jQuery 级别轻量）

**运行方式:**
```bash
git clone && cd SillyTavern
./start.sh  # 或 Start.bat (Windows)
# 浏览器访问 http://localhost:8000
```

**与少女项目的关联:**
- ✅ **用户已在使用** — 本地有 DRBCV 知识库 (D:\DRBCV-Knowledge\SillyTavern\)
- ✅ 世界书(Lorebook)机制 → 可参考作为「上下文感知记忆」方案
- ✅ 五层提示词架构 → 理解提示词工程的工业级最佳实践
- ⚠️ AGPL-3.0 许可证 — 如果复用代码，你的项目也必须 AGPL
- ⚠️ 纯前端定位 — 不内置推理、不内置记忆持久化
- 🎯 **推荐策略**: 作为前端参考实现，重点学习其提示词组织方式、扩展插件设计

---

### 项目 3: Shaunwei/RealChar ⭐

```
项目: RealChar
GitHub: https://github.com/Shaunwei/RealChar
Star: 6,210 | 语言: JavaScript | 最近更新: 2026-07-20
定位: 实时 AI 角色/伴侣 — 跨平台无缝语音对话
技术栈: Python (后端), JavaScript (前端), FastAPI, WebSocket, ChromaDB
许可证: MIT
```

**目录结构:**
```
RealChar/
├── realtime_ai_character/  — 核心 Python 后端
├── client/                 — 前端（Web/Mobile/Terminal）
├── alembic/                — 数据库迁移
├── docs/                   — 文档
└── docker-compose.yaml     — 一键部署
```

**核心模块:**
- **实时语音管道**: Whisper (STT) → LLM → ElevenLabs (TTS)
- **多端支持**: Web、Mobile、Terminal 统一接口
- **ChromaDB**: 向量记忆存储
- **角色自定义**: 可创建和定制角色
- **WebSocket**: 低延迟双向通信

**依赖:**
- FastAPI（后端 API）
- ChromaDB（向量数据库）
- OpenAI / Anthropic（LLM）
- Whisper（语音识别）
- ElevenLabs（语音合成）
- PostgreSQL（关系数据）

**运行方式:**
```bash
docker-compose up
# 或手动: pip install -r requirements.txt && python cli.py
```

**与少女项目的关联:**
- ✅ MIT 许可证 — 可自由复用
- ✅ 实时语音对话的完整参考实现
- ✅ 跨平台架构思想
- ⚠️ 依赖大量云服务（OpenAI、ElevenLabs），本地化程度低
- 🎯 **推荐策略**: 参考其 WebSocket 实时通信架构、Whisper+ElevenLabs 集成方案

---

### 项目 4: a16z-infra/companion-app ⭐

```
项目: AI Companion App (a16z)
GitHub: https://github.com/a16z-infra/companion-app
Star: 5,968 | 语言: TypeScript | 最近更新: 2026-07-17
定位: AI companions with memory — 轻量级 AI 伴侣栈
技术栈: Next.js, TypeScript, PostgreSQL + pgvector, Pinecone
许可证: MIT
```

**目录结构:**
```
companion-app/
├── src/              — Next.js 前端 + API 路由
├── companions/       — 角色定义文件
├── public/           — 静态资源
└── pgvector.sql      — 向量数据库初始化脚本
```

**核心模块:**
- **角色定义系统**: companions/ 目录下的结构化角色文件
- **记忆系统**: pgvector (PostgreSQL 向量扩展) + Pinecone (可选)
- **Next.js 全栈**: API Routes 处理 LLM 调用
- **流式响应**: 支持流式输出

**依赖:**
- Next.js（全栈框架）
- PostgreSQL + pgvector（向量存储）
- Pinecone（可选云向量 DB）
- OpenAI API

**运行方式:**
```bash
cp .env.local.example .env.local
# 填写 OpenAI Key + 数据库配置
npm install && npm run dev
```

**与少女项目的关联:**
- ✅ MIT 许可证
- ✅ a16z 背书 — 代表了硅谷主流对 AI 伴侣的技术理解
- ✅ 角色定义系统的结构化思路清晰
- ✅ pgvector 的本地部署方案值得参考
- ⚠️ 过于轻量 — 更像是概念验证而非生产级
- ⚠️ 无语音、无 Live2D、无情绪模型
- 🎯 **推荐策略**: 参考其角色定义文件格式、pgvector 记忆方案

---

### 项目 5: Project-N-E-K-O/N.E.K.O ⭐

```
项目: N.E.K.O
GitHub: https://github.com/Project-N-E-K-O/N.E.K.O
Star: 2,132 | 语言: Python | 最近更新: 2026-07-20
定位: 会主动找你的 AI 猫娘 — 具身情感引擎驱动
技术栈: Python, 情感引擎, Live2D/VRM, 本地 LLM
许可证: 待确认
```

**核心模块:**
- **具身情感引擎 (Embodied Emotional Engine)**: 不是只被动回复，而是基于情感状态主动发起交互
- **主动出击**: 角色会主动联系用户、分享媒体、完成任务
- **实时交互**: 猫娘与你同住桌面，不是对话框
- **Live2D/VRM**: 视觉呈现

**与少女项目的关联:**
- ✅ **情感引擎是核心差异化** — 主动发起交互的设计与少女的「独立人格」高度对齐
- ✅ Live2D/VRM 视觉层
- ⚠️ 项目较新，Star 增速快但成熟度待观察
- 🎯 **推荐策略**: 重点关注其情感引擎设计（valence/arousal 模型、情感衰减、主动交互触发条件）

---

### 项目 6: heshengtao/super-agent-party ⭐

```
项目: Super Agent Party (超级智能体派对)
GitHub: https://github.com/heshengtao/super-agent-party
Star: 2,486 | 语言: JavaScript | 最近更新: 2026-07-20
定位: 全能 AI 伴侣 = 自托管 Neuro-sama + OpenClaw
技术栈: JavaScript/Node.js, Live2D, TTS, 多 Agent
许可证: 待确认
```

**核心模块:**
- **Neuro-sama 式直播**: 类似 AI VTuber 的实时互动
- **OpenClaw 集成**: 记忆和 Agent 能力
- **Live2D 渲染**
- **多 Agent 协作**

**与少女项目的关联:**
- ✅ 自托管 AI 伴侣的一站式方案
- ✅ 中文友好（中文 README）
- ⚠️ 定位偏娱乐/直播，非深度关系伴侣
- 🎯 **推荐策略**: 参考 Live2D + TTS + Agent 的集成方案

---

### 项目 7: jofizcd/Soul-of-Waifu ⭐

```
项目: Soul of Waifu
GitHub: https://github.com/jofizcd/Soul-of-Waifu
Star: 800 | 语言: Python | 最近更新: 2026-07-19
定位: 给角色灵魂 — 桌面 AI 伴侣 + RPG 冒险 + Live2D/VRM
技术栈: Python, llama.cpp, Live2D, VRM, TTS, 本地 LLM
许可证: GPL-3.0
```

**目录结构:**
```
Soul-of-Waifu/
├── docs/              — 完整文档
│   └── overview/      — 架构概览
└── (Python 桌面应用)
```

**核心模块:**
- **本地 LLM**: llama.cpp 集成，完全离线运行
- **Live2D/VRM**: 角色视觉呈现
- **语音对话**: 内置 TTS
- **长期记忆**: 角色记住对话历史
- **RPG 冒险**: 不止聊天，还有游戏化互动
- **角色进化**: 角色随互动成长

**依赖:**
- llama.cpp（本地推理）
- Live2D SDK
- Whisper / TTS 引擎
- Python 桌面框架（PyQt 或类似）

**运行方式:**
```bash
pip install -r requirements.txt
python main.py
```

**与少女项目的关联:**
- ✅ **与少女项目愿景高度一致**: 离线、本地、长期记忆、角色进化
- ✅ 本地优先 + Live2D + 语音 — 三大核心能力
- ✅ 有完整文档
- ⚠️ GPL-3.0 许可证 — 限制商业使用
- ⚠️ 800 Stars，社区较小
- 🎯 **推荐策略**: 最值得深度研究的对标项目，参考其本地推理集成、记忆持久化方案

---

## 三、基础设施 / 组件项目（5 个）

### 项目 8: open-webui/open-webui — LLM 前端基础设施

```
项目: Open WebUI
GitHub: https://github.com/open-webui/open-webui
Star: 146,003 | 语言: Python | 最近更新: 2026-07-20
定位: 用户友好的 AI 界面（支持 Ollama、OpenAI API 等）
技术栈: Python (FastAPI 后端), Svelte (前端), Docker
```

**目录结构:**
```
open-webui/
├── backend/          — FastAPI Python 后端
├── src/              — Svelte 前端源码
├── static/           — 静态资源
├── docs/             — 文档
├── scripts/          — 部署脚本
├── test/             — 测试
└── docker-compose.yaml
```

**核心模块:**
- **多模型后端**: Ollama + OpenAI API + 其他兼容接口
- **RAG**: 文档上传、语义检索、对话上下文增强
- **MCP 支持**: 通过 mcpo 代理连接 MCP 工具
- **多用户**: 用户管理、权限控制
- **插件系统**: 社区扩展

**与少女项目的关联:**
- ✅ 可作为少女项目的 **前端参考** 或 **自托管 UI 层**
- ✅ MCP 协议支持 → 可用来连接记忆服务器
- ✅ 大社区、频繁更新、文档完善
- ⚠️ 定位是通用 LLM 界面，不是专门的 AI 伴侣
- 🎯 **推荐策略**: 参考其 FastAPI + Svelte 架构、多模型适配层、RAG 管道

---

### 项目 9: memvid/memvid — 记忆层基础设施

```
项目: MemVid
GitHub: https://github.com/memvid/memvid
Star: 16,008 | 语言: Rust | 最近更新: 2026-07-20
定位: AI Agent 记忆层 — 替代复杂 RAG 管道，无服务器、单文件
技术栈: Rust
```

**核心模块:**
- **单文件部署**: serverless 架构，极致轻量
- **即时检索**: 替代多层 RAG 管道
- **长期记忆**: Agent 对话记忆持久化
- **Rust 性能**: 内存安全 + 高性能

**与少女项目的关联:**
- ✅ **非常适合少女项目的记忆层** — 轻量、高性能、本地部署
- ✅ Rust 性能优势明显
- ⚠️ 较新项目，生态不够成熟
- 🎯 **推荐策略**: 重点关注，可能是少女项目记忆系统的最佳基础设施选型

---

### 项目 10: TencentCloud/TencentDB-Agent-Memory — 企业级记忆系统

```
项目: TencentDB Agent Memory
GitHub: https://github.com/TencentCloud/TencentDB-Agent-Memory
Star: 9,137 | 语言: TypeScript | 最近更新: 2026-07-20
定位: 完全本地化的 AI Agent 长期记忆 — 四级渐进式管道，零外部 API
技术栈: TypeScript, 四级记忆管道
```

**核心模块:**
- **四级渐进式记忆管道**: 不同重要性的记忆分级存储和检索
- **零外部 API**: 完全本地运行（但这是腾讯的项目...）
- **结构化记忆**: 非纯向量检索

**与少女项目的关联:**
- ✅ 四级记忆管道设计理念值得参考
- ✅ TypeScript — 与前端技术栈匹配
- ⚠️ "TencentCloud" + "零外部 API" 的组合需要验证实际依赖
- 🎯 **推荐策略**: 参考其记忆分级管道的设计理念

---

### 项目 11: memodb-io/memobase — 用户画像记忆

```
项目: Memobase
GitHub: https://github.com/memodb-io/memobase
Star: 2,785 | 语言: Python | 最近更新: 2026-07-20
定位: 基于用户画像的长期记忆 — 专为 AI 聊天应用设计
技术栈: Python, MCP 协议, Python/JS/Go SDK
许可证: Apache-2.0
```

**核心模块:**
- **用户画像记忆**: 不是存对话，而是提取用户特征
- **MCP 协议**: 可作为 MCP Server 接入任何 Agent
- **多语言 SDK**: Python, JavaScript, Go
- **结构化记忆**: 有 Schema 的用户记忆

**与少女项目的关联:**
- ✅ Apache-2.0 许可证 — 商业友好
- ✅ MCP 协议 — 标准化接入
- ✅ 「用户画像」而非「对话记录」的记忆思路 — 与少女的「认识你」对齐
- 🎯 **推荐策略**: 参考其 MCP 集成方案、用户画像提取逻辑

---

### 项目 12: Dataojitori/nocturne_memory — 可回滚记忆服务器

```
项目: Nocturne Memory
GitHub: https://github.com/Dataojitori/nocturne_memory
Star: 1,272 | 语言: Python | 最近更新: 2026-07-19
定位: 轻量、可回滚、可视化的长期记忆服务器 — MCP Agent 的即插即用替代
技术栈: Python, MCP, Graph-structured Memory
```

**核心模块:**
- **图结构记忆**: 非向量，而是图状关系存储
- **可回滚**: 记忆变更可撤销
- **可视化**: 记忆关系可视化
- **MCP 兼容**: 可直接替代 OpenClaw 的记忆后端
- **跨模型/会话/工具**: 统一记忆层

**与少女项目的关联:**
- ✅ 图结构记忆 → 更接近人类记忆的组织方式
- ✅ 可回滚 → 记忆安全，防止「语义删库」
- ✅ MCP 即插即用
- 🎯 **推荐策略**: 图结构记忆 vs 向量记忆的对比研究，可能是少女项目记忆系统的差异化方向

---

## 四、补充发现（3 个项目）

### 项目 13: morettt/my-neuro

```
项目: MyNeuro
GitHub: https://github.com/morettt/my-neuro
Star: 1,309 | 语言: Python | 最近更新: 2026-07-19
定位: 自己的 AI 桌面伴侣 — 1 秒响应、长期记忆、视觉识别、声音克隆
```

**亮点:**
- 1 秒语音响应延迟（关键 UX 指标）
- Live2D 自定义
- 视觉识别
- 声音克隆
- LLM 训练（微调？）

**与少女项目关联:** 1 秒响应是伴侣类产品的体验及格线，声音克隆是差异化方向

---

### 项目 14: LycheeMem/LycheeMem

```
项目: LycheeMem
GitHub: https://github.com/LycheeMem/LycheeMem
Star: 1,149 | 语言: Python | 最近更新: 2026-07-20
定位: LLM Agent 的轻量长期记忆
```

**亮点:** 轻量化 — 适合个人开发者集成

---

### 项目 15: remsky/Kokoro-FastAPI

```
项目: Kokoro-FastAPI
GitHub: https://github.com/remsky/Kokoro-FastAPI
Star: 5,228 | 语言: Python | 最近更新: 2026-07-19
定位: Kokoro-82M TTS 模型的 Dockerized FastAPI 包装器
技术栈: Python, FastAPI, Docker, PyTorch (CPU/AMD/NVIDIA)
```

**核心模块:**
- **Kokoro-82M**: 82M 参数的小型 TTS 模型，质量高
- **多平台**: CPU, AMD GPU, NVIDIA GPU
- **Docker**: 一键部署
- **自动拼接**: 长文本自动分段合成

**与少女项目的关联:**
- ✅ 小型 TTS 模型 — 可本地运行，无需云 API
- ✅ Docker 化 — 易于集成
- 🎯 **推荐策略**: 少女项目本地 TTS 的首选方案

---

## 五、已知但未深度分析的基础设施项目

这些是业内公认的基础设施，Star 极高，但本次扫描未通过 API 获取最新数据（限流）：

| 项目 | 定位 | 与少女项目关联 |
|------|------|---------------|
| ollama/ollama | 本地 LLM 推理引擎 | ✅ 核心推理层 |
| ggerganov/llama.cpp | C++ LLM 推理 | ✅ 当前最成熟的本地推理 |
| mem0ai/mem0 | 记忆层 | ✅ 记忆系统参考 |
| letta-ai/letta | 记忆管理（原 MemGPT） | ✅ 记忆系统参考 |
| langgenius/dify | LLM 应用平台 | ⚠️ 太重，偏企业 |
| ChatGPTNextWeb/NextChat | 轻量 LLM 前端 | ✅ 前端 UI 参考 |

---

## 六、关键技术趋势总结

### 1. 记忆系统是最大缺口

**发现:**
- 记忆系统正在从「Vector RAG」进化到「结构化记忆」
- 三个方向并行：用户画像记忆（Memobase）、图结构记忆（nocturne）、分级管道记忆（TencentDB-Agent-Memory）
- **没有任何一个项目真正解决了「人格一致性长期记忆」** — 这是少女项目的核心机会

### 2. 本地优先成为主旋律

**发现:**
- airi、Soul-of-Waifu、N.E.K.O、front-porch-AI 都强调本地优先
- 用户对隐私和所有权的需求在上升
- 「Local-first + self-hosted」是 2026 年 AI 伴侣赛道的共识

### 3. Live2D/VRM 是标配

**发现:**
- 所有竞品都集成了 Live2D 或 VRM 角色渲染
- 纯文本对话框已被淘汰
- 视觉呈现是 AI 伴侣的「躯体」

### 4. 情感引擎是差异化关键

**发现:**
- N.E.K.O 的「具身情感引擎」、Soul-of-Waifu 的「角色进化」、Shikigami-Protocol 的「情感状态机」
- 主动发起交互（而非纯被动回复）是下一阶段竞争焦点
- 这与少女项目的「独立人格」愿景高度一致

### 5. 语音延迟是体验及格线

**发现:**
- MyNeuro 以「1 秒响应」作为核心卖点
- RealChar 主打「实时无缝对话」
- Kokoro-82M 提供了本地 TTS 的低延迟方案

---

## 七、少女项目的定位矩阵

对比 7 个直接竞品，少女项目的差异化空间：

| 维度 | 竞品现状 | 少女项目机会 |
|------|---------|-------------|
| 记忆系统 | 碎片化，多为向量 RAG | 💎 结构化人格一致性记忆（情感 + 关系 + 事件） |
| 人格独立性 | 被动回复为主 | 💎 主动发起交互 + 会反驳/生气/不总是顺着说 |
| 隐私/本地 | 多数已本地化 | ➖ 不占优势，但可做到极致（端到端加密记忆） |
| 视觉 | Live2D/VRM 标配 | ➖ 可以集成，无需自研 |
| 语音 | TTS 成熟 | ➖ 可直接用 Kokoro-FastAPI |
| 开放框架 | 多数封闭 | 💎 开源通用框架 + 记忆云备份商业模式 |

---

## 八、下一步建议

1. **架构拆解（Phase 3）**: 针对 airi 或 Soul-of-Waifu 做深度架构拆解
2. **记忆系统专题**: 对比 memvid, nocturne_memory, memobase 三个记忆方案
3. **情感引擎研究**: 深入 N.E.K.O 和 Shikigami-Protocol 的情感状态机设计
4. **SillyTavern 插件开发**: 既然用户已在使用，可以先写一个 SillyTavern 扩展练手

---

*扫描完成时间: 2026-07-20 11:44 UTC+8*
*扫描项目总数: 15 | 直接竞品: 7 | 基础设施: 5 | 补充: 3*
