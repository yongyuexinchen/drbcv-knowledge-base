---
name: Hysteria2
type: discriminant
status: core
source: "[[自建代理实操经历]]"
domain: Self-Hosted-Proxy
---

# Hysteria2（歇斯底里2）

## 类型判定
判别 — 基于 QUIC/UDP 的高速代理协议，利用 UDP 多路复用和 Brutal 拥塞控制在高延迟链路上榨取最大带宽。不适合 Cloudflare 等 L7 代理栈。

## 类比 ★
### 一句话比喻
Hysteria2 = 高速公路（QUIC/UDP），Shadowsocks = 乡间小路（TCP 单连接）。高速公路快但要自己找路——遇到收费站（Cloudflare L7）直接被拦下。乡间小路虽然绕一点（多了 Cloudflare 中转），但每个检查站都能过。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| QUIC/UDP | 不限速的高速公路 |
| Brutal 拥塞控制 | 自适应油门——根据路况实时调整速度 |
| Cloudflare L7 关卡 | 只允许"轿车"（HTTP）通行的收费站 |

## 是什么
Hysteria2 基于 IETF QUIC 协议，在 UDP 443 端口上运行。它使用自定义的 Brutal 拥塞控制算法，在高延迟（如中美 174ms）链路上能比 TCP 协议多榨取 3-5 倍带宽。原生支持端口跳跃、多路复用、模糊伪装。

## 正例
1. **笔记本直连 VPS**：`hysteria2://zt2nnfr2bstjeu94@192.255.128.175:443`，延迟 174ms，访问 Google、GitHub 正常。因为走 UDP，运营商的 TCP 封锁对它无效。
2. **手机 Nekobox**：同样配置，手机切 WiFi/流量都能用——Hysteria2 的端口跳跃能应对移动网络的 NAT 限制。

## 反例/边界
1. **不兼容 Cloudflare CDN/Tunnel**：Hysteria2 基于 QUIC/UDP，Cloudflare 免费产品的 L7 代理栈完全不支持。不能通过域名走 Cloudflare 代理。
2. **UDP QoS 限速**：部分运营商（尤其国内）对 UDP 有 QoS 限速，Hysteria2 在这些网络下可能反而不如 TCP 协议。
3. **端口被封风险**：UDP 443 在某些严格网络环境下可能被 QoS 或封锁。

## 详细解释
Hysteria2 配置特点：
- 服务端：监听 `*:443` UDP，自定义 obfs 密码，伪装 SNI 为 `www.microsoft.com`
- 客户端：通过 `hysteria2://` 链接导入，跳过证书验证 (`insecure=1`)
- 系统代理：HTTP 代理 `127.0.0.1:10809`，SOCKS5 `127.0.0.1:10808`

为什么选 Hysteria2 为主力：
- 安装和配置极简（一个二进制 + 两行配置）
- 延迟 174ms 下速度远超 VMess/VLESS TCP
- UDP 协议天然绕过运营商的 TCP 封锁（笔记本 ISP 不封 UDP）
- 相对 Reality 协议，兼容性更好（Xray 26.x 的 Reality 配置更复杂）

## 关系
### → 指向
- [[代理协议透传兼容性]] (Hysteria2 不适合 L7 代理)

### ← 被指向
- [[L4-vs-L7]] (Hysteria2 是 L4 协议)
