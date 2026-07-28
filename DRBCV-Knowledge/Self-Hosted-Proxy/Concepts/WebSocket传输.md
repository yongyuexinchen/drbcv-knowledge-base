---
name: WebSocket传输
type: discriminant
status: core
source: "[[自建代理实操经历]]"
domain: Self-Hosted-Proxy
---

# WebSocket 传输层（代理协议载体）

## 类型判定
判别 — HTTP 协议升级机制，允许在 HTTP 连接之上建立全双工持久通信通道。是代理协议（Shadowsocks/VLESS/VMess）穿透 HTTP 反向代理时最常用的载体。

## 类比 ★
### 一句话比喻
WebSocket = 打电话时先按标准流程拨号（HTTP 握手），接通后切换到加密对讲机模式（WebSocket 帧）。前面的拨号过程（HTTP Upgrade）所有人都能看懂，后面对讲机里说什么（代理协议数据）只有双方知道。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| HTTP Upgrade 握手 | 标准拨号："喂，请转加密频道" |
| WebSocket 二进制帧 | 对讲机的加密语音包 |
| cloudflared HTTP 代理 | 电话总机——允许转接，但会监听拨号过程 |

## 是什么
WebSocket 通过 HTTP/1.1 的 `Upgrade: websocket` 头建立连接后，切换为二进制帧协议。每个 WebSocket 帧有 2-14 字节的头（opcode、掩码、长度），后面跟 payload。代理协议（SS/VLESS）的数据被放在 payload 中传输。

## 正例
1. **Shadowsocks + WebSocket + Cloudflare Tunnel ✅**：WebSocket 升级成功 → SS 加密流作为二进制帧传输 → cloudflared 只看到标准 WebSocket 帧 → 透传成功。
2. **ttyd 网页终端**：ttyd 用 WebSocket 传输终端 I/O，Cloudflare Tunnel 完美代理——因为全是标准 WebSocket 帧。

## 反例/边界
1. **VLESS over WebSocket ❌**：WebSocket 升级本身成功（curl 返回 400 证明 Xray 收到了），但 VLESS 握手数据在 WebSocket 帧中被 cloudflared 缓存/重组，握手时序断裂。
2. **Xray 26.x 已弃用 WebSocket**：官方推荐迁移到 XHTTP (HTTP/2 + HTTP/3)。但对 Cloudflare Tunnel 环境，XHTTP 兼容性同样不好。
3. **WebSocket 帧的 opcode 限制**：代理协议通常只用 Binary (0x2) 帧，不用 Text (0x1)。cloudflared 可能对非文本 WebSocket 帧做额外处理。

## 详细解释
WebSocket 帧结构（简化）：
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |                               |
|N|V|V|V|       |S|             |                               |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+-------------------------------+
```

为什么 cloudflared 可能破坏 VLESS 的 WebSocket 帧：
1. **掩码处理**：客户端发出的帧有掩码（MASK=1），服务端去掩码。cloudflared 作为中间代理可能需要重新掩码——这一步骤如果处理不当，会改变帧内的 VLESS 协议数据。
2. **帧分片重组**：VLESS 握手数据可能跨多个 WebSocket 帧，cloudflared 的 HTTP 代理可能缓存并重组这些帧，导致帧边界变化。
3. **X-Forwarded-For 注入**：cloudflared 的 HTTP 代理会在初始 HTTP 请求中添加头，这些额外的数据可能干扰协议嗅探。

## 关系
### → 指向
- [[代理协议透传兼容性]] (WS 是兼容性分析的核心载体)
- [[L4-vs-L7]] (WS 是 L7 协议，需考虑 HTTP 代理行为)

### ← 被指向
- [[Shadowsocks]] (SS 通过 WS 承载)
- [[Cloudflare-Tunnel]] (Tunnel 是 WS 的代理层)
