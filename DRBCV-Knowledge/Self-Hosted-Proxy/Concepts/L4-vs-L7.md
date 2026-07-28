---
name: L4-vs-L7
type: connection
status: core
source: "[[自建代理实操经历]]"
domain: Self-Hosted-Proxy
---

# Layer 4 vs Layer 7 代理

## 类型判定
关系 — 网络代理在两个不同协议层级上的本质差异，是理解"为什么 Cloudflare 免费版不能代理 VLESS"的基础。

## 类比 ★
### 一句话比喻
L4 代理 = 快递员，只管把包裹从 A 送到 B，不拆封不看内容。L7 代理 = 海关安检，每个包裹都要拆开检查，发现包装不合规（不是标准 HTTP）直接扔进焚烧炉。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| L4 代理 (TCP/UDP) | 快递员：不管箱子里装什么，送到就行 |
| L7 代理 (HTTP) | 海关：开箱检查，只放行合法物品 |
| VLESS 二进制帧 | 没有报关单的走私货——海关当即销毁 |

## 是什么
- **L4（传输层）代理**：工作在 TCP/UDP 层，只转发数据包，不解析内容。例：Cloudflare Spectrum ($5/月)、HAProxy TCP 模式。
- **L7（应用层）代理**：工作在 HTTP/HTTPS 层，解析 HTTP 头和 WebSocket 帧，可按 URL 路由。例：Cloudflare CDN、Nginx、Cloudflare Tunnel。

## 正例
1. **Hysteria2 直连 VPS**：UDP 端口 443 → VPS，纯 L4 转发，运营商只能看到加密 UDP 包，无法拦截（笔记本/手机可用）。
2. **ttyd 网页终端**：HTTP/WebSocket 服务 → Cloudflare Tunnel（L7），完美兼容——因为 ttyd 本身就是 HTTP 协议。

## 反例/边界
1. **VLESS + Cloudflare CDN**：Cloudflare CDN 是 L7 HTTP 代理，收到 VLESS 二进制帧后无法解析，直接丢弃或触发 WAF——这就是为什么走橙色云 DNS 的代理都连不上。
2. **Cloudflare Tunnel 看起来像 L4，实际上仍然是 L7**：ingress 永远是 HTTP 协议，即使 Type 选 TLS，底层仍是 HTTP 连接。

## 详细解释
免费 Cloudflare 产品的 L4/L7 边界：
| 产品 | 层级 | 协议 | 费用 |
|------|:--:|------|:--:|
| CDN (橙色云) | L7 | HTTP/HTTPS only | 免费 |
| Tunnel | L7 | HTTP only (ingress) | 免费 |
| Spectrum | L4 | 任意 TCP/UDP | $5/月起 |

这个表是整整三天的折腾浓缩成的一行——我们试了 CDN、Tunnel、各种协议组合，每次都死在 L7 的 HTTP 过滤上。最终 Shadowsocks 能过，不是因为它"兼容 L7"，而 是因为它无握手+加密流刚好不触发 L7 的协议检测。

## 关系
### → 指向
- [[Cloudflare-Tunnel]] (Tunnel 是 L7 代理的典型实现)
- [[代理协议透传兼容性]] (理解 L4/L7 是判断协议能否透传的前提)

### ← 被指向
- （无前置概念——这是网络架构的基础概念层）
