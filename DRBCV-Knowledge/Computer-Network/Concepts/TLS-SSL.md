---
name: TLS-SSL
type: discriminant
status: core
source: "[[自建代理基础概念]]"
domain: Computer-Network
---

# TLS/SSL（传输层安全协议）

## 类型判定
判别 — 互联网加密通信的标准。HTTPS 中的 "S" 就是 TLS。浏览器地址栏的🔒图标表示连接已加密。

## 类比 ★
### 一句话比喻
TLS = 你和收信人约定好的一套"秘密握手+密码本"。握手阶段：先确认对方是本人（证书验证），再商量用什么暗号（加密算法），最后交换一次性密码（会话密钥）。之后所有通信都用这个一次性密码加密——就算邮递员偷看也看不懂。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| TLS 握手（证书验证+密钥协商） | 接头暗号："天王盖地虎"+"宝塔镇河妖" |
| 会话密钥 | 确认身份后约定的一次性暗号 |
| 证书（由 CA 签发） | 公安局发的身份证——第三方担保身份 |
| 自签名证书（自己签发） | 自己手写的身份证——没人信 |

## 是什么
TLS 在 TCP 连接建立后、应用数据发送前进行握手。握手完成三件事：①验证服务器身份（证书）②协商加密算法 ③生成会话密钥。之后所有数据用对称加密传输。TLS 1.3 将握手从 2-RTT 缩短到 1-RTT。

## 正例
1. **Cloudflare 提供的免费证书**：`vps.yongyuexinchen.xin` 的 HTTPS ——浏览器看到的是 Cloudflare 签发的正规证书，🔒正常。
2. **V2RayN 走 Cloudflare TLS**：V2RayN 连 `vps.yongyuexinchen.xin:443`，Cloudflare 边缘做 TLS 终止，证书合法 → 不报错。

## 反例/边界
1. **Xray 自签名证书**：Xray 直连 VPS:443 时报 `x509: certificate signed by unknown authority`——因为 Xray 用的是自己签发的证书，不是 CA 签发的。
2. **Xray 26.x 废弃 allowInsecure**：旧版本可以通过 `allowInsecure=true` 跳过证书验证，26.x 版本删除了这个选项，必须用正规证书或 pinnedPeerCertSha256。
3. **TLS 不防深度包检测**：GFW 能看到 TLS 握手中的 SNI 字段（目标域名明文），即使流量加密，GFW 也知道你在访问哪个网站。

## 详细解释
TLS 握手在本次项目中的两处关键应用：

1. **Cloudflare 场景**（正常）：
```
V2RayN ──→ Cloudflare (正规 TLS 证书) ──→ VPS Xray (内部 HTTP，无 TLS)
```
Cloudflare 处理所有 TLS，内部走明文。V2RayN 不报证书错误。

2. **直连场景**（证书错误）：
```
V2RayN ──→ VPS Xray (自签名证书，无 CA 认证)
```
V2RayN 不信任自签名证书 → 报 `x509: unknown authority`。

## 关系
### → 指向
- [[证书与自签名证书]] (证书是 TLS 的核心组件)
- [[SNI]] (TLS 握手中的明文字段——GFW 的检测点)

### ← 被指向
- [[HTTPS]] (HTTPS = HTTP + TLS)
- [[CDN]] (CDN 通常做 TLS 终止)
