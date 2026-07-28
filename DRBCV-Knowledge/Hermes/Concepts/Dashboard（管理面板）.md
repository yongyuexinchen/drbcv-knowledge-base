---
name: Dashboard（管理面板）
type: system
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
---

# Dashboard（管理面板）

## 类型判定
系统型 — Dashboard 是 Hermes 的 Web 图形化管理界面，替代 YAML 和 CLI 进行配置管理、状态监控。

## 是什么
Hermes Dashboard 是一个基于浏览器的 Web 管理面板（`http://127.0.0.1:9119`），提供：消息渠道配置（Telegram/Discord/微信）、MCP 目录浏览与配置、凭证管理（`.env` + `auth.json` 可视化编辑）、Webhooks 配置、Gateway 状态监控、内嵌 Chat 终端（`--tui` 模式）。v0.16 支持完整中文界面。

## 输入-输出空间
**输入**：浏览器访问 `http://localhost:9119`
**输出**：图形化配置界面 → 修改实时写入 config.yaml / .env

## 正例（≥2个）
- 配置微信接入：Dashboard 里填 WEIXIN_ACCOUNT_ID → 自动写入 .env → Gateway 重启后生效
- 监控 Kanban Board：Dashboard 里看各 Profile 的任务负载、调度日志
- MCP 目录浏览：Dashboard 里搜 GitHub MCP Server → 一键安装

## 反例/边界（≥1个）
- Dashboard 需要 OAuth/Token 认证——不是任意局域网用户都能访问
- 不是所有配置都能在 Dashboard 改——复杂的 custom_providers 块仍需手动编辑
- `--tui` 参数启用内嵌 Chat 标签页，默认只有管理界面

## 详细解释
```bash
hermes dashboard                    # 启动，自动打开浏览器
hermes dashboard --port 8080        # 自定义端口
hermes dashboard --tui              # 启用内嵌 Chat
hermes dashboard --status           # 查看运行状态
hermes dashboard &>/dev/null &      # 后台运行
```

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| 内嵌 Chat | --tui → 浏览器内嵌 Hermes 聊天终端 |
| 中文界面 | v0.16 正式支持 |
| Remote Gateway | 桌面应用通过 OAuth 连接云服务器 Gateway |

### 启动参数
```bash
hermes dashboard              # 默认 9119，自动打开浏览器
hermes dashboard --port 8080  # 自定义端口
hermes dashboard --tui        # 启用内嵌 Chat
hermes dashboard &>/dev/null &  # 后台运行
```


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Gateway（消息网关）]] — 监控 Gateway 状态
- [[Kanban Board（任务看板）]] — 监控 Board 进度

### ← 被指向
- [[Config.yaml]] (implements) — Dashboard 是 config.yaml 的图形化编辑器