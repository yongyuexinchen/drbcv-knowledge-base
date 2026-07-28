---
name: Cloudflare-Tunnel
type: discriminant
status: core
source: "[[自建代理实操经历]]"
domain: Self-Hosted-Proxy
---

# Cloudflare Tunnel（反向隧道）

## 类型判定
判别 — Cloudflare 提供的一种免费反向代理隧道，让内网服务通过出站连接暴露到公网。

## 类比 ★
### 一句话比喻
你在地下室开了一家店（VPS），外面的人进不来。Cloudflare Tunnel = 你从地下室挖了一条秘密通道直通商场大门口（Cloudflare CDN），顾客在商场门口就能找到你——通道是你自己挖的（出站连接），保安（运营商）拦不住。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| VPS 主动连接 Cloudflare（出站） | 你从地下室往外挖通道 |
| ISP 只看到去 Cloudflare 的流量 | 保安看到你在挖地，以为你在装修 |
| 用户通过域名访问服务 | 顾客在商场门口看到你的招牌 |

## 是什么
Cloudflare Tunnel 是一个反向代理隧道。VPS 上的 cloudflared 客户端主动连接到 Cloudflare 边缘网络，建立持久连接。外部用户的请求通过 Cloudflare → 这条隧道 → VPS 上的本地服务。因为连接是 VPS 主动发起的（出站），运营商的入站封锁对它无效。

## 正例
1. **VPS IP 被运营商封锁**：家里电脑无法直连 192.255.128.175，但通过 `vps.yongyuexinchen.xin`（走 Tunnel）可以访问 VPS 上的服务。
2. **ttyd 网页终端**：VPS 跑 ttyd 在 127.0.0.1:7681，Tunnel 入口 `ssh.yongyuexinchen.xin` → `localhost:7681`，任何浏览器都能打开。

## 反例/边界
1. **不是 TCP 代理**：Tunnel 的 ingress 永远走 HTTP 协议。即使选 Type="SSH"，底层仍是 `http://localhost:22`。这导致 sshd 返回 SSH banner → cloudflared HTTP 解析器崩溃。
2. **不能透传原始 TCP**：需要 $5/月的 Cloudflare Spectrum 才能做 Layer 4 TCP 代理。
3. **仪表盘模式不读本地 config.yml**：`cloudflared tunnel run --token` 从 Cloudflare API 拉远程配置，本地 config.yml 的 `tcp://` 或 `ssh://` 被忽略。

## 详细解释
cloudflared 运行在仪表盘管理模式（`--token-file`）时：
1. 从 Cloudflare API 拉取 ingress 规则
2. 所有 ingress 规则强制为 HTTP 协议
3. 即使 dashboard 里选 SSH 类型，rule 仍为 `http://localhost:22`

要使用非 HTTP 协议必须切到本地配置模式（需要 credentials JSON 文件），但该模式下的 `tcp://` ingress 仅用于 WARP 路由的私有网络，不适用于公网访问。

## 关系
### → 指向
- [[L4-vs-L7]] (Tunnel 是 L7 HTTP 隧道，不是 L4 TCP 隧道)
- [[cloudflared-仪表盘陷阱]] (为什么本地配置被远程覆盖)
- [[反向代理架构]] (Tunnel 就是一种反向代理)

### ← 被指向
- [[代理协议透传兼容性]] (为什么 VLESS 过不了 Tunnel 但 Shadowsocks 能)
