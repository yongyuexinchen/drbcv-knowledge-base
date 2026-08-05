---
name: HTTP协议
type: discriminant
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# HTTP 协议

## 类型判定
判别 — 互联网最基础的通信协议，定义了浏览器和服务器之间"请求-响应"的格式。几乎所有的 Web 服务、API、CDN、反向代理都建立在 HTTP 之上。

## 类比 ★
### 一句话比喻
HTTP = 餐厅的点餐流程。你坐下说"我要一份红烧牛肉面"（GET /noodles），服务员（服务器）回"好的，200 元"（HTTP 200 OK）然后端上来。如果你点的菜不在菜单上（GET /ws 但服务器没配这个路径），服务员回"404 找不到"。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| HTTP 请求 (GET /path) | 点菜：我要 XX |
| HTTP 状态码 (200/404/502) | 服务员回答：有了/没有/厨房坏了 |
| HTTP 头 (Headers) | 备注：不要香菜、加辣 |

## 是什么
HTTP 是无状态、文本化的请求-响应协议。客户端发送 `METHOD /path HTTP/1.1` + 头部 + 可选 Body → 服务器返回 `HTTP/1.1 200 OK` + 头部 + Body。HTTP/2 和 HTTP/3 增加了多路复用和二进制帧，但核心的"请求-响应"模型不变。

## 正例
1. **curl 测试的 400/404 响应**：`curl https://vps.yongyuexinchen.xin/ws` → HTTP 400。这是纯 HTTP 请求，Xray 正确返回了状态码。
2. **ttyd 网页终端**：浏览器发 HTTP 请求 → ttyd 返回 HTML 页面 → WebSocket 升级 → 终端交互。全程 HTTP 生态。

## 反例/边界
1. **HTTP ≠ 原始 TCP**：不能把非 HTTP 协议（VLESS、SSH）直接丢给 HTTP 代理——代理期望 HTTP 格式，收到二进制数据会崩溃（`malformed HTTP status code "Debian-2"`）。
2. **HTTP 无状态 ≠ 不能保持连接**：HTTP/1.1 有 Keep-Alive，WebSocket 可以做持久连接——但底层仍然是 HTTP 协议。
3. **WebSocket 是 HTTP 的"升级"**：WebSocket 开始是 HTTP（Upgrade 头），成功后切换为二进制帧——但这依赖 HTTP 代理正确支持 Upgrade。cloudflared 在这步出了我们遇到的坑。

## 详细解释
关键的 HTTP 状态码（本项目遇到的）：
| 状态码 | 含义 | 本项目的实际场景 |
|:--:|------|------|
| 200 | OK | Google 能打开 |
| 302 | 重定向 | Cloudflare Access 跳转登录页 |
| 400 | 错误请求 | curl 访问 Xray `/ws`——缺少 WebSocket 升级 |
| 403 | 禁止 | CF Tunnel 拒绝 tinyproxy HTTP CONNECT |
| 404 | 未找到 | curl 访问 Xray `/`——没有这个路径 |
| 502 | 网关错误 | Tunnel 连不上源站（旧 521 状态页） |
| 521 | 服务器宕机 | Cloudflare 连不上源站 |

curl 的 400 和 404 是我们在排错时最有用的信息——它证明了 Tunnel 是通的、DNS 是对的、问题出在协议层而非网络层。

## 关系
### → 指向
- [[TLS-SSL]] (HTTPS = HTTP + TLS)
- [[WebSocket传输]] (WebSocket 是 HTTP 的升级协议)
- [[CDN]] (CDN 主要是 HTTP 加速)

### ← 被指向
- [[Cloudflare-Tunnel]] (Tunnel ingress 走 HTTP)
- [[SOCKS5-vs-HTTP代理]] (HTTP 代理是一种正向代理)
