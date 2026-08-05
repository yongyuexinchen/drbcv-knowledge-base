---
name: 正向代理-vs-反向代理
type: connection
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# 正向代理 vs 反向代理

## 类型判定
关系 — 两种方向相反的代理模式。正向代理代表客户端访问外网，反向代理代表服务端接收外部请求。理解这个区别是整个 VPS 代理架构的基础。

## 类比 ★
### 一句话比喻
正向代理 = 你请一个代购帮你从海外买东西——代购代表你（客户端）去访问目标网站。反向代理 = 商场门口的前台——前台代表商场（服务端）接待所有顾客，然后分发给各个店铺。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 正向代理 (V2RayN → VPS → Google) | 代购：你给钱，他帮你从海外买 |
| 反向代理 (用户 → CF → VPS 服务) | 商场前台：顾客找前台，前台引到店铺 |
| SOCKS5/HTTP 代理 | 正向代理的具体实现 |

## 是什么
- **正向代理**：部署在客户端一侧。客户端配置代理地址（如 `127.0.0.1:10809`），所有请求先到代理，代理代为访问目标。V2RayN、Hysteria2、机场订阅都是正向代理。
- **反向代理**：部署在服务端一侧。用户访问代理的域名，代理将请求转发到内网服务。Nginx、Cloudflare Tunnel 是反向代理。

## 正例
1. **笔记本的 Hysteria2——正向代理**：`127.0.0.1:10809` → Hysteria2 客户端 → VPS → Google。电脑不知道 Google 的真实地址，全由 VPS 代劳。
2. **Cloudflare Tunnel——反向代理**：用户访问 `vps.yongyuexinchen.xin` → Cloudflare → cloudflared → Xray:10000。用户不知道 VPS 内网结构和端口。
3. **Nginx 反向代理**：`api.example.com` → Nginx → `localhost:8000`。外部只看到 Nginx 的 443 端口。

## 反例/边界
1. **VPN 不是纯正向代理**：VPN 工作在网络层（L3），代理工作在应用层（L7）。VPN 代理所有流量，正向代理只代理配置了代理的软件。
2. **Cloudflare Tunnel 不是正向代理**（常见误解）：有人以为 Tunnel 能把 VPS 的流量"推"出来，实际上 Tunnel 是反向代理——用户请求主动进入 Tunnel。
3. **一个服务可以同时用两种代理**：VPS 上 Xray 的 SS Inbound（接收正向代理流量）通过 Cloudflare Tunnel（反向代理）暴露给外部——两层代理嵌套。

## 详细解释
本项目中的两种代理共存：
```
【正向代理】                    【反向代理】
笔记本                        外部用户
  │                             │
  ├─ Hysteria2 ─→ VPS ─→ Google │
  │                             │
  └─ Shadowsocks ─→ CF Tunnel ─→ VPS Xray ─→ Google
                    (正向)       (反向)
```

Cloudflare Tunnel 之所以能绕过 ISP 封锁，是因为它把"VPS 等待入站连接"（被封锁）变成了"VPS 主动连接 Cloudflare"（出站不封）——反向代理的连接方向是反的。

## 关系
### → 指向
- [[反向代理架构]] (反向代理的具体架构设计)
- [[SOCKS5-vs-HTTP代理]] (正向代理的两种实现)

### ← 被指向
- [[Cloudflare-Tunnel]] (Tunnel 是反向代理)
- [[Hysteria2]] (Hysteria2 本地 HTTP 代理是正向代理)
