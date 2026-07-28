---
name: Token认证 / JWT
type: procedure
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-后端工程
---

# Token认证 / JWT

## 类型判定
过程型 — 「登录→发通行证→每次请求出示→验证放行」的身份认证流水线。

## 类比 ★
### 一句话比喻
JWT 像游乐园的手环——你买票时园方给你戴上手环（登录→签发 Token），之后玩每个项目（每个 API 请求）工作人员看一眼手环就放行，不用每次都掏身份证查票。手环过期了就得重新买票。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 登录 → 签发 Token | 买票 → 戴手环——验证身份一次，发凭证 |
| 请求携带 Token（Authorization Header） | 玩项目前露手环——工作人员只看手环，不查身份证 |
| Token 过期 / 刷新 | 手环过了今天变色失效——需要重新买票或去服务台续期 |

## 是什么
Token 认证是无状态身份验证机制。流程：① 用户登录提供用户名密码 → ② 服务端验证成功，生成一个 Token（JWT 是含签名的 JSON）返回客户端 → ③ 客户端后续每个请求在 HTTP Header 中携带 `Authorization: Bearer <token>` → ④ 服务端验证签名和有效期，确认身份后放行。JWT（JSON Web Token）是最流行的 Token 实现，分 Header、Payload、Signature 三段。

## 输入-输出空间
- **输入**: 用户凭证（用户名+密码）、或 Refresh Token
- **输出**: Access Token（短期，通常 15-60 分钟）+ 可选 Refresh Token（长期，用于续期）
- **JWT 结构**: `Header.Payload.Signature` — Signature 用密钥签名，防止篡改

## 正例（≥2 个）
1. **AI 伴侣登录**: 用户输入密码 → FastAPI `/auth/login` 返回 JWT → 前端存 localStorage → 后续每次 `/chat` 请求带 Token
2. **API 鉴权中间件**: FastAPI 的 Depends 函数自动从 Header 提取 JWT → 验签 → 注入 `current_user` 到路由

## 反例/边界（≥1 个）
1. **Session 认证（Cookie + 服务端 Session）**: 传统方案，服务端存 Session，需要共享存储——JWT 无状态更适合微服务/分布式
2. **边界 — Token 无法主动失效**: JWT 签发后到过期前无法撤销（除非加黑名单存 Redis）——如果用户修改密码，旧 Token 仍有效

## 详细解释
JWT 的 Payload 示例：
```json
{
  "sub": "user_123",
  "name": "永月",
  "iat": 1700000000,
  "exp": 1700003600
}
```
`iat` 是签发时间，`exp` 是过期时间。

验证流程：
```
客户端                 服务端
  │  POST /auth/login    │
  │─────────────────────→│ 验证密码 → 生成 JWT
  │  ← {access_token}    │
  │                      │
  │  GET /chat           │
  │  Auth: Bearer xxx    │
  │─────────────────────→│ 验签 → 解析 user_id → 放行
  │  ← 聊天响应           │
```

在 AI 伴侣中，Token 认证保护所有 API 端点，确保只有用户本人能访问自己的对话历史、记忆和 AI 伴侣配置。

## 关系
### → 指向
- [[REST API]] — JWT 通过 REST API 的 Authorization Header 传递，是无状态 API 的标配
- [[Redis]] — Token 黑名单存 Redis 实现即时失效（修改密码后旧 Token 立刻作废）
- [[FastAPI]] — FastAPI 的依赖注入系统一行 Depends 即可完成 JWT 验证

### ← 被指向
- [[SQLAlchemy]] — 用户数据（密码哈希）存于 SQLAlchemy 管理的 users 表，登录时查询
