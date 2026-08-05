---
name: Custom Models（自定义模型）
type: concept
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: grok-build
---

# Custom Models（自定义模型）

## 类型判定
概念型 — Custom Models 是 Grok Build 的模型后端替换机制，**这是让 Grok 零成本运行的关键**。

## 是什么
Grok 支持三种 API 后端（OpenAI Chat Completions / Responses / Anthropic Messages）。在 `~/.grok/config.toml` 配置 `[model.<name>]` 段即可接入任意 OpenAI 兼容端点。**开源的是 Agent 框架（"手"），模型推理（"脑"）可自由替换。**

## 输入-输出空间
- **输入**：TOML 配置（model ID + base_url + api_key + context_window）
- **输出**：Grok 的所有 LLM 调用走配置的端点

## 正例（≥2个）
1. **DeepSeek 官方**：`base_url = "https://api.deepseek.com/v1"`，国内直连，费用远低于 xAI
2. **硅基流动**：`base_url = "https://api.siliconflow.cn/v1"`（需余额充足）
3. **Ollama 本地**：`base_url = "http://localhost:11434/v1"`，完全离线零成本

## 反例/边界（≥1个）
- 自定义模型≠绕过 Grok 的 CLI 认证——首次仍需 OAuth（或 npm 安装后直接用 API Key）
- `context_window` 须手动设（不设默认 200K），设错导致过早 compaction
- API key 优先级：`api_key` 字段 > `env_key` 环境变量 > xAI session token > `XAI_API_KEY`

## 详细解释
推荐配置（DeepSeek 官方，已验证通过）：
```toml
[models]
default = "deepseek-v4"

[model.deepseek-v4]
model = "deepseek-chat"
base_url = "https://api.deepseek.com/v1"
name = "DeepSeek V4 (官方)"
api_key = "sk-..."
context_window = 128000
```

使用：`grok -m deepseek-v4 -p "任务" --yolo --output-format json`

## 细节备注

### 计费对比
| 后端 | 成本 | 国内可达 | 备注 |
|------|------|---------|------|
| xAI 内置 grok-build | 按 xAI 定价 | 需 VPN | 默认模型 |
| DeepSeek 官方 | ≈硅基 1/4 | 直连 ✓ | ★ 推荐 |
| 硅基流动 | 4x 加价 | 直连 ✓ | 当前欠费 |
| Ollama 本地 | 零 | 本机 ✓ | 需 GPU |

### 为什么 LLM 会幻觉自己的提供商
Grok 传给模型的 system prompt 不含 base_url。LLM 不知道自己在哪个 API 上跑。
当 Grok 问"你用的什么 API"，DeepSeek 模型可能回答"我在用 xAI"——**这是幻觉**，以 config 为准。

## 个人见解
> 我以前以为 Grok 只能用 xAI 的模型，现在发现它能用 DeepSeek、甚至本地 Ollama。这个灵活性让 Hermes 集成方案完全零额外成本。
>
> （填写你的理解）

## 关系
### 依赖 (depends-on)
- [[Grok Build Overview（Grok Build 总览）]] — 模型能力支撑所有功能

### ← 被指向
- [[Headless Mode（无头模式）]] — `-m` 旗标选模型
- [[Hermes-Grok Integration（Hermes-Grok 集成）]] — Adapter 默认使用 DeepSeek
