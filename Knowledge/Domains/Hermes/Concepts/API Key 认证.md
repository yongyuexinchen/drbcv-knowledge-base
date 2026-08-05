---
name: API Key 认证
type: discriminant
status: core
source: "[[Hermes教程-模块一-入门篇]]"
domain: hermes
---

# API Key 认证

## 类型判定
判别型 — 它是一组认证方案的分类体系，核心问题是「你是谁→你能用什么」。

## 是什么
API Key 认证是 LLM 服务验证调用者身份的主流方式。三种基本模式：(1) API Key —— 静态密钥串，放在 HTTP 请求头里；(2) OAuth / PKCE —— 通过浏览器登录获取临时 token；(3) 凭证池化 —— 多个 Key 组成池，自动轮转。

## 输入-输出空间
**输入**：身份凭证（Key / Token / 用户名密码）
**输出**：授权结果——通过（返回数据）或拒绝（HTTP 401/403）

## 正例（≥2个）
- Bearer Token（API Key 模式）：DeepSeek 用 `Authorization: Bearer sk-xxxx`，OpenAI 用 `Authorization: Bearer sk-xxx`
- 自定义 Header（API Key 模式）：硅基流动可用 `Authorization: Bearer sk-xxx`，也可接受 OpenAI 格式
- OAuth 2.1 PKCE：Nous Portal 不需要手动管理 Key——浏览器弹窗授权后自动获取 token，Hermes 缓存到 `auth.json`
- 凭证池化：配 3 个 DeepSeek Key → Hermes 自动轮转，余额不足的 Key 跳过

## 反例/边界（≥1个）
- API Key 写在代码里（硬编码）→ 提交到 GitHub 会被扫描工具检测并吊销
- 把 Key 值当成 `key_env` 环境变量名填进 config.yaml → `key_env` 是变量名（如 `OPENAI_API_KEY`），不是 Key 值本身
- IP 白名单限制 → Key 正确但 IP 不在白名单内，依然返回 403

## 详细解释
三种认证模式的对比：

| 模式 | 凭证形式 | 存储位置 | 适合场景 |
|------|---------|---------|---------|
| API Key | `sk-...` 字符串 | `.env` 文件 | 开发、中转站、个人项目 |
| OAuth/PKCE | 浏览器授权 → token | `auth.json` | 不想管 Key、企业 SSO |
| Key 池化 | 多个 API Key | `.env` 多个变量 | 高并发、避免单 Key 限流 |

**Bearer Token** 是 API Key 的 HTTP 传输方式：客户端在请求中带 `Authorization: Bearer <token>` 头，服务端解析验证。绝大多数 LLM API 都用这个格式。

**Key 安全原则**：永远放 `.env` 文件（不在代码仓库内），用环境变量读取，定期轮换。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| OAuth PKCE 流程 | 浏览器弹窗 → 用户授权 → 回调 code → 换取 token → 缓存到 auth.json |
| Credential Pool 轮转 | 多个 Key 组池 → 401/403/余额不足 → 标记 exhausted → 跳过 |
| Bitwarden 集成 | hermes secrets bitwarden → Key 从密码管理器读取 |

### 安全原则
- Key 永远放 .env（不入 git），不要写在 config.yaml 里
- key_env 是环境变量名（如 OPENAI_API_KEY），不是 Key 值本身——新手最高频错误
- 定期轮换：中转站 Key 通常 1-3 个月过期


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 属于 (is-a)
- [[Provider（模型提供商）]] — 认证是 Provider 配置的一部分

### 依赖 (depends-on)
- [[Base URL + Endpoint]] — 认证信息随每个 HTTP 请求发送到 API 端点

### ← 被指向
- [[Custom Provider（自定义提供商）]] (depends-on) — 中转站的接入需要配置 `key_env`
- [[Gateway（消息网关）]] (depends-on) — Gateway 的多平台接入需要各自的 Token 认证