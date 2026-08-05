---
name: Agent Loop（Agent 循环）
type: system
status: core
source: "[[Hermes教程-模块五-实战篇]]"
domain: hermes
---

# Agent Loop（Agent 循环）

## 类型判定
系统型 — 它是 Agent 的核心运行时引擎，组织 prompt→LLM→tool→result 四个阶段的循环。

## 是什么
Agent Loop 是 Hermes 的基本执行单元。每一轮：构建系统提示词 → 调用 LLM → 如果 LLM 返回 tool_calls 则执行工具 → 工具结果注入对话 → 再次调用 LLM → 直到 LLM 返回纯文本（不再调用工具）或达到 `max_turns` 上限。

## 输入-输出空间
**输入**：用户消息 + 系统提示词（SOUL.md + Memory + Skills + Tools schema + 项目上下文） + 历史对话
**输出**：最终文本回复（或 `max_turns` 耗尽后的最后状态）

## 正例（≥2个）
- 用户说"帮我查今天天气"→ Hermes 在 Agent Loop 中：调用 web_search → 拿到结果 → 组织回复
- 用户说"写一篇博客"→ Gateway 收到 → Agent Loop 中创建 Kanban task → 返回"已创建任务"（不再执行具体写作）
- 用户说"你好"→ 一次 LLM 调用就够了，不需要工具 → 直接返回

## 反例/边界（≥1个）
- `max_turns: 90`（默认）→ 最多 90 轮 tool call 循环，超过强制终止
- 上下文压缩触发时（prompt 达窗口 50%）→ 自动压缩历史，保持循环继续
- Tool call 失败 → 错误信息注入对话 → LLM 重试或承认失败
- delegate_task 子 Agent 有自己的独立 Agent Loop，不共享父 Agent 的上下文

## 详细解释
伪代码：
```
while turns < max_turns:
    response = LLM.chat(messages, tools)
    if response has no tool_calls:
        return response.content         # 结束
    for each tool_call:
        result = execute_tool(tool_call)
        messages.append(tool_result)
    turns++
```

`max_turns` 的设计目的是防止 Agent 陷入无限循环（调用工具 → 不满意 → 再调用 → 再不满意......）。实际上大多数任务 5-15 轮就完成了。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| max_turns | 默认 90；大多数任务 5-15 轮完成 |
| 工具并行执行 | 同一轮互不依赖的 tool_call 自动并行（最多 8 worker） |
| Checkpoints | 开启后每次写入文件自动创建快照 → /rollback [N] 恢复 |

### 终止条件
1. LLM 返回纯文本（无 tool_calls）→ 正常结束
2. 达到 max_turns → 强制终止
3. 上下文压缩触发（达窗口 50%）→ 自动压缩后继续
4. 用户 /stop → 立即终止

### 设计约束
- 中间不改变工具定义 → 保护 Prompt Cache 前缀
- 中间不改变 system prompt 结构 → 同上


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Provider（模型提供商）]] — LLM 调用走 Provider
- [[Tool／Toolset（工具集）]] — 工具调用在此循环中执行
- [[Context Window（上下文窗口）]] — 上下文容量约束循环的长度
- [[Prompt Cache（提示词缓存）]] — 稳定的系统提示词前缀让缓存持续命中

### ← 被指向
- [[Delegation（任务委派）]] (depends-on) — 子 Agent 有自己的 Agent Loop
- [[Kanban Board（任务看板）]] (depends-on) — Worker 启动后进入独立的 Agent Loop