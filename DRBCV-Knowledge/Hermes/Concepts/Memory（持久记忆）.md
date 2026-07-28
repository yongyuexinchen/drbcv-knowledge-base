---
name: Memory（持久记忆）
type: system
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
---

# Memory（持久记忆）

## 类型判定
系统型 — Memory 是跨会话信息持久化的完整系统，由 MEMORY.md + USER.md + session_search + 外部 Provider 四个组件构成。

## 是什么
Hermes 的持久记忆系统让 Agent 在新会话中自动拥有历史上下文。核心是两个 Markdown 文件：`MEMORY.md`（Agent 笔记：环境、约定、经验）和 `USER.md`（用户画像：偏好、习惯、背景），每个会话开始时注入系统提示词。另有 `session_search`（FTS5 全文搜索历史会话）和 8 个可选外部记忆 Provider。

## 输入-输出空间
**输入**：Agent 调用 `memory(action="add")` 写入 → 持久化到 `~/.hermes/memories/`
**输出**：下一会话系统提示词自动包含记忆内容（当前会话不刷新）

## 正例（≥2个）
- Agent 记住"用户偏好 TypeScript > JavaScript"→ 下次生成代码自动用 TS
- Agent 记住"项目 Docker 用国内镜像源"→ 下次配 Docker 自动加上
- Agent 记住"博客发布到 github.com/yongyuexinchen/tech-blog"→ 下次写博客知道目标仓库

## 反例/边界（≥1个）
- 容量上限：MEMORY.md 2200 字符（约 800 tokens），超限拒绝写入 → Agent 必须合并/替换旧条目
- 不是"自动保存一切"：Agent 需要主动判断什么值得记、什么不值得
- 当前会话不刷新：写入后只在**下一会话**生效——这是为了保持 Prompt Cache 前缀稳定
- session_search ≠ Memory：Memory 是「永远要记住的稳定事实」，session_search 是「上次我们讨论的具体内容」

## 详细解释
记忆条目用 `§` 分隔。`memory` 工具的动作：`add`（添加）、`replace`（含 `old_text` 定位）、`remove`（含 `old_text` 定位）。`old_text` 做子串匹配，必须唯一定位 1 条。

**应该记**：用户偏好、环境事实、纠正、项目约定、显式要求。
**不应该记**：模糊信息、通用知识、代码/日志、临时状态、已在 SOUL.md/AGENTS.md 中的内容。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| MEMORY vs USER | MEMORY=Agent 笔记（环境/约定），USER=用户画像（偏好/习惯） |
| 分隔符 | 记忆条目用 ASCII 节号符号分隔 |
| 安全扫描 | 写入前检查提示词注入、凭证外泄、不可见字符 |
| 外部 Provider | 8 个可选：honcho, mem0, openviking, byterover, hindsight 等 |

### 记忆管理原则
- 应该记：用户偏好、环境事实、纠正、项目约定
- 不应该记：模糊信息、通用知识、代码/日志、临时状态
- 容量满时拒绝写入 → Agent 需合并/替换旧条目
- 写入后只在下一会话生效 → 保护 Prompt Cache 前缀


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — Memory 注入系统提示词

### ← 被指向
- [[Session Search（会话搜索）]] — 互补关系：Memory=稳定事实，Session Search=历史对话
- [[Profile（多实例）]] — 每个 Profile 有独立的 Memory