---
name: Shadowsocks
type: discriminant
status: core
source: "[[自建代理实操经历]]"
domain: Self-Hosted-Proxy
---

# Shadowsocks（影梭）

## 类型判定
判别 — 一种轻量级加密代理协议，无复杂握手阶段，通过加密流直接传输 TCP/UDP 数据。是唯一能无损穿透 Cloudflare Tunnel HTTP 代理的代理协议。

## 类比 ★
### 一句话比喻
Shadowsocks = 把原始信件装进加密信封（WebSocket 帧），收件人用同一把钥匙（密码）拆开。全程只有"装→发→拆"，没有多余的确认和协商。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 加密 TCP 流 | 用密码写的信，外人看不懂 |
| WebSocket 包裹 | 在加密信外面套一层标准快递袋 |
| cloudflared 转交 | 快递中转站：只检查快递袋格式，不看内容 |

## 是什么
Shadowsocks 使用预共享密钥（pre-shared key）加密 TCP/UDP 流。客户端加密原始流量 → 服务端解密 → 转发到目标。与 VLESS/VMess 的核心区别：没有多轮握手和协议协商，连接建立后直接传输加密数据流。

## 正例
1. **Shadowsocks + WebSocket + Cloudflare Tunnel**：WebSocket 建立后，SS 加密流作为二进制帧传输。cloudflared 看到的是标准 WebSocket 帧，不做干预。实测 Google 200 (2.5s)，GitHub 200 (3.1s)。
2. **SS + v2ray-plugin (WebSocket 伪装)**：标准的 SS 通过 Cloudflare CDN 的方案，将 SS 流伪装成 HTTPS WebSocket 流量。

## 反例/边界
1. **性能不如 Hysteria2**：SS 是 TCP 单连接，Hysteria2 的 QUIC 多路复用延迟更低（174ms vs SS+CF 的 2-3s）。
2. **不适合高延迟场景的流媒体**：通过 Cloudflare Tunnel 的 SS 延迟较高，适合日常浏览和开发，不适合视频。

## 详细解释
SS 的协议栈（通过 Cloudflare Tunnel）：
```
V2RayN
  └─ Shadowsocks (aes-256-gcm 加密 TCP 流)
      └─ WebSocket (ws, path=/ws)
          └─ TLS (Cloudflare 边缘终止)
              └─ Cloudflare Tunnel (QUIC/HTTP2)
                  └─ cloudflared (HTTP 转发)
                      └─ Xray SS Inbound (解密 → 外网)
```

为什么 SS 能过而 VLESS 不能：
- VLESS 握手：客户端 → 0x00 版本号 → 服务端响应 → 加密协商 → 流控建立 → 传输
- SS 连接：客户端 → 加密数据流（直接从第一个字节开始）
- cloudflared 在 WebSocket 升级后缓存数据帧重组，VLESS 的多轮握手被打断，SS 的单向流不受影响

配置参数：
- 加密方法: `aes-256-gcm`
- 密码: `zt2nnfr2bstjeu94`
- 传输: WebSocket
- 路径: `/ws`

## 关系
### → 指向
- [[代理协议透传兼容性]] (SS 是唯一兼容的协议)
- [[WebSocket传输]] (SS 通过 WS 承载)

### ← 被指向
- [[Cloudflare-Tunnel]] (Tunnel 是 SS 的传输通道)
