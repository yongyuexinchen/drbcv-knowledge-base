---
name: Cron（定时任务）
type: system
status: core
source: "[[Hermes教程-模块三-进化篇]]"
domain: hermes
---

# Cron（定时任务）

## 类型判定
系统型 — Cron 是 Hermes 的定时任务系统，支持自然语言调度 + cron 表达式 + 作业链 + 无 Agent 脚本。

## 是什么
Hermes 内置的定时任务调度器，在 Gateway 内每 60 秒 tick 一次，到期的任务启动新 Agent 会话执行 prompt。支持四种调度格式、多平台投递、`context_from` 作业链、No-Agent 纯脚本模式。

## 输入-输出空间
**输入**：`cronjob(action="create", schedule="every 1d at 09:00", prompt="...", deliver="telegram")`
**输出**：到期时启动 Agent → 最终回复投递到指定平台

## 正例（≥2个）
- 博客选题流水线：Job1 收集新闻 → Job2 筛选选题 → Job3 生成简报（context_from 链）
- 每日 AI 摘要：`schedule="0 9 * * *"` 每天早上 9 点跑
- 站点健康监控：No-Agent script 每 30 分钟 curl 博客站点 → 挂了才发告警

## 反例/边界（≥1个）
- Cron 运行时不加载 cron 管理工具——防止递归创建无限定时任务
- `context_from` 读的是上游**最近一次已完成**输出，不等待同一 tick 的并行任务
- No-Agent 模式脚本放在 `~/.hermes/scripts/`，超时默认 120s
- `[SILENT]` 开头 → 成功静默不投递（失败仍投递）

## 详细解释
四种调度格式：
| 格式 | 示例 | 行为 |
|------|------|------|
| 相对延迟 | `30m` | 一次性，30 分钟后 |
| 循环间隔 | `every 2h` | 每 2 小时 |
| Cron 表达式 | `0 9 * * 1-5` | 工作日 9:00 |
| ISO 时间 | `2026-03-15T09:00:00` | 指定时刻一次 |

`deliver` 投递：`origin`（来源平台）、`local`（只存文件）、`telegram`、`discord`、`all`、组合如 `telegram,discord`。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| [SILENT] 静默 | 回复以 [SILENT] 开头 → 成功时抑制投递，失败仍投递 |
| No-Agent | 纯脚本不走 LLM → 零 token 费用 |
| job output | ~/.hermes/cron/output/{job_id}/{timestamp}.md |

### 调度格式
| 格式 | 示例 | 行为 |
|------|------|------|
| 相对延迟 | 30m | 一次性 |
| 循环间隔 | every 2h | 持续重复 |
| Cron 表达式 | 0 9 * * 1-5 | 工作日 9:00 |
| ISO 时间戳 | 2026-03-15T09:00:00 | 指定时刻一次 |

### context_from 注意
读上游最近一次已完成输出 → 不等待同一 tick 的并行任务


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Gateway（消息网关）]] — Cron 调度循环在 Gateway 内运行
- [[Agent Loop（Agent 循环）]] — 到期启动新 Agent 会话

### ← 被指向
- [[Kanban Board（任务看板）]] — Cron 可以创建 Kanban Task