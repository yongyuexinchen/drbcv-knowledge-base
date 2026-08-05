---
name: Gateway（消息网关）
type: system
status: core
source: "[[Hermes教程-模块四-协作篇]]"
domain: hermes
---

# Gateway（消息网关）

## 类型判定
系统型 — Gateway 是 Hermes 的多平台消息接入与分发系统，把 Telegram/微信/Discord 等 23+ 平台统一接入 Agent。

## 是什么
Gateway 是 Hermes 的长期运行服务进程，负责：接收各消息平台的消息 → 维护每个聊天对应的会话 → 转发给 Hermes Agent Loop 处理 → 把回复发回原平台。同时运行 Cron 调度循环和 Kanban Dispatcher。

## 输入-输出空间
**输入**：Telegram/微信/Discord 用户消息
**输出**：Agent 处理后回复 → 发回对应平台

## 正例（≥2个）
- 微信接入：在微信里 @Hermes Bot → Gateway 收到 → Agent Loop 处理 → 回复到微信
- Telegram 审批：博客 reviewer block 了 task → Gateway 推送通知到 Telegram → 用户回复 `/kanban unblock` → Gateway 执行
- 多平台同步：用户从 Telegram 发指令「写博客」→ Gateway 处理 → 结果推送到 Telegram + Discord

## 反例/边界（≥1个）
- Gateway 和 CLI 用同一套 Hermes 引擎——配置、会话、记忆、技能全部共享
- Windows 上 Gateway 重启不能从内部触发（`hermes gateway restart` 拒绝自杀）
- 配对码 1 小时过期，有速率限制
- 跨平台不是「同一条消息发到所有平台」——每个平台独立维护会话

## 详细解释
支持的平台（23+）：Telegram、Discord、Slack、WhatsApp、微信、iMessage、Signal、Email、SMS、Matrix、Mattermost、Teams、LINE、SimpleX、ntfy、Google Chat、Home Assistant、DingTalk、Feishu、WeCom、QQBot、IRC、Yuanbao。

**配对安全**：默认拒绝所有未知用户 → 首次私信收到配对码 → 管理员 `hermes pairing approve` → 此后可自由对话。也可以配置 `ALLOWED_USERS` 列表。

## 细节备注

### 支持平台（23+）
Telegram · Discord · Slack · WhatsApp · 微信 · iMessage · Signal · Email · SMS · Matrix · Mattermost · Teams · LINE · SimpleX · ntfy · Google Chat · Home Assistant · DingTalk · Feishu · WeCom · QQBot · IRC · Yuanbao

### 配对安全
- 默认拒绝未知用户 → 首次私信收到配对码（Pairing code: XKGH5N7P）
- 配对码 1 小时过期 + 速率限制 + 加密随机数
- hermes pairing approve <platform> <code> → 永久有效

### Windows 限制
- hermes gateway restart 从内部调用被拒绝 → 需 taskkill + hermes gateway start


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — 消息转发到 Agent Loop 处理
- [[Session（会话）]] — 每个平台聊天对应一个 Session

### ← 被指向
- [[Cron（定时任务）]] (depends-on) — Cron 调度循环在 Gateway 内运行
- [[Dispatcher（调度器）]] (depends-on) — 默认在 Gateway 内运行
- [[Dashboard（管理面板）]] (depends-on) — 管理 Gateway 状态