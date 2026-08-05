---
name: Tool／Toolset（工具集）
type: system
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
---

# Tool／Toolset（工具集）

## 类型判定
系统型 — Toolset 是 Agent 能力边界的组织系统：决定 Agent 能做什么、不能做什么。

## 是什么
Tool（工具）是 Hermes 调用的单个能力——搜索网页、执行命令、读写文件。Toolset（工具集）是一组相关工具的集合，按平台按需启用/禁用。Agent 只能调用已启用 Toolset 中的工具。

## 输入-输出空间
**输入**：`hermes tools enable/disable <toolset>` 配置
**输出**：Agent 的 system prompt 中包含已启用工具的 JSON Schema 定义 → LLM 按 Schema 发出 tool_call → Hermes 路由到对应 handler

## 正例（≥2个）
- `terminal` + `file` toolset → Agent 可以执行命令 + 读写文件（编码必备）
- `web` toolset → Agent 可以 web_search + web_extract（调研必备）
- `delegation` toolset → Agent 可以 delegate_task 委派子任务
- Gateway 平台可以单独配置：微信 Agent 禁用 terminal，保留 web

## 反例/边界（≥1个）
- 禁用 terminal → Agent 不能执行命令，但可以通过 patch/write_file 编辑文件
- 子 Agent 的 toolset 受限：不能 clarify（不能和用户交互）、不能 memory（不写入持久记忆）、不能 delegation（叶子节点不允许继续委派）
- 某些工具需要 API Key 才能启用（如 check_seo 需要 OPENAI_API_KEY）→ 未配时工具不会出现在 schema 中

## 详细解释
主要 Toolset 分类：

| Toolset | 核心工具 | 用途 |
|---------|---------|------|
| terminal | terminal, process | shell 命令 + 进程管理 |
| file | read_file, patch, write_file, search_files | 文件操作 |
| web | web_search, web_extract | 网络搜索 + 内容提取 |
| browser | browser_navigate, browser_snapshot, browser_vision | 浏览器自动化 |
| delegation | delegate_task | 子 Agent 委派 |
| memory | memory, session_search | 持久记忆 + 会话搜索 |
| vision | vision_analyze | 图像理解 |
| cronjob | cronjob | 定时任务管理 |

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 并行执行 | 互不依赖的 tool_call 自动并行（最多 8 worker） |
| Smart Approvals | Agent 学习哪些命令你反复批准 → 逐步减少审批 |
| Post-Write Linting | v0.13+：写入后自动格式检查（Python/JSON/YAML/TOML） |
| 条件显示 | 需要 API Key 的工具未配时不出现 |

### 常用 toolset 速查
| Toolset | 核心工具 | 场景 |
|---------|---------|------|
| terminal | terminal, process | 编译/git/脚本 |
| file | read_file, patch, write_file | 代码编辑 |
| web | web_search, web_extract | 查资料 |
| browser | browser_navigate, browser_snapshot | 交互操作 |
| delegation | delegate_task | 并行子任务 |
| memory | memory, session_search | 记忆+历史 |


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — 工具在此循环中被调用

### ← 被指向
- [[Profile（多实例）]] (depends-on) — 每个 Profile 可以配置不同的 toolset
- [[Delegation（任务委派）]] (depends-on) — 子 Agent 的 toolset 受限
- [[Gateway（消息网关）]] (depends-on) — 不同平台可以启用/禁用不同 toolset