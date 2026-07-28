---
name: Skill（技能系统）
type: system
status: core
source: "[[Hermes教程-模块三-进化篇]]"
domain: hermes
---

# Skill（技能系统）

## 类型判定
系统型 — Skill 是 Hermes 的自进化机制，由创建、加载、维护（Curator）三个阶段组成完整生命周期。

## 是什么
Skill 是 Hermes 的可复用工作流程，存储在人类可读的 `SKILL.md` 文件中。Agent 解决复杂问题后可以自动创建 Skill，下次遇到类似任务时自动加载。这是 Hermes 区别于其他 Agent 框架的核心能力——**越用越聪明**。

## 输入-输出空间
**输入**：一个复杂任务成功完成 → Agent 调用 `skill_manage(action="create")` → 沉淀为 SKILL.md
**输出**：下次相似任务 → 系统提示词自动注入 Skill 内容 → Agent 按照 Skill 中的步骤执行

## 正例（≥2个）
- `blog-kanban-workflow`：博客创作流程 Skill，定义 orchestrator→researcher→writer→reviewer→publisher 的标准流水线
- `hermes-custom-provider`：配置中转站的 Skill，含完整 YAML 模板 + 常见坑点
- Agent 自动沉淀：安装 Docker 遇到 3 个坑 → 成功后创建 `docker-windows-pitfalls` Skill → 下次装 Docker 自动避开

## 反例/边界（≥1个）
- Skill 是 Markdown 文件，人能直接编辑——不是黑盒
- 内置 Skill + Hub Skill 不会被 Curator 自动归档——只有 Agent 自己创建的会被管理
- 不是每次任务都建 Skill——简单一次性的任务不建，只有「有复用价值的复杂任务」才沉淀
- Skill 加载会改变 system prompt → 可能破坏 Prompt Cache 前缀

## 详细解释
Skill 目录结构：
```
~/.hermes/skills/
├── blog-kanban-workflow/SKILL.md    ← 主文件（含 YAML frontmatter）
├── hermes-custom-provider/
│   ├── SKILL.md
│   └── templates/
│       └── siliconflow-config.yaml   ← 可选模板
```

`skill_manage` 的四个核心动作：`create`（新建）、`patch`（小修）、`edit`（重写）、`delete`（删除）。Agent 优先用 `patch` 而非 `edit`，避免覆盖用户手动修改。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| Conditional Activation | Skill 根据工具可用性自动显示/隐藏 |
| Platform-Specific | frontmatter 中 platforms: [linux, macos] → Windows 上不显示 |
| Skill Bundles | v0.15+：多个 Skill 绑定为一个斜杠命令 |
| external_dirs | 团队共享技能目录 → 只读扫描，本地优先 |

### 使用原则
- Skill 加载改变 system prompt → 首次加载导致一次 cache miss → 后续稳定
- Agent 建 Skill 优先用 patch 而非 edit
- 只有「有复用价值的复杂流程」才值得沉淀


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — Skill 在系统提示词中注入
- [[Curator（技能维护）]] — Curator 管理 Agent 自建 Skill 的生命周期

### ← 被指向
- [[Prompt Cache（提示词缓存）]] (depends-on) — Skill 加载改变 system prompt，可能破坏缓存
- [[Profile（多实例）]] (depends-on) — 不同 Profile 可有不同的 Skill 集