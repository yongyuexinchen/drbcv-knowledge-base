---
name: DNS污染
type: discriminant
status: core
source: "[[自建代理实操经历]]"
domain: Self-Hosted-Proxy
---

# DNS 污染

## 类型判定
判别 — GFW 在 DNS 解析阶段返回伪造 IP 地址，导致浏览器访问 Google 时实际连到了 GFW 的封锁页面而非真实服务器。

## 类比 ★
### 一句话比喻
你打电话问 114："Google 公司地址在哪？" 114（DNS）被人篡改了电话本，告诉你一个假的地址（污染 IP）。你按假地址找过去——发现是派出所（GFW 封锁页）。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| DNS 查询 google.com | 打 114 查公司地址 |
| 被污染的 DNS 服务器 | 被篡改的电话本 |
| 返回的假 IP | 骗子给的假地址 |

## 是什么
GFW 在 DNS 查询经过国际出口时，抢在真实 DNS 响应之前返回一个虚假的 IP 地址。客户端收到假 IP 后连接到 GFW 重置服务器，连接被 RST 或重定向。这是最常见的网络封锁手段之一。

## 正例
1. **笔记本的坑**（已解决）：SOCKS5 代理默认用本地 DNS 解析，然后通过代理连接——本地解析到假 IP，代理连过去被 RST。解决方法：Firefox 开 `socks_remote_dns=true`，或 Windows 用 HTTP 代理模式（代理端解析 DNS，即在 VPS 上解析）。
2. **Hysteria2 自动处理**：HTTP 代理模式 (`127.0.0.1:10809`) 天然在服务端解析 DNS，Chrome/Edge/Firefox 全都正常。

## 反例/边界
1. **SNI 检测更隐蔽**：即使 DNS 解析正确，GFW 还能通过 TLS 握手中的 SNI（Server Name Indication）字段识别目标域名。DNS 污染只是封锁链的第一环。
2. **国内 DNS vs 国际 DNS**：`114.114.114.114` 也会被污染，`8.8.8.8` (Google DNS) 可能被劫持。DoH/DoT（DNS over HTTPS/TLS）可以防劫持，但连接 DoH 服务器本身可能被封锁。

## 详细解释
架构中 DNS 污染的处理：
- **笔记本**：Hysteria2 HTTP 代理 → 服务端解析 DNS → 不受本地 DNS 污染影响
- **手机**：Nekobox 默认远程 DNS → 同样不受影响
- **家里电脑（Shadowsocks+Cloudflare）**：SS 代理自动在 VPS 端解析 DNS，也不受影响

这是为什么"管 VPS 比管客户端的 DNS 容易"——代理的 DNS 解析全移到 VPS 侧，本地 DNS 配置可以完全不管。

## 关系
### → 指向
- [[ISP封锁]] (DNS 污染是 ISP 封锁的一种手段)
- [[反向代理架构]] (远程 DNS 解析是架构的隐含优势)

### ← 被指向
- （DNS 是网络基础层概念）
