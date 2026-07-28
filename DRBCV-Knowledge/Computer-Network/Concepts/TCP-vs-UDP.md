---
name: TCP-vs-UDP
type: connection
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# TCP vs UDP（传输层协议对比）

## 类型判定
关系 — 互联网数据传输的两种基本方式，是理解"为什么 Hysteria2 比 Shadowsocks 快"和"为什么 Hysteria2 不能过 Cloudflare"的前提。

## 类比 ★
### 一句话比喻
TCP = 寄挂号信——必须对方签收确认，丢了一页就重发，顺序不能乱。UDP = 扔纸飞机——扔出去不管对方收没收到，快但不保证。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| TCP 三次握手 + 确认机制 | 挂号信：签收、确认、丢了重寄 |
| UDP 无连接直接发 | 扔纸飞机：不确认、不重发、丢了就丢了 |
| QUIC (UDP升级版) | 纸飞机上装了GPS和编号——快且不会丢 |

## 是什么
- **TCP**（传输控制协议）：面向连接，保证数据按序到达、不丢失、不重复。需要三次握手建立连接。HTTP、SSH、Shadowsocks 都用 TCP。
- **UDP**（用户数据报协议）：无连接，直接发送数据包，不保证到达。速度快但不可靠。Hysteria2、视频通话、DNS 查询都用 UDP。

## 正例
1. **Shadowsocks 走 TCP**：通过 Cloudflare Tunnel 时需要 WebSocket（基于 TCP），慢但稳定，能过 HTTP 代理。
2. **Hysteria2 走 UDP**：直连 VPS 时用 QUIC/UDP，延迟 174ms 下比 TCP 快 3-5 倍——因为 UDP 不需要握手确认，丢包也不等重传。
3. **浏览器访问网站**：HTTP/HTTPS 走 TCP——网页必须完整加载，不能丢数据。

## 反例/边界
1. **GFW 对 UDP 的 Qos 限速**：部分运营商对 UDP 限速，可能导致 Hysteria2 反而不如 TCP。
2. **Cloudflare 不接受 UDP**：免费 Cloudflare CDN/Tunnel 只处理 TCP 上的 HTTP，UDP 协议（Hysteria2）完全不能过。
3. **不是"UDP 永远比 TCP 快"**：在低丢包网络下两者差别不大；高丢包时 QUIC 的优化才有优势。

## 详细解释
TCP 连接过程（为什么"三次握手"）：
```
客户端                      服务器
   |--- SYN (我想连接)-------->|
   |<-- SYN+ACK (收到，你继续)-|
   |--- ACK (好的，开传)------>|
   |<===== 数据传输 ==========>|
```

UDP 连接过程（为什么"无连接"）：
```
客户端                      服务器
   |===== 数据包1 ===========>|
   |===== 数据包2 ===========>|  (可能丢了)
   |===== 数据包3 ===========>|
   (不确认，不重发)
```

Hysteria2 用的 QUIC 是"UDP 升级版"——在 UDP 之上加了确认、重传、多路复用，既快又可靠。这就是为什么 Hysteria2 直连是最优方案。

## 关系
### → 指向
- [[DNS]] (DNS 查询默认走 UDP)
- [[HTTP协议]] (HTTP/1.1 和 HTTP/2 走 TCP)

### ← 被指向
- [[Hysteria2]] (基于 QUIC/UDP)
- [[Shadowsocks]] (基于 TCP)
