# Memobase / SillyTavern / Soul-of-Waifu 深度架构解构

> 产出日期: 2026-07-20
> 分析者: vb-architect
> 版本: v3.0 — 基于源码逐行阅读

---

## 目录

1. [Memobase — 用户记忆系统](#1-memobase)
2. [SillyTavern — 角色扮演前端](#2-sillytavern)
3. [Soul-of-Waifu — 桌面AI伴侣](#3-soul-of-waifu)
4. [交叉对比矩阵](#4-交叉对比矩阵)
5. [可独立提取的组件清单](#5-可独立提取的组件清单)
6. [设计模式精华](#6-设计模式精华)
7. [架构建议：companion-core MVP](#7-架构建议)

---

## 1. Memobase — 用户记忆系统

### 1.1 目录结构

```
src/
├── server/api/
│   ├── api.py                          # FastAPI 入口，路由注册
│   ├── config.yaml.example             # 全量配置模板
│   └── memobase_server/
│       ├── env.py                      # 配置加载 + 日志 + tiktoken
│       ├── connectors.py               # PostgreSQL + Redis 连接池
│       ├── struct_logger.py            # 结构化日志
│       ├── errors.py                   # 统一错误码
│       ├── utils.py                    # token 计算、字符串截断
│       ├── types.py                    # Pydantic 类型定义
│       ├── auth/                       # 鉴权（token + admin API）
│       ├── api_layer/                  # HTTP 路由处理函数（薄层，委托给 controller）
│       │   ├── user.py, profile.py, buffer.py
│       │   ├── blob.py, event.py, context.py
│       │   ├── roleplay.py, chore.py, project.py
│       │   └── middleware.py           # Auth 中间件
│       ├── controllers/                # 业务逻辑核心
│       │   ├── buffer.py               # 缓冲队列管理
│       │   ├── profile.py              # 用户画像 CRUD + Redis 缓存
│       │   ├── context.py              # 上下文组装（profile + event gist）
│       │   ├── event.py, event_gist.py # 事件存储 + 向量搜索
│       │   ├── blob.py                 # 原始 blob 存储
│       │   ├── project.py              # 项目/配置管理
│       │   ├── buffer_background.py    # 后台定时 flush
│       │   ├── full.py                 # 全量 profile 导出
│       │   └── modal/                  # *** 核心引擎：LLM 驱动的记忆处理 ***
│       │       ├── chat/               # 聊天处理管道
│       │       │   ├── __init__.py     # 主流程：summary → extract → merge → organize → re-summary
│       │       │   ├── entry_summary.py  # LLM: 聊天 → 结构化摘要
│       │       │   ├── extract.py      # LLM: 摘要 → 话题/子话题/事实
│       │       │   ├── merge_yolo.py   # LLM: 新旧 profile 合并去重
│       │       │   ├── organize.py     # LLM: profile 层级重组
│       │       │   ├── summary.py      # LLM: profile memo 过长时压缩
│       │       │   ├── event_summary.py# LLM: 事件标签
│       │       │   └── types.py        # 内部类型 + prompt 模板索引
│       │       ├── summary/            # 摘要类 blob 处理
│       │       └── roleplay/           # 角色扮演增强（兴趣检测、主动话题）
│       ├── models/                     # SQLAlchemy ORM
│       │   ├── database.py             # 表定义：Project, User, GeneralBlob, BufferZone, UserProfile, UserEvent, UserEventGist
│       │   ├── blob.py, action.py, claim.py
│       │   ├── response.py             # API 响应模型
│       │   └── utils.py                # Promise 单子
│       ├── prompts/                    # 多语言 prompt 模板
│       │   ├── chat_context_pack.py    # 上下文包装
│       │   ├── extract_profile.py      # profile 提取 prompt
│       │   ├── merge_profile*.py       # 合并 prompt
│       │   ├── summary_entry_chats.py  # 聊天总结 prompt
│       │   └── roleplay/
│       ├── llms/                       # LLM 调用抽象
│       │   ├── openai_model_llm.py     # OpenAI 兼容调用
│       │   ├── doubao_cache_llm.py     # 豆包缓存 LLM
│       │   └── embeddings/             # openai/jina/ollama/lmstudio
│       └── telemetry/                  # OpenTelemetry 追踪
├── client/                             # Python SDK（async/await）
│   ├── __init__.py                     # MemoBaseClient
│   └── tests/
└── mcp/                                # MCP Server 包装
```

### 1.2 核心模块职责矩阵

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| `api_layer` | HTTP 请求解析、参数验证、鉴权 | HTTP Request | 委托给 controller |
| `controllers/buffer` | 缓冲队列管理：插入、满检测、flush | Blob 数据 | 触发 modal 处理 |
| `controllers/profile` | 用户画像 CRUD + Redis 缓存 | Profile 数据 | 缓存刷新 |
| `controllers/context` | 上下文组装：profile + event gist | user_id, 参数 | 组装好的 context 字符串 |
| `modal/chat` | LLM 记忆处理管道（6 步骤） | 聊天 blobs | 增量 profile + event |
| `modal/chat/entry_summary` | 聊天 → 结构化事件描述 | 原始聊天 | 摘要字符串 |
| `modal/chat/extract` | 摘要 → 话题/子话题/事实 | 摘要 + 现有 profiles | FactResponse 列表 |
| `modal/chat/merge_yolo` | 新旧 profile 合并去重 | 新 facts + 旧 profiles | MergeAddResult |
| `modal/chat/organize` | profile 层级重组 | 所有 profiles | 优化后的列表 |
| `models/database` | ORM 表定义 + Schema 验证 | — | — |
| `llms` | LLM API 调用抽象层 | prompt + model | completion |

### 1.3 核心数据流（完整追踪）

```
┌─────────────────────────────────────────────────────────────────────┐
│  MEMOBASE 数据流：从聊天到记忆                                       │
│                                                                     │
│  ① INSERT BLOB                                                      │
│     POST /api/v1/blobs/insert/{user_id}                            │
│     ├─ 客户端写入 GeneralBlob (JSONB 列: blob_data)                 │
│     └─ 同步写入 BufferZone (状态=idle, token_size 已计算)           │
│                                                                     │
│  ② BUFFER FLUSH (触发条件二选一)                                    │
│     ├─ 主动触发: POST /api/v1/users/buffer/{user_id}/chat          │
│     └─ 自动触发: buffer token 总量 > max_chat_blob_buffer_token_size│
│                                                                     │
│  ③ FLUSH 执行 (controllers/buffer.py: flush_buffer_by_ids)         │
│     ├─ 状态机: idle → processing → done/failed                     │
│     ├─ JOIN BufferZone + GeneralBlob 取数据                         │
│     └─ 委托给 BLOBS_PROCESS[BlobType.chat] = modal/chat/process_blobs│
│                                                                     │
│  ④ MODAL CHAT PROCESSING (6 阶段 LLM 管道)                          │
│     ├─ Step 1: truncate_chat_blobs (token 预算截断)                 │
│     ├─ Step 2: entry_chat_summary (LLM: 聊天→事件摘要)              │
│     ├─ Step 3: extract_topics (LLM: 摘要→话题/子话题/memo)          │
│     ├─ Step 4: merge_or_valid_new_memos (LLM: 合并去重)             │
│     ├─ Step 5: organize_profiles (LLM: 层级重组)                    │
│     └─ Step 6: re_summary (LLM: 超长 memo 压缩)                     │
│                                                                     │
│  ⑤ 并行: profile 更新 + event 存储                                 │
│     ├─ add_update_delete_user_profiles → UserProfile 表             │
│     ├─ append_user_event → UserEvent 表 (+ embedding 向量)          │
│     └─ 清除 Redis profile 缓存                                      │
│                                                                     │
│  ⑥ CONTEXT ASSEMBLY (controllers/context.py)                       │
│     ├─ 并行获取: get_user_profiles + search_user_event_gists        │
│     ├─ profile_section: topic::sub_topic: memo 格式                 │
│     ├─ event_section: 最近的 event gist 内容                        │
│     ├─ token 预算: profile_event_ratio 控制分配                     │
│     └─ 输出: context_prompt(profile_section, event_section)         │
│                                                                     │
│  OUTPUT: 组装好的 context 字符串，可直接注入 LLM system prompt       │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.4 数据库 Schema

```
projects (project_id PK, project_secret, profile_config TEXT, status)
users (id UUID PK, project_id FK, additional_fields JSONB)
general_blobs (id UUID PK, user_id FK, blob_type, blob_data JSONB)
buffer_zones (id UUID PK, user_id FK, blob_id FK, blob_type, token_size, status)
user_profiles (id UUID PK, user_id FK, content TEXT, attributes JSONB {topic, sub_topic})
user_events (id UUID PK, user_id FK, event_data JSONB, embedding VECTOR)
user_event_gists (id UUID PK, event_id FK, gist_data JSONB, embedding VECTOR)
billings / project_billings
user_statuses
```

### 1.5 设计模式与"为什么这样设计"

**① Buffer + Flush 模式 → 为什么不用实时处理？**
- 解耦写路径（快）和处理路径（慢，需要 LLM 调用）
- 批量处理减少 LLM 调用次数（多个消息合并为一次 summarize）
- 容许高峰期积压，闲时处理
- 状态机（idle → processing → done/failed）保证幂等性

**② Promise 单子 → 为什么不用 Python 异常？**
- 显式的错误传播链（.ok() / .msg() / .data()）
- 避免 try/except 地狱
- 统一错误码（CODE 枚举）贯穿全栈
- 错误可以跨异步边界传递

**③ 三层记忆模型 → 为什么不是简单 KV？**
- Blob (原始) → Profile (结构化) → Event Gist (摘要+向量)
- 原始数据不丢（Blob），长期记忆可结构化（Profile），搜索靠向量（Event Gist）
- 每个层级有不同的保留策略和访问模式

**④ Config 驱动的 Prompt 模板 → 为什么？**
- 不同场景（companion/education/assistant）需要不同的 profile schema
- 通过 `additional_user_profiles` 配置话题槽位
- ProfileConfig 可 per-project 覆盖 Config

**⑤ Redis 缓存 + 主动失效 → 为什么？**
- 高频读取（每次上下文组装）需要缓存
- 写操作后主动删除缓存（refresh_user_profile_cache）
- TTL 兜底（20 分钟）防止内存泄漏

---

## 2. SillyTavern — 角色扮演前端

### 2.1 目录结构

```
src/
├── server-main.js          # Express 应用入口，中间件注册
├── server-init.js          # 服务器启动参数解析
├── server-startup.js       # HTTP/HTTPS 服务器启动 + 所有路由挂载
├── server-directory.js     # 服务器目录路径
├── server-events.js        # 事件总线（SERVER_STARTED 等）
├── util.js                 # 庞大工具函数集（1500+ 行）
├── users.js                # 多用户：目录隔离、Cookie Session、登录
├── transformers.js         # Transformers.js 本地模型（分类/嵌入/STT/TTS/字幕）
├── prompt-converters.js    # Prompt 模板格式转换
├── plugin-loader.js        # 插件系统：动态加载 plugins/ 目录
├── request-proxy.js        # HTTP 请求代理
├── private-request-filter.js # 内网请求安全过滤
├── fetch-patch.js          # 全局 fetch 补丁
├── jimp.js                 # 图片处理
├── character-card-parser.js # 角色卡解析（PNG + JSON）
├── validator/              # TavernCard v1/v2 验证
├── vectors/                # 向量嵌入多后端（OpenAI/Ollama/Cohere/Google/LlamaCpp）
├── middleware/              # Express 中间件
│   ├── whitelist.js, basicAuth.js, corsProxy.js
│   ├── webpack-serve.js, cacheBuster.js
│   ├── accessLogWriter.js, validateFileName.js
│   └── userCss.js, hostWhitelist.js
├── endpoints/              # REST API 路由处理函数（40+ 文件）
│   ├── chats.js            # 聊天 CRUD + 备份 + 导入导出
│   ├── characters.js       # 角色卡 CRUD + 磁盘缓存
│   ├── openai.js           # OpenAI/Claude/Gemini 代理
│   ├── backends/           # LLM 后端（chat-completions, text-completions, kobold, 等）
│   ├── settings.js, presets.js, themes.js
│   ├── groups.js           # 群聊
│   ├── worldinfo.js        # 世界信息/知识库
│   ├── vectors.js, tokenizers.js, classify.js
│   ├── speech.js, translate.js, caption.js
│   ├── stable-diffusion.js, images.js
│   ├── extensions.js, secrets.js, quick-replies.js
│   └── users-public.js, users-admin.js, users-private.js
└── tokenizers/             # 本地 tokenizer 模型文件
    ├── llama.model, mistral.model, claude.json, llama3.json, ...
```

### 2.2 核心模块职责矩阵

| 模块 | 职责 | 关键特性 |
|------|------|----------|
| `server-main.js` | Express 应用装配 | 中间件顺序：helmet → CORS → auth → session → CSRF → 静态 → API |
| `endpoints/chats.js` | 聊天文件读写 | JSONL 格式，每行一个消息对象，文件系统存储 |
| `endpoints/characters.js` | 角色卡管理 | PNG 隐写 JSON (v1/v2)，磁盘缓存 (node-persist)，内存 LRU |
| `endpoints/openai.js` | LLM API 代理 | 流式 SSE，请求/响应转换，多模型路由 |
| `prompt-converters.js` | Prompt 模板引擎 | 宏替换 ({{user}}/{{char}}/...)，格式转换 |
| `transformers.js` | 本地 AI 模型 | 情感分类/图像字幕/嵌入/STT/TTS，均跑在 WASM/ONNX |
| `users.js` | 多用户系统 | 目录级隔离，Cookie Session，迁移工具 |
| `plugin-loader.js` | 插件系统 | 动态 import，生命周期钩子 |

### 2.3 核心数据流

```
┌─────────────────────────────────────────────────────────────────────┐
│  SILLYTAVERN 数据流：从对话到响应                                    │
│                                                                     │
│  ① 角色卡加载                                                       │
│     └─ PNG 文件 → 解析嵌入 JSON (v2 spec/charx) → 内存缓存 + 磁盘缓存│
│                                                                     │
│  ② 聊天历史                                                         │
│     └─ data/<user>/chats/<char>/xxx.jsonl → 逐行 JSON 消息对象      │
│                                                                     │
│  ③ 消息发送 (POST /api/backends/chat-completions)                   │
│     ├─ 前端组装请求: messages (system + history + user)              │
│     ├─ 代理到 LLM API (OpenAI/Claude/Kobold/...)                    │
│     ├─ SSE 流式返回 → 前端渐进渲染                                   │
│     └─ 完成后追加到 JSONL 文件                                       │
│                                                                     │
│  ④ Prompt 构建 (前端 + 服务端)                                      │
│     ├─ 系统提示词模板（可配置 preset）                                │
│     ├─ 角色描述 + 性格 + 场景 + 首条消息                             │
│     ├─ 世界信息/知识库（触发式注入）                                  │
│     ├─ 聊天历史（受 context window 限制）                            │
│     └─ 宏替换：{{user}} → 用户名, {{char}} → 角色名                  │
│                                                                     │
│  ⑤ 扩展系统 (extensions/)                                           │
│     ├─ Summarize: 聊天历史 → 摘要 → 注入 prompt                      │
│     ├─ Vector Storage: 聊天 → 嵌入 → ChromaDB/Qdrant → 检索         │
│     ├─ Stable Diffusion: 场景生成                                    │
│     └─ TTS: 角色回复 → 语音合成                                      │
│                                                                     │
│  ⑥ 响应后处理                                                       │
│     ├─ TTS 朗读                                                      │
│     ├─ 角色表情（基于情感分类）                                       │
│     └─ 聊天备份（throttle 节流）                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.4 设计模式与"为什么这样设计"

**① 全文件系统存储 → 为什么不用数据库？**
- 部署极简：零依赖（不需要 PostgreSQL/Redis）
- 用户可直接编辑 JSON/JSONL 文件
- 备份 = 复制目录
- 牺牲了并发性能，换取了可维护性和可迁移性

**② PNG 隐写角色卡 → 为什么？**
- 社区互操作性标准（Character Card v2 spec）
- 一张图片包含所有角色信息，方便分享
- 不依赖中心化数据库

**③ 中间件链 + 插件系统 → 为什么？**
- 插件可在任意中间件位置注入
- 生命周期钩子：SERVER_STARTED, 路由注册, 退出清理
- 扩展可在不修改核心代码的情况下增加功能

**④ 多 LLM 后端统一代理 → 为什么？**
- OpenAI API 格式成为事实标准
- 每个后端只需实现 request→OpenAI-format 转换
- 前端代码完全不变

**⑤ 前端 SPA + Webpack 中间件 → 为什么？**
- 开发时热重载
- 生产构建优化
- 前后端一体部署
- 前端通过 `/api` 前缀区分 API 调用

---

## 3. Soul-of-Waifu — 桌面AI伴侣

### 3.1 目录结构

```
├── main.py                              # 应用入口：QApplication + MainWindow
├── start.bat, installer.bat             # Windows 启动/安装脚本
├── requirements.txt
├── app/
│   ├── configuration/
│   │   ├── configuration.py             # 配置管理（3 类：Settings/API/Characters）
│   │   ├── settings.json                # 主设置（JSON）
│   │   ├── api.json                     # API Token（JSON）
│   │   └── characters.json              # 角色数据（JSON，核心存储）
│   ├── gui/
│   │   ├── sowInterface.py             # Qt Designer 生成的 UI 类 (700+ 行)
│   │   ├── sowSystem.py                # 自定义 UI 系统（暗色主题、波形可视化、Live2D）
│   │   ├── interface_signals.py        # *** 信号中心（18000 行！）***
│   │   └── sow_system_signals.py       # SoW 系统模块（主动对话、自主行为）
│   ├── utils/
│   │   ├── ai_clients/
│   │   │   ├── openai_client.py        # OpenAI/OpenRouter 客户端（含 RAG 记忆）
│   │   │   ├── character_ai_client.py  # Character.AI 逆向
│   │   │   ├── mistral_ai_client.py    # Mistral API
│   │   │   └── local_ai_client.py      # LlamaCpp Python 本地 LLM
│   │   ├── text_to_speech.py           # TTS 多引擎（ElevenLabs/XTTSv2/EdgeTTS/Kokoro/Silero + RVC）
│   │   ├── speech_to_text.py           # STT (Whisper/SenseVoice)
│   │   ├── translator.py               # 翻译（Google/Yandex）
│   │   ├── character_cards.py          # 角色卡管理 + Soul Gateway 在线市场
│   │   ├── models_hub.py               # 模型下载中心
│   │   ├── ambient_client.py           # 环境音效
│   │   └── emotions/                   # Live2D/VRM 表情渲染
│   ├── translations/                   # 多语言 YAML（en/ru）
│   ├── font/, ffmpeg/, voices/
│   └── cache/, data/                   # 运行时数据
└── assets/
    ├── emotions/images/live2d/vrm/
    ├── backgrounds/, ambient/, rvc_models/
    └── local_llm/                     # 本地 LLM 模型存储
```

### 3.2 核心模块职责矩阵

| 模块 | 职责 | 技术栈 |
|------|------|--------|
| `main.py` | 应用入口，窗口创建，信号连接 | PyQt6 + qasync |
| `configuration/` | 三层 JSON 配置管理 | 纯 JSON 文件 |
| `interface_signals.py` | UI 事件处理中心（超大单体） | PyQt6 Signal/Slot |
| `sowSystem.py` | 自定义 UI 渲染（波形、Live2D OpenGL） | PyQt6 + Live2D SDK + OpenGL |
| `sow_system_signals.py` | 主动对话/自主行为模块 | 定时器 + LLM 调用 |
| `ai_clients/openai_client.py` | Prompt 构建 + RAG 记忆 | OpenAI + SentenceTransformer + cosine |
| `ai_clients/local_ai_client.py` | 本地 LLM 加载和推理 | llama-cpp-python |
| `text_to_speech.py` | TTS 管道（引擎 + RVC 变声） | EdgeTTS/Kokoro/XTTSv2 → RVC |
| `character_cards.py` | 角色创建/存储 + Soul Gateway | PyQt6 + 文件 I/O |

### 3.3 核心数据流

```
┌─────────────────────────────────────────────────────────────────────┐
│  SOUL-OF-WAIFU 数据流：从输入到响应                                  │
│                                                                     │
│  ① 角色创建                                                         │
│     └─ UI 表单 → ConfigurationCharacters.save_character_card()      │
│        → characters.json（嵌套 JSON：角色信息 + 聊天 + 配置）         │
│                                                                     │
│  ② 消息发送                                                         │
│     ├─ 用户输入 → 选择 AI Client（OpenAI/CharacterAI/Mistral/Local）  │
│     ├─ build_system_prompt() 构建完整 prompt                         │
│     │   ├─ System prompt (preset 模板)                               │
│     │   ├─ Character profile (角色描述+性格+场景)                     │
│     │   ├─ Lorebook (关键词触发)                                     │
│     │   ├─ Story Summary (自动摘要)                                  │
│     │   ├─ Persona (用户人设)                                        │
│     │   ├─ Author's Notes                                           │
│     │   ├─ Smart Memory (RAG: 旧消息→embedding→cosine→top3)         │
│     │   └─ Chat History (token 预算分配: 80%线性 + 20%RAG)           │
│     └─ LLM API 调用 → 流式响应 → 追加到 chat_content JSON             │
│                                                                     │
│  ③ Smart Memory (RAG—核心差异化功能)                                │
│     ├─ 超出上下文窗口的旧消息 → SentenceTransformer(all-MiniLM-L6)   │
│     ├─ 嵌入缓存 (embedding_cache dict, 按 message hash)              │
│     ├─ 查询向量: encode(last_bot_reply + user_message)               │
│     ├─ cosine_similarity → top-3 → 注入 [RECALLED MEMORIES] block    │
│     └─ 相似度阈值: 0.35，RAG 预算: 总 token 的 20%                   │
│                                                                     │
│  ④ Auto-Summarization                                                │
│     ├─ 每 N 条消息触发 (可配置 interval)                              │
│     ├─ chat_history → LLM → summary_text                             │
│     └─ 注入为 [Story Summary: {{summary}}]                           │
│                                                                     │
│  ⑤ SoW System (主动对话)                                            │
│     ├─ 定时器触发 (sow_system_signals.py)                             │
│     ├─ 后台 LLM 调用（独立线程）                                     │
│     └─ TTS 合成 + 自动播放 + Live2D 表情同步                          │
│                                                                     │
│  ⑥ TTS 管道                                                         │
│     └─ 文本 → TTS 引擎 (EdgeTTS/Kokoro/XTTSv2/ElevenLabs)            │
│            → RVC 变声 (可选) → AudioPlaybackWorker → 设备播放         │
│                                                                     │
│  ⑦ 角色渲染                                                         │
│     ├─ Live2D: OpenGL + Live2D SDK v3 → 动画表情                     │
│     ├─ VRM: QWebEngineView → Three.js VRM → 3D 模型                  │
│     └─ 静态表情: QPixmap → 基于情绪切换                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.4 设计模式与"为什么这样设计"

**① JSON 文件作为数据库 → 为什么？**
- 桌面应用，单用户，零部署
- 用户可直接编辑 characters.json 迁移角色
- 无需任何服务器基础设施
- 缺点：18000 行 interface_signals.py 暗示架构需要拆分

**② 本地 RAG 记忆 → 为什么选择 SentenceTransformer 而不是远程 API？**
- 隐私优先：所有数据留在本地
- 零网络依赖：离线可用
- all-MiniLM-L6-v2 (80MB) 轻量但效果足够
- 嵌入缓存避免重复计算

**③ TTS + RVC 管道 → 为什么是两阶段？**
- TTS 引擎负责自然语音合成
- RVC 负责声音特征迁移（变成角色的声音）
- 分离关注点：换一个角色只需换 RVC 模型

**④ 多个 AI Client 的 Strategy 模式 → 为什么？**
- OpenAI/CharacterAI/Mistral/Local — 不同用户不同需求
- 统一接口：`generate_response()` 或 `format_messages()`
- 切换后端无需改 UI 代码

**⑤ Signal/Slot 架构 → 为什么这么重？**
- PyQt6 原生范式，UI 事件驱动的必然选择
- 但 interface_signals.py 18000 行严重违反单一职责
- 应拆分为：ChatSignals, CharacterSignals, SettingsSignals 等

---

## 4. 交叉对比矩阵

### 4.1 架构维度对比

| 维度 | Memobase | SillyTavern | Soul-of-Waifu |
|------|----------|-------------|---------------|
| **语言/运行时** | Python / FastAPI | Node.js / Express | Python / PyQt6 |
| **部署模型** | 微服务 (API Server) | Web 服务 (SPA) | 桌面应用 |
| **存储** | PostgreSQL + Redis | 文件系统 (JSONL, PNG) | JSON 文件 |
| **多用户** | tenant 隔离 (project_id) | 目录隔离 (user dirs) | 单用户 |
| **记忆系统** | **核心功能**：三层记忆模型 | 依赖扩展 (Summarize + Vector Storage) | **自研 RAG**：本地 embedding |
| **LLM 集成** | OpenAI 兼容 (统一) | 40+ 后端适配器 | 4 个 Client (Strategy) |
| **Prompt 构建** | YAML 配置 + 自定义模板 | 宏系统 + Preset 模板 | 顺序模板 + Order 配置 |
| **向量存储** | pgvector (PostgreSQL) | 扩展 (ChromaDB/Qdrant) | 本地 NumPy (cosine) |
| **插件系统** | 无 | 完整插件系统 | 无 |
| **角色系统** | 无（专注记忆） | Character Card v2 | 自研 JSON 格式 |
| **TTS** | 无 | 扩展 | **核心功能**（5 引擎 + RVC） |
| **Avatar** | 无 | 静态图片 | **核心功能**（Live2D/VRM/静态） |
| **流式响应** | 无（异步处理） | SSE | SSE |
| **上下文窗口管理** | ratio 分配 (profile/event) | truncation (FIFO) | 80/20 分配 (线性/RAG) |
| **代码规模** | ~150 文件 (Python) | ~100 文件 (JS) | ~55 文件 (Python) |

### 4.2 共同模式

**① 三层上下文策略**

三个项目都意识到纯聊天历史不够，都在构建"系统提示词 + 结构化记忆 + 聊天历史"三层：

```
Memobase:       System Prompt + Profile(topic::sub_topic:memo) + Event Gist + Chat History
SillyTavern:    System Prompt + Character Card + World Info + Summary + Chat History
Soul-of-Waifu:  System Prompt + Character Profile + Lorebook + Summary + RAG Memory + Chat History
```

**② Chat → Summary → Structured Memory 管道**

Memobase 和 Soul-of-Waifu 都实现了类似的管道：
```
Chat Messages → LLM Summarize → Structured Extraction → Merge with Existing
```
Memobase 把这个管道做成了核心产品，Soul-of-Waifu 只实现了其中 auto-summarization 部分。

**③ Token 预算管理**

三个项目都有显式的 token 计数和截断逻辑。Memobase 使用 tiktoken，Soul-of-Waifu 也用了 tiktoken（本地缓存），SillyTavern 使用 tokenizer 模型文件。

**④ 配置驱动的 Prompt 模板**

都支持用户自定义系统提示词模板。Memobase 用 YAML config，SillyTavern 用 Preset JSON，Soul-of-Waifu 用 Preset JSON。

### 4.3 差异点与定位

| 项目 | 核心定位 | 最大优势 | 最大缺陷 |
|------|----------|----------|----------|
| **Memobase** | 记忆即服务 (MaaS) | 三层记忆模型成熟、多租户、生产级部署 | 无前端、无角色系统、只管记忆 |
| **SillyTavern** | 通用角色扮演平台 | 社区生态、插件系统、40+ 后端、跨平台 | 无内置记忆（靠扩展）、文件系统扩展性差 |
| **Soul-of-Waifu** | 本地桌面 AI 伴侣 | 全离线、RAG 记忆、Live2D/TTS 一体化 | 单用户、架构混乱 (18000 行文件)、缺少社区 |

---

## 5. 可独立提取的组件清单

### 5.1 从 Memobase 可提取

| 组件 | 描述 | 提取难度 | 依赖 |
|------|------|----------|------|
| **Buffer + Flush 管道** | 异步消息缓冲 → 批量处理 | ⭐⭐ 中 | PostgreSQL, SQLAlchemy |
| **Promise 单子** | models/utils.py:Promise | ⭐ 易 | 纯 Python，零依赖 |
| **Config → Profile Schema** | YAML 配置驱动的话题/子话题 Schema | ⭐ 易 | PyYAML |
| **Context Assembler** | profile + event gist 比例分配 | ⭐⭐ 中 | profile controller, event controller |
| **多语言 Prompt 模板系统** | 按语言 + 任务索引 prompt | ⭐ 易 | 纯字符串 |
| **LLM 调用抽象层** | embed + complete 的多后端适配 | ⭐ 易 | OpenAI, Jina, Ollama SDK |

### 5.2 从 SillyTavern 可提取

| 组件 | 描述 | 提取难度 | 依赖 |
|------|------|----------|------|
| **Character Card Parser** | PNG 隐写 JSON 的读写 | ⭐ 易 | Node.js Buffer, zlib |
| **Prompt Macro System** | {{user}}/{{char}} 替换引擎 | ⭐ 易 | 纯字符串替换 |
| **多 LLM 代理模式** | 统一 OpenAI 格式的前端代理 | ⭐⭐ 中 | Express, http-proxy |
| **插件系统架构** | 动态加载 + 生命周期钩子 | ⭐⭐⭐ 难 | 与 Express 深度耦合 |
| **用户目录隔离** | 多用户文件系统分区 | ⭐ 易 | Node.js fs |
| **聊天备份系统** | throttle 节流 + JSONL 轮转 | ⭐ 易 | lodash, write-file-atomic |

### 5.3 从 Soul-of-Waifu 可提取

| 组件 | 描述 | 提取难度 | 依赖 |
|------|------|----------|------|
| **本地 RAG 记忆引擎** | SentenceTransformer + cosine + 嵌入缓存 | ⭐⭐ 中 | SentenceTransformer, sklearn |
| **TTS + RVC 管道** | 多引擎合成 → 变声 → 播放 | ⭐⭐ 中 | PyAudio, RVC, TTS 引擎 |
| **Lorebook 触发系统** | 关键词+范围+延迟+冷却+概率 | ⭐⭐ 中 | 纯 Python |
| **Live2D 表情渲染** | OpenGL + Live2D SDK v3 | ⭐⭐⭐ 难 | Live2D SDK, OpenGL |
| **Auto-Summarization** | 定时触发 + LLM 摘要 + 注入 prompt | ⭐ 易 | 纯 Python |
| **Signal/Slot UI 架构** | 事件驱动的界面交互模式 | ⭐⭐ 中 | PyQt6 |

### 5.4 最有价值的前 5 个提取组件

1. **Memobase 三层记忆模型** — 最成熟、可直接作为后端服务
2. **Soul-of-Waifu 本地 RAG 记忆** — 轻量、离线、隐私友好
3. **SillyTavern 角色卡格式** — 社区标准、互操作性好
4. **Memobase Buffer + Flush 管道** — 异步批量处理模式
5. **Soul-of-Waifu TTS + RVC 管道** — 多引擎 + 变声，体验核心

---

## 6. 设计模式精华

### 6.1 Memobase 的 Pipeline 模式

```
Blob → Buffer → truncate → entry_summary → extract → merge → organize → re_summary → Profile DB
```

这是经典的 ETL 管道在 LLM 时代的应用。每一步都可以独立替换（换 prompt、换 LLM），管道顺序可调整（通过 config 控制哪些步骤启用）。

### 6.2 SillyTavern 的 Adapter 模式

```
40+ LLM Backends → OpenAI-compatible format → Frontend
```

所有后端适配为一个统一格式，前端完全不需要知道后端差异。这是教科书级的 Adapter 模式。

### 6.3 Soul-of-Waifu 的 Strategy 模式

```
4 AI Clients (OpenAI/CharacterAI/Mistral/Local) → 统一接口 → UI
```

类似的 Strategy 模式也用在 TTS（5 引擎）和 Translator（2 引擎）上。

### 6.4 共同的 Dependency Injection

三个项目都通过外部配置注入 LLM 参数，而不是硬编码。Memobase 用 `Config` dataclass + YAML + 环境变量，SillyTavern 用 `config.yaml` + `getConfigValue()`，Soul-of-Waifu 用 JSON + `ConfigurationSettings`。

### 6.5 三个项目都没做好的：Agentic Memory

- Memobase 有结构化的 profile，但不能让 LLM 主动查询记忆
- SillyTavern 靠扩展的向量检索，但无结构化
- Soul-of-Waifu 的 RAG 只看相似度，不理解语义关联

**机会点**：结构化记忆（Memobase）+ 向量检索（SillyTavern）+ 本地执行（Soul-of-Waifu）的结合。

---

## 7. 架构建议：companion-core MVP

基于三个项目的分析，推荐的 MVP 架构：

```
┌──────────────────────────────────────────────────────────┐
│                    companion-core                         │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Memory Core  │  │ Persona Core  │  │ Interaction    │  │
│  │ (Memobase)   │  │ (ST CharCard) │  │ (SoW TTS/RAG)  │  │
│  │              │  │               │  │                │  │
│  │ · Buffer     │  │ · Name/Desc   │  │ · TTS Pipeline │  │
│  │ · Extract    │  │ · Personality │  │ · RAG Memory   │  │
│  │ · Merge      │  │ · Scenario    │  │ · Avatar       │  │
│  │ · Context    │  │ · Lorebook    │  │ · Streaming    │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                 │                   │           │
│         └─────────┬───────┴───────────────────┘           │
│                   │                                       │
│           ┌───────▼────────┐                              │
│           │ Prompt Assembler│                             │
│           │ (persona +      │                             │
│           │  memory + chat) │                             │
│           └───────┬────────┘                              │
│                   │                                       │
│           ┌───────▼────────┐                              │
│           │ LLM Backend    │                              │
│           │ (Adapter模式)   │                              │
│           └────────────────┘                              │
└──────────────────────────────────────────────────────────┘
```

### 关键技术决策建议

| 决策 | 建议 | 理由 |
|------|------|------|
| 存储 | SQLite + pgvector 扩展 或 ChromaDB | 本地优先，零运维 |
| 语言 | Python | 三个项目中有两个是 Python，生态最好 |
| 记忆模型 | Memobase 三层模型 + SoW RAG | 结构化 + 语义检索双轨 |
| 角色格式 | SillyTavern CharCard v2 | 社区标准，可导入生态内容 |
| TTS | EdgeTTS (免费) + RVC | 低延迟，本地运行 |
| Prompt 模板 | Memobase Config 驱动 | 最灵活，支持 per-character 定制 |
| 交付形式 | 本地 Python 库 + FastAPI 可选 | 可嵌入桌面应用，也可独立服务 |

### 不要重复造的轮子

- **不要** 从头写 LLM 后端适配（SillyTavern 已有 40+ 个）
- **不要** 从头设计角色卡格式（CharCard v2 是社区标准）
- **不要** 用 JSON 文件当数据库（Memobase 的 SQL 方案更适合生产）
- **要** 借鉴 Memobase 的 Pipeline 模式处理记忆
- **要** 借鉴 Soul-of-Waifu 的本地 RAG 做离线优先
- **要** 借鉴 SillyTavern 的插件系统做可扩展性

---

*本文档基于对三个项目源码的逐文件阅读生成，共计阅读核心文件 25+ 个，覆盖三项目全部核心模块。*
