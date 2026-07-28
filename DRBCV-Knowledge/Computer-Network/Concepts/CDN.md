---
name: CDN
type: discriminant
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# CDN（内容分发网络）

## 类型判定
判别 — 全球分布的缓存服务器网络。用户访问网站时，CDN 将请求引导到最近的节点，加速访问并隐藏源站真实 IP。

## 类比 ★
### 一句话比喻
CDN = 连锁便利店（7-Eleven）。总部（源站 VPS）只在洛杉矶有一家工厂，但全球每个城市都有便利店（CDN 节点）。你买一瓶水不用飞到洛杉矶——去街角便利店就行，便利店缺货才从工厂调货。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 源站 VPS (192.255.128.175) | 洛杉矶的工厂 |
| CDN 节点 (104.21.96.47) | 街角的连锁便利店 |
| 用户访问域名 | 去最近便利店买东西 |
| 橙色云 (Proxied) | 便利店代售模式 |

## 是什么
Cloudflare CDN 在全球 300+ 城市有节点。当你把域名的 DNS 设为"橙色云"（Proxied），用户访问域名时 DNS 返回的是 CDN 节点的 IP（如 `104.21.96.47`），而非源站 IP。CDN 节点接收请求 → 缓存命中则直接返回 → 未命中则回源（到 VPS 取数据）。

## 正例
1. **隐藏源站 IP**：`vps.yongyuexinchen.xin` 解析到 Cloudflare CDN IP (`104.21.x.x`)，而非 `192.255.128.175`——GFW 和运营商看不到真实 VPS IP。
2. **DDoS 防护**：攻击流量打在 Cloudflare 全球节点上，由 Cloudflare 吸收，VPS 不受影响。

## 反例/边界
1. **CDN 只代理 HTTP/HTTPS**：免费版 CDN 只转发 80/443 端口的 HTTP 流量。SSH (22)、VLESS (非标准 HTTP) 不能走 CDN。
2. **CDN 是 L7 代理——和我们试了 9 次才搞懂的坑**：CDN 理解 HTTP 协议，会检查 WebSocket 帧，非标准代理协议的二进制帧被丢弃——这就是 VLESS+CDN 失败的原因。
3. **CDN ≠ Tunnel**：CDN 是"用户→CDN→源站"的三角代理，Tunnel 是"用户→CF→Tunnel→内网服务"的隧道。Tunnel 的底层也是 L7 HTTP，但它可以做 hostname 路由。

## 详细解释
橙色云 vs 灰色云：
```
橙色云 (Proxied):
用户 → DNS 查询 → 返回 CDN IP (104.21.96.47) → CDN 节点 → VPS
(源站 IP 隐藏，CDN 做缓存和过滤)

灰色云 (DNS only):
用户 → DNS 查询 → 返回源站 IP (192.255.128.175) → 直连 VPS
(源站 IP 暴露，但不受 CDN 协议限制)
```

本项目 DNS 记录全部设为橙色云——这是通过 Cloudflare 隐藏源站、绕过 ISP 封锁的前提。但代价是 CDN 的 L7 过滤让我们折腾了 9 次协议测试。

## 关系
### → 指向
- [[L4-vs-L7]] (CDN 是 L7 代理)
- [[DNS]] (CDN 依赖 DNS 将用户引导到最近节点)
- [[代理协议透传兼容性]] (CDN 的 L7 限制决定了哪些协议能过)

### ← 被指向
- [[Cloudflare-Tunnel]] (Tunnel 是 CDN 的补充——解决 CDN 不能访问内网的问题)
