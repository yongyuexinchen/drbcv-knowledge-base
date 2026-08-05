---
name: Session Management（会话管理）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: grok-build
---

# Session Management（会话管理）

## 类型判定
系统型 — Session 是 Grok 的有状态执行单元，支持跨调用续接和多轮迭代修复。

## 是什么
Grok 每次 headless 调用绑定一个 UUID session。session 持久化在 SQLite journal 中，记录完整的对话历史、工具调用、文件改动。`--resume` 可续接历史上下文，`-c` 可继续最近会话。**这对 Hermes 的"多轮修复循环"至关重要。**

## 输入-输出空间
- **输入**：`--resume <session_id>` 或 `-c`（继续最近）
- **输出**：新轮次追加到既有 session，Grok 记得之前的代码和项目结构

## 正例（≥2个）
1. **多轮修复**：第一轮写代码 → 第二轮 `--resume` 修 bug → 第三轮加测试
2. **Hermes 场景**：第一次 `run` 拿到 `sessionId` → 验收不通过 → `resume` "测试第 3 条失败，修复"

## 反例/边界（≥1个）
- `-s` 只创建新 session（UUID），不续接——续接用 `-r` 或 `-c`
- `--fork-session`：从旧 session 分叉出新 session，不污染原历史
- session 目录：`~/.grok/sessions/<id>/`
- 过期策略：自动清理（可配），不是永久保留

## 详细解释
Session 生命周期：
```
创建         续接            结束
grok -p       grok -p          grok 进程退出
  │         --resume <id>        │
  ▼              │               ▼
新 UUID     追加到此 session   stopReason 写入
               │
          Grok 记得之前
          的上下文/代码
```

## 细节备注

### 与 Hermes session_search 的关系
| 维度 | Grok Session | Hermes Session |
|------|-------------|----------------|
| 存储 | SQLite journal | SQLite session DB |
| 持久性 | 同项目可续接 | 跨项目搜索 |
| 记忆注入 | 不开（GROK_MEMORY=0） | Memory + Obsidian |

Adapter 负责桥接：拿到 Grok 的 `sessionId` → 留存于 Hermes 对话中 → 下次 `resume` 时传入。

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Goal Orchestration（目标编排）]] — 编排过程记录在 session 中

### ← 被指向
- [[Headless Mode（无头模式）]] — `--resume` 是 headless 旗标
- [[Hermes-Grok Integration（Hermes-Grok 集成）]] — Adapter 管理 sessionId
