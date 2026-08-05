---
name: SNI
type: discriminant
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# SNI（服务器名称指示）

## 类型判定
判别 — TLS 握手中的明文字段，告诉服务器客户端想访问哪个域名。是 GFW 深度包检测（DPI）最常用的封锁手段——因为它是 TLS 加密通信中唯一明文暴露的域名信息。

## 类比 ★
### 一句话比喻
SNI = 你进一栋有很多公司的写字楼，门口保安问你："找哪家公司？"你必须说出来（明文），保安才能告诉你电梯去几楼。但你说出来的那一刻——全大厅的人（GFW）都知道你要去哪家公司了。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| TLS 加密通信 | 进入大楼后的加密对话——没人能偷听 |
| SNI 明文 | 进门前必须对保安说出的公司名 |
| GFW 监听 SNI | 大厅里站着的便衣——记下所有访客的目的地 |
| ECH (加密 SNI) | 提前办好加密访客证——保安不用问也能让进 |

## 是什么
SNI 是 TLS 握手 ClientHello 中的一个扩展字段。因为一台服务器可能托管多个 HTTPS 网站（同一个 IP 不同域名），服务器需要 SNI 来知道应该用哪个证书。SNI 在 TLS 1.3 中是唯一必须明文传输的域名信息。

## 正例
1. **Cloudflare 自动处理 SNI**：`vps.yongyuexinchen.xin` 的证书由 Cloudflare 管理，SNI 匹配正确，TLS 握手正常。
2. **Hysteria2 伪装 SNI**：Hysteria2 配置 `sni=www.microsoft.com`——GFW 看到 SNI 是微软，以为是正常 HTTPS 流量，实际是代理。

## 反例/边界
1. **GFW 通过 SNI 封锁特定域名**：即使 DNS 返回真实 IP，GFW 在 TLS 握手阶段看到 SNI=`google.com`，可以直接 RST 阻断连接——这就是为什么 DNS 正确有时候仍然打不开。
2. **SNI 明文是 TLS 1.3 的历史遗留**：ECH（Encrypted Client Hello，加密 SNI）已标准化但尚未广泛部署。在 ECH 普及前，SNI 是 GFW 最主要的检测手段。
3. **CDN 和 Tunnel 隐藏了真实 SNI**：通过 Cloudflare，GFW 看到的 SNI 是 `vps.yongyuexinchen.xin`（一个正常域名），而非 `google.com`——这就是为什么走 CDN/Tunnel 能绕过 SNI 检测。

## 详细解释
SNI 在本项目两次出现：
```
1. Hysteria2 伪装:
   客户端 → SNI=www.microsoft.com → VPS
   GFW 看到：有人在访问微软官网（正常流量）
   实际：Hysteria2 代理数据

2. Cloudflare Tunnel:
   V2RayN → SNI=vps.yongyuexinchen.xin → Cloudflare
   GFW 看到：访问一个普通个人域名
   实际：代理流量，Cloudflare 再转发到 VPS
```

两个方案都避免了 SNI=`google.com` 出现在明文中——只要 SNI 不触发 GFW 的黑名单，TLS 握手就能完成。

## 关系
### → 指向
- [[TLS-SSL]] (SNI 是 TLS 握手的扩展字段)
- [[CDN]] (CDN 通过 SNI 路由到不同源站)

### ← 被指向
- [[DNS污染]] (SNI 封锁是 DNS 污染之后的第二道防线)
