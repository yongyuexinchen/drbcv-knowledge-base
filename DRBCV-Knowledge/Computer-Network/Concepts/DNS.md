---
name: DNS
type: discriminant
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# DNS（域名系统）

## 类型判定
判别 — 互联网的电话本，把人类可读的域名（`google.com`）翻译成机器可读的 IP 地址（`142.250.80.46`）。

## 类比 ★
### 一句话比喻
DNS = 手机通讯录。你存的是"张三"（域名），拨号时手机自动查通讯录找到 138xxxx（IP 地址）。如果通讯录被篡改——"张三"变成了诈骗电话——你打过去就是假的。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 域名 (google.com) | 通讯录里的联系人名字 |
| IP 地址 (142.250.80.46) | 实际的电话号码 |
| DNS 服务器被污染 | 通讯录被黑客篡改——假号码 |
| DNS over HTTPS (DoH) | 加密通讯录——篡改者看不到你查谁 |

## 是什么
DNS 是分层的分布式数据库。当你输入 `google.com`：
1. 浏览器问本地 DNS 服务器（通常是运营商提供的）
2. 本地 DNS 逐级向上查询：根 DNS → `.com` DNS → `google.com` DNS
3. 返回 IP 地址
4. GFW 可以在这个过程的第 2 步拦截，抢在真实响应之前返回假 IP

## 正例
1. **正常 DNS 解析**：`nslookup google.com` → 返回真实 IP `142.250.x.x`，浏览器连接成功。
2. **代理端 DNS 解析（推荐）**：HTTP 代理模式 (`127.0.0.1:10809`) 下，DNS 查询在 VPS 端（美国）执行，返回的是真实 IP，不受中国 DNS 污染影响。

## 反例/边界
1. **DNS 污染**：GFW 在 DNS 查询经过国际出口时注入假 IP 响应。本地 DNS 服务器（`114.114.114.114`）本身没有被篡改，是查询结果被拦截篡改。
2. **DNS 劫持**：更彻底的攻击——直接把你的 DNS 请求重定向到 GFW 控制的假 DNS 服务器。
3. **DNS 不是唯一被封的环节**：即使 DNS 正确（如通过代理解析），GFW 还能通过 SNI 检测和 IP 封锁拦截连接。

## 详细解释
DNS 记录类型（我们实际用到的）：
| 类型 | 全称 | 作用 | 本项目的例子 |
|------|------|------|------|
| A | Address | 域名 → IPv4 | `vps.yongyuexinchen.xin` → `192.255.128.175` |
| CNAME | Canonical Name | 域名 → 另一个域名 | `www` → `@` |
| NS | Name Server | 指定 DNS 服务器 | `deb.ns.cloudflare.com` |
| Tunnel | Cloudflare Tunnel | 域名 → Tunnel | `ssh` → `vps-proxy` |

本项目从阿里云 DNS 切到 Cloudflare DNS 就是为了利用后两种记录类型（Tunnel 类型是绕过 ISP 封锁的关键）。

## 关系
### → 指向
- [[DNS污染]] (DNS 被污染的具体机制)
- [[ISP封锁]] (DNS 污染是封锁的第一层)

### ← 被指向
- [[CDN]] (CDN 依赖 DNS 将用户引导到最近的节点)
- [[TLS-SSL]] (TLS 握手依赖 DNS 解析后的 IP)
