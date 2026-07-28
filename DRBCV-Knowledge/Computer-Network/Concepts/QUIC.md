---
name: QUIC
type: discriminant
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# QUIC 协议

## 类型判定
判别 — Google 开发的下一代传输协议，基于 UDP 但内置了 TCP 的可靠性和 TLS 的加密。HTTP/3 和 Hysteria2 都运行在 QUIC 之上。

## 类比 ★
### 一句话比喻
TCP = 单车道公路——一次只能过一辆车（一个请求），堵车就全等。QUIC = 多车道高速公路——多辆车（多路复用）同时跑在不同的车道上，一辆车爆胎（丢包）只堵那条车道，其他车照开不误。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| TCP 单流（队头阻塞） | 单车道：前面车停，后面全堵 |
| QUIC 多流（独立流） | 多车道：左车道堵了，右车道继续 |
| QUIC 0-RTT 重连 | 办了 ETC——不用再停车排队 |
| UDP 底层 | 不限速的高速公路匝道 |

## 是什么
QUIC 在 UDP 之上实现了：①0-RTT/1-RTT 连接建立（比 TCP+TLS 快一个往返）②多路复用（无队头阻塞）③内置 TLS 1.3 加密 ④连接迁移（切 WiFi 不断连）。HTTP/3 就是 HTTP over QUIC。Hysteria2 用自定义协议替代 HTTP 层，直接跑在 QUIC 上。

## 正例
1. **Hysteria2 基于 QUIC**：`hysteria2://...` 走 QUIC/UDP 443，延迟 174ms 下比 TCP 快 3-5 倍——因为 QUIC 的 0-RTT 和多路复用消除了 TCP 的握手和队头阻塞开销。
2. **Google/YouTube 已全面 HTTP/3**：访问这些网站时浏览器自动升级到 QUIC——你可以感受到加载更快，尤其在丢包网络下。

## 反例/边界
1. **不兼容 HTTP 代理栈**：Cloudflare CDN/Tunnel 的免费 L7 代理只处理 HTTP/1.1 和 HTTP/2（TCP），不处理 QUIC (UDP)——这就是 Hysteria2 不能走 Cloudflare 的根本原因。
2. **UDP Qos 限速**：部分运营商对 UDP 做 Qos 限速，QUIC 在这些网络下可能反而不如 TCP。
3. **QUIC 的 0-RTT 重放攻击风险**：0-RTT 数据可能被攻击者重放——对代理场景影响不大，但对银行转账等操作需服务端额外防护。

## 详细解释
QUIC vs TCP+TLS 的连接建立对比：
```
TCP + TLS 1.2 (3-RTT):
  客户端 → SYN → 服务器           (1 RTT)
  服务器 → SYN+ACK → 客户端
  客户端 → ACK + ClientHello →   (1 RTT)
  服务器 → ServerHello + 证书 →   (1 RTT)
  开始传输                       (总计 3 RTT)

QUIC (1-RTT / 0-RTT):
  客户端 → ClientHello → 服务器   (1 RTT)
  服务器 → 证书 + 完成 → 
  开始传输                       (总计 1 RTT)
  
  (重连时 0-RTT——直接发数据)
```

在 174ms 的中美延迟下，TCP+TLS 握手就吃掉 522ms（3×174），QUIC 只需 174ms（1×174）——节省了 348ms。这就是为什么 Hysteria2 直连体验明显好于 Shadowsocks+CF。

## 关系
### → 指向
- [[TCP-vs-UDP]] (QUIC 基于 UDP 但实现了 TCP 的功能)
- [[TLS-SSL]] (QUIC 内置 TLS 1.3)

### ← 被指向
- [[Hysteria2]] (Hysteria2 基于 QUIC)
