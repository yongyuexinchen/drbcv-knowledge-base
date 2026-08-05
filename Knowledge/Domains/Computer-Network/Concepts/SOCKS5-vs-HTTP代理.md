---
name: SOCKS5-vs-HTTP代理
type: connection
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# SOCKS5 vs HTTP 代理（正向代理的两种实现）

## 类型判定
关系 — 正向代理的两种协议。SOCKS5 更底层，可代理任意 TCP/UDP；HTTP 代理只代理 HTTP/HTTPS 流量。选择哪种直接影响 DNS 解析位置和浏览器兼容性。

## 类比 ★
### 一句话比喻
SOCKS5 = 万能插座转换器——不管什么插头（HTTP、FTP、游戏），插上去都能通电。HTTP 代理 = 专用充电器——只能充 HTTP/HTTPS 协议的设备，其他设备插不上。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| SOCKS5 (代理所有协议) | 万能插座——什么插头都能插 |
| HTTP 代理 (只代理 HTTP) | 专用充电器——只适配特定设备 |
| 远程 DNS 解析 | 代为查询——不用本地电话本 |

## 是什么
- **SOCKS5 代理**（`127.0.0.1:10808`）：工作在传输层（L4），代理 TCP 连接。不解析 HTTP 内容，不修改数据。DNS 默认在本地解析（可配远程 DNS）。
- **HTTP 代理**（`127.0.0.1:10809`）：工作在应用层（L7），只代理 HTTP/HTTPS 请求。HTTPS 通过 CONNECT 方法做隧道。DNS 在服务端（VPS）解析。

## 正例
1. **笔记本用 10809 (HTTP 代理)**：解决了 DNS 污染——VPS 端解析 DNS，返回真实 IP。Chrome/Edge/Firefox 全部可用。
2. **Firefox 用 10808 (SOCKS5) + 远程 DNS**：`about:config` → `network.proxy.socks_remote_dns=true`。效果等同于 HTTP 代理的远程 DNS。
3. **V2RayN 自动提供两种**：SOCKS5 端口 10808 + HTTP 代理端口 10809——开一个 V2RayN，两个端口同时可用。

## 反例/边界
1. **SOCKS5 默认本地 DNS**：浏览器配 SOCKS5 代理 `127.0.0.1:10808` 但不开远程 DNS → DNS 查询走本地 → 被污染 → Google 超时。这是项目初期最大的坑之一。
2. **HTTP 代理不支持非 HTTP 协议**：FTP、SSH、游戏不能走 HTTP 代理——这些必须用 SOCKS5 或 VPN。
3. **部分软件不支持 HTTP 代理**：比如终端 `curl --socks5` 比 `curl -x http://` 更通用——但不是所有软件都有 SOCKS5 选项。

## 详细解释
本项目的代理配置演进：
```
第一版（翻车）：
  系统代理 127.0.0.1:10808 (SOCKS5)
  → DNS 本地解析 → 污染 → Google 打不开

第二版（Firefox 单独解决）：
  Firefox SOCKS5 + socks_remote_dns=true
  → Firefox 能用了，Chrome 仍不行

第三版（最终方案）：
  系统代理 127.0.0.1:10809 (HTTP 代理)
  → DNS VPS 端解析 → 所有浏览器都能用了
```

选择铁律：**不懂就选 HTTP 代理**——DNS 自动在远端解析，不踩污染坑。

## 关系
### → 指向
- [[正向代理-vs-反向代理]] (两种都是正向代理的实现)
- [[DNS污染]] (代理类型决定了 DNS 解析位置)

### ← 被指向
- [[Hysteria2]] (Hysteria2 同时提供 SOCKS5 和 HTTP 两种代理端口)
