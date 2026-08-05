---
name: Hermes-Grok Integration（Hermes-Grok 集成）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: grok-build
---

# Hermes-Grok Integration（Hermes-Grok 集成）

## 类型判定
系统型 — 这是连接 Hermes（认知 OS）和 Grok Build（编码 Agent）的桥接层，定义了五条设计红线和完整的任务闭环。

## 是什么
Hermes-Grok 集成通过一个 Skill + Adapter 将 Grok 接入 Hermes 的 Agent 调度体系。Hermes 负责规划、下发验收标准、记忆回写；Grok 负责实际的编码执行。集成面是 Grok 的 Headless CLI，通过 subprocess 调用，**进程边界即架构边界**。

## 输入-输出空间
- **输入**：Hermes Planner 拆解的叶子编码任务（`task` + `workspace` + `constraints`）
- **输出**：envelope JSON（`ok`, `session_id`, `verification`, `memory_digest`）→ Hermes 写 Memory

## 正例（≥2个）
1. **完整闭环**：用户"写 RAG demo" → Planner→Router→grok-build Skill→Adapter→Grok CLI→返回 JSON→git diff 核验→Memory 写入
2. **降级**：Grok 不可用 → doctor 探测失败 → 回退 codex/claude-code Skill

## 反例/边界（≥1个）
- ❌ 不链接 Grok Rust crate（只 subprocess）
- ❌ 不开 Grok Memory（`GROK_MEMORY=0` 硬编码）
- ❌ 不下发"做一个系统"（只给叶子任务）
- ❌ 不信 Grok 自述（以 git diff 核验）

## 详细解释
```
Hermes 收到任务
  │
  ▼
Planner: "这是编码任务，拆为: ①建文件 ②写代码 ③跑测试"
  │
  ▼
Skill Router: 匹配 grok-build Skill → 加载 SKILL.md
  │
  ▼
Agent 按范式调用:
  terminal("python grok_adapter.py run --task '...' --workdir E:/project --policy guarded")
  │
  ▼ (subprocess)
grok -m deepseek-v4 -p "任务书" --yolo --output-format json --cwd E:/project
  │
  ▼ (Grok 内部: goal_planner → 工具循环 → 改文件 → 跑测试)
stdout JSON: {"ok":true, "sessionId":"...", "verification":{...}}
  │
  ▼
Adapter 后处理: git diff 核验 → 组装 envelope
  │
  ▼
Hermes: 汇报用户 + memory("RAG demo 已完成，FAISS+3 测试通过")
```

## 细节备注

### 五条设计红线
| # | 红线 | 落实 |
|---|---|---|
| 1 | Core 不依赖 Grok | Skill 目录可整体删除 |
| 2 | 进程边界 | subprocess，不 link Rust crate |
| 3 | 记忆主权 | GROK_MEMORY=0 硬编码在 adapter |
| 4 | 规划主权 | 只下发叶子任务，--max-turns=30 |
| 5 | git 核验 | verification 字段来自 git，非 LLM 自述 |

### 策略三档
| 档位 | Grok 旗标 |
|------|----------|
| readonly | `--tools "read_file,grep,list_dir"` |
| guarded | `--allow "Edit(**)" --deny "Bash(rm -rf*)"` |
| auto | `--yolo` |

### 文件位置
```
~/.hermes/skills/autonomous-ai-agents/grok-build/
├── SKILL.md          ← Agent 读的调用范式
├── config.yaml       ← 策略映射
└── scripts/
    └── grok_adapter.py   ← doctor / run / resume
```

## 个人见解
> 这个集成方案的核心不是"接一个工具"，而是定义了 Hermes 的"执行器接口"。未来换 Codex/Claude Code/任何编码 Agent，只要实现同样的 adapter 接口就行。这是操作系统的"驱动模型"。
>
> （填写你的理解）

## 关系
### 依赖 (depends-on)
- [[Hermes Architecture（核心架构）]] — Hermes 的 Planner + Router 触发集成
- [[Grok Build Overview（Grok Build 总览）]] — 被集成方
- [[Headless Mode（无头模式）]] — 集成面
- [[Custom Models（自定义模型）]] — 零成本运行的关键

### ← 被指向
- [[Planner（任务规划器）]] — 把编码任务路由到本集成
- [[Skill Router（技能路由）]] — 加载 grok-build Skill
