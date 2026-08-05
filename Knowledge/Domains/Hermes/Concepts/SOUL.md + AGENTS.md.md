---
name: SOUL.md + AGENTS.md
type: discriminant
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
---

# SOUL.md + AGENTS.md

## 类型判定
判别型 — 区分 Agent 人格和项目规则的两种上下文文件：SOUL.md =「我是谁」，AGENTS.md =「这个项目怎么搞」。

## 是什么
两个都是 Hermes 自动加载的 Markdown 上下文文件，但职责完全不同：
- **SOUL.md**（`~/.hermes/SOUL.md`）：Agent 的身份/人格定义——语气、风格、沟通偏好、默认行为。注入到系统提示词开头。
- **AGENTS.md**（项目目录下）：项目规则——架构、约定、注意事项、构建命令。只在所属目录及子目录生效。兼容 Claude Code、Codex 等。

## 输入-输出空间
**输入**：对应目录下的 Markdown 文件 → 会话开始时自动加载
**输出**：内容注入 system prompt → 影响 Agent 的行为模式

## 正例（≥2个）
- SOUL.md：「你是技术专栏作者。开头用问题切入，代码示例必须可运行。」→ Writer Agent 每次写作都按这个风格
- AGENTS.md：「本项目用 uv 管理依赖，禁止 pip install。PR 前跑 pytest。」→ Agent 在项目目录下自动遵守
- .hermes.md：「博客 repo 的 Git 规范：commit message 用英文，分支名用 feature/xxx」→ Agent 在博客目录下自动遵守

## 反例/边界（≥1个）
- SOUL.md 不适合写项目规则（路径、仓库约定）——应该放 AGENTS.md
- AGENTS.md 不适合写人格（语气、风格）——应该放 SOUL.md
- AGENTS.md 有多个发现优先级：`.hermes.md` > `AGENTS.md` > `CLAUDE.md` > `.cursorrules`（只加载第一个匹配的）
- 安全扫描：包含「ignore previous instructions」等注入模式的上下文文件会被 BLOCKED
- 截断上限 20,000 字符：超长文件保留前 70% + 后 20%，中间截断

## 详细解释
上下文文件加载流程：
```
会话开始 → 扫描 cwd →
  1. 向上查 .hermes.md / HERMES.md（到 git root 为止）
  2. cwd 下的 AGENTS.md / CLAUDE.md / .cursorrules
  3. 安全扫描（注入检测）
  4. 截断（>20,000 字符）
  5. 注入系统提示词
```

`SOUL.md` 独立加载（不参与优先级竞争），始终从 `HERMES_HOME/SOUL.md` 读取。

`/personality` 命令可在 SOUL.md 之上追加一层临时人格覆盖（不修改 SOUL.md 本身）。

## 细节备注

### 安全扫描 7 类威胁
指令覆盖 · 欺骗行为 · 系统提示词覆盖 · 隐藏 HTML 注释 · 隐藏 div · 凭证外泄 · 不可见字符

### 上下文文件优先级链
```
.hermes.md  >  AGENTS.md  >  CLAUDE.md  >  .cursorrules
  (向上查到 git root)     (仅 cwd)
```
第一条匹配就停止，不会同时加载多种。

### SOUL.md 特殊规则
- 仅从 HERMES_HOME/SOUL.md 加载
- /personality 叠加临时人格（不修改文件本身）
- 内置 14 种人格：helpful、concise、technical、creative、teacher、kawaii、catgirl、pirate 等


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — 内容注入系统提示词
- [[Context Window（上下文窗口）]] — 占用上下文空间

### ← 被指向
- [[Profile（多实例）]] (depends-on) — 每个 Profile 有独立的 SOUL.md
- [[Memory（持久记忆）]] — 互补：SOUL.md=人格（长期稳定），Memory=事实（动态更新）