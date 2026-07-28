---
name: Grok Build Overview（Grok Build 总览）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: grok-build
---

# Grok Build Overview（Grok Build 总览）

## 类型判定
系统型 — Grok Build 是 xAI 开源的 Rust 编码 Agent，作为 Hermes 的"执行手"接入，负责文件操作、代码生成、终端执行。

## 是什么
Grok Build（CLI 名 `grok`）是 xAI（SpaceXAI）开源的终端 AI 编码代理。约 60 个 Rust crate，三种运行模式：交互 TUI、Headless 无头、ACP 嵌入。**对 Hermes 而言，它的角色是纯执行器——接任务、改代码、跑测试、回报结果。不参与规划，不维护记忆。**

## 输入-输出空间
- **输入**：自然语言任务 + 工作目录（git 仓库）+ 安全策略 + 模型选择
- **输出**：文件改动 + 测试结果 + session_id + token 消耗（JSON 格式）

## 正例（≥2个）
1. **一次性脚本**：`grok -m deepseek-v4 -p "写 fibonacci.py" --yolo` → 创建文件 → 运行验证 → 返回 JSON
2. **多轮迭代**：`grok -p "修复 bug" --resume <session_id>` → 加载上下文 → 改代码 → 跑测试 → 成功
3. **只读审查**：`grok -p "审查代码" --tools "read_file,grep"` → 只读分析，不写文件

## 反例/边界（≥1个）
- Grok 不是聊天 AI——它是编码 Agent，核心价值是"改你的代码"
- Grok 开源≠免费——开源的是 Agent 框架（Rust CLI），模型推理另算（但可搭自定义端点避费）
- Grok 的 Agent Loop 有 max_turns 上限（默认无限制，可手动设 `--max-turns 30`）
- ❌ 不要开 Grok 内建记忆（`GROK_MEMORY=0`）——记忆主权归 Hermes

## 详细解释
Grok 的核心模块（~60 crates，三层布局）：
```
crates/codegen/
  ├── xai-grok-shell      ← Agent 运行时核心（goal 编排、session、subagent）
  ├── xai-grok-tools      ← 工具实现（terminal、文件编辑、搜索）
  ├── xai-grok-workspace  ← 文件系统、VCS、checkpoint
  ├── xai-grok-memory     ← 记忆系统（实验性，我们禁用它）
  ├── xai-grok-compaction ← 上下文压缩
  ├── xai-grok-mcp        ← MCP 客户端
  └── xai-grok-pager      ← TUI 界面（集成时不需要）

crates/common/
  ├── xai-tool-protocol   ← 进程外工具协议
  └── xai-tool-runtime    ← 工具分发

third_party/              ← Mermaid 图表渲染
```

## 细节备注

### 三种运行模式
| 模式 | 命令 | 用途 |
|------|------|------|
| 交互 TUI | `grok` | 开发者手动使用 |
| Headless | `grok -p "..." --output-format json` | ★ Hermes 集成面 |
| ACP 嵌入 | stdio JSON-RPC | v1.0 长期方向 |

### 安装（Windows 中国）
```bash
npm install -g @xai-official/grok   # 绕过 x.ai 被墙
```
配置 `~/.grok/config.toml` 指向 DeepSeek 官方 API，零 xAI 成本。

## 个人见解
> 我之前以为 Grok 是个"开源版 ChatGPT"，实际它是编码 Agent——专门改文件的。和 Hermes 配合才能发挥完整价值。
>干脆让他做hermes执行层算了，hermes写代码也许不太行，做规划大脑还是可以的

## 关系
### 依赖 (depends-on)
- [[Goal Orchestration（目标编排）]] — Grok 内部的 Agent Loop
- [[Tool Calling（工具调用）]] — 文件操作、终端执行的实现

### ← 被指向
- [[Hermes-Grok Integration（Hermes-Grok 集成）]] — Hermes 通过 Adapter 调用 Grok
