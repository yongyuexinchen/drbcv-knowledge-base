---
name: Custom Provider（自定义提供商）
type: connection
status: core
source: "[[Hermes教程-模块一-入门篇]]"
domain: hermes
---

# Custom Provider（自定义提供商）

## 类型判定
连接型 — 它连接 Hermes 和任何 OpenAI 兼容的中转站/自建 API，是突破厂商锁定的关键。

## 是什么
Custom Provider 是 Hermes 接入非内置提供商的机制。只需在 `config.yaml` 中配置三要素（`name`、`base_url`、`key_env`），任何 OpenAI 兼容的 API 端点都能成为 Hermes 的模型来源。

## 输入-输出空间
**输入**：`config.yaml` 中的 `custom_providers` 数组 + `model.provider: custom` + `model.base_url`
**输出**：Hermes 把该端点当作标准 Provider 使用——调用 `/v1/chat/completions`、处理响应、统计 token

## 正例（≥2个）
- 硅基流动接入：`base_url: https://api.siliconflow.cn/v1`，`key_env: SILICONFLOW_KEY`，调 DeepSeek/Qwen/GLM 全通
- 本地 vLLM/Ollama：`base_url: http://localhost:11434/v1`，`key_env: NONE`（本地无需 Key）
- 任何中转站：APIHub、猫头鹰等——只要兼容 `/v1/chat/completions` 就能用

## 反例/边界（≥1个）
- `provider: openai` 不行——Hermes 的 main-model resolver 不认这个值，**必须填 `provider: custom`**
- 忘了配 `custom_providers` 块 → 即使 `provider: custom`，resolver 也找不到凭证
- `key_env` 是环境变量名，不是 Key 值——把 Key 直接写进 `key_env` 字段是常见错误
- 中转站不兼容标准 endpoint → 需要自定义 `api_mode` 或放弃

## 详细解释
完整配置模板：
```yaml
model:
  default: anthropic/claude-fable-5
  provider: custom                    # ← 关键：必须是 "custom"
  base_url: https://your-relay.com/v1

custom_providers:
  - name: my-relay
    base_url: https://your-relay.com/v1
    key_env: RELAY_API_KEY           # 环境变量名
    default_model: anthropic/claude-fable-5  # 可选
    context_length: 200000           # 可选，覆盖上下文窗口
```

**为什么需要 custom_providers 块？** Hermes 的 provider resolver 靠它做两件事：(1) 找到匹配的 `base_url` 对应哪个凭证; (2) 应用该端点的特殊参数。没有这个块 = resolver 空手而归。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| context_length 覆盖 | custom_providers[].context_length: 200000 |
| api_mode | 默认 openai_chat；少数中转站需特殊模式 |
| default_model | 可不配——由 model.default 指定 |

### 配置坑点
- provider: openai 不行，必须 provider: custom
- 忘了配 custom_providers 块 → resolver 找不到凭证
- key_env 填了 Key 值而不是变量名
- base_url 带了 /chat/completions 后缀 → 双拼路径

### Gateway 重启限制
hermes gateway restart 从内部调用被拒绝（不能自己杀自己）


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 属于 (is-a)
- [[Provider（模型提供商）]] — Custom Provider 是一种 Provider

### 依赖 (depends-on)
- [[Base URL + Endpoint]] — 通过自定义 base_url 寻址
- [[API Key 认证]] — 通过 key_env 获取凭证
- [[OpenAI 兼容 API]] — 要求端点兼容此协议

### ← 被指向
- [[中转站／API 代理]] (implements) — 中转站通过 Custom Provider 接入 Hermes