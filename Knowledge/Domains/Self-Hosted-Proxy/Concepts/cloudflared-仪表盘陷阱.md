---
name: cloudflared-仪表盘陷阱
type: discriminant
status: core
source: "[[自建代理实操经历]]"
domain: Self-Hosted-Proxy
---

# cloudflared 仪表盘管理模式陷阱

## 类型判定
判别 — `cloudflared tunnel run --token` 从 Cloudflare API 拉取远程配置，本地 config.yml 的 `tcp://` 或 `ssh://` ingress 被忽略。所有 ingress 强制走 HTTP 协议。

## 类比 ★
### 一句话比喻
你以为在厨房自己炒菜（写 config.yml），但服务员（cloudflared `--token` 模式）直接无视你手里的菜谱，掏出公司总部下发的标准套餐配方（Cloudflare API 远程配置）——你说要放辣椒 (tcp://)，他偏给你做成清汤 (http://)。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 你写的 config.yml (`ssh://localhost:22`) | 你自己写的菜谱 |
| Cloudflare API 远程配置 | 总部下发的标准配方 |
| 实际执行的 `http://localhost:22` | 服务员做出来的清汤 |

## 是什么
`cloudflared tunnel run --token-file /etc/cloudflared/token` 启动时，会调用 Cloudflare API 拉取 dashboard 中该 Tunnel 的 ingress 规则。本地 config.yml 中的非 HTTP 协议（如 `tcp://`、`ssh://`、`unix://`）会被忽略，所有规则强制转为 `http://` 前缀。

## 正例
1. **日志验证**：`journalctl -u cloudflared | grep "Updated to new configuration"`，即使 config.yml 写 `ssh://localhost:22`，实际配置显示 `http://localhost:22` version=N。
2. **SSH 连接报错**：cloudflared 连 sshd 时报 `malformed HTTP status code "Debian-2"`——因为 HTTP 解析器收到了 SSH banner。

## 反例/边界
1. **本地配置模式需要 credentials JSON**：要使用真正的本地 ingress 规则，需要 `cloudflared tunnel login` 生成的 cert.pem 和手动创建的 credentials JSON 文件（包含 AccountTag、TunnelSecret、TunnelID），而非简单的 token。
2. **tcp:// ingress 仅用于 WARP 路由**：即使在本地配置模式下，`tcp://` 类型的 ingress 只能用于 Cloudflare WARP 路由的私有网络，不支持公网访问。

## 详细解释
这一条是整个 3 天折腾中最隐蔽的坑——我们反复修改 config.yml 但日志显示 config 不变，每次都是 `http://localhost:22`。直到对比两个 config 版本的日志，才发现 `Updated to new configuration version=N`——cloudflared 完全从 API 读配置。

最终方案中，Shadowsocks 能工作恰恰因为它不依赖特殊协议：仪表盘模式的 HTTP ingress 转发 WebSocket 帧时，Shadowsocks 的加密 TCP 流被包装在标准 WebSocket 二进制帧中，cloudflared 不加干预。

## 关系
### → 指向
- [[Cloudflare-Tunnel]] (Tunnel 的两种管理模式)
- [[代理协议透传兼容性]] (仪表盘 HTTP 限制决定了哪些协议能透传)

### ← 被指向
- （这是实操中发现的特定陷阱，无独立前置概念）
