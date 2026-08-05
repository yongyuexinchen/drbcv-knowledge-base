---
name: Tool Calling
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-Agent
---

# Tool Calling（工具调用）

## 类型判定
判别型 — Agent 调用外部工具（搜索、数据库、API、代码执行器等）的能力，将 LLM 从「只能说话」扩展为「能做事」。

## 类比 ★
### 一句话比喻
Tool Calling 像给一个足不出户的书呆子配了一部智能手机——以前他只能凭脑子里的知识回答你，现在他能打开地图查路线、上点评网搜餐厅、用计算器算账、发微信找人帮忙。书呆子（LLM）还是那个书呆子，但有了手机（Tools），他能做的事翻了十倍。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| Tool Calling | 书呆子掏出手机——原来只靠脑力，现在能调用全世界的服务 |
| Function Definition（工具定义） | 手机上装好的 App——每个 App 有自己的功能和使用说明 |
| Tool Choice（LLM 选择调用哪个工具） | 书呆子判断「该用地图还是用计算器？」——根据当前问题选择 |

## 是什么
Tool Calling 是 LLM 调用预定义外部函数的能力。流程：① 定义工具的 JSON Schema（函数名、参数、描述）；② LLM 在生成过程中判断需要调用工具时，输出一个结构化的 function_call（而非自然语言）；③ 系统执行该函数，将结果返回给 LLM；④ LLM 基于工具结果继续推理或生成最终回复。在 AI 伴侣中，常用工具包括：搜索（获取实时信息）、记忆操作（读取/写入用户记忆）、日历操作、邮件发送等。

## 输入-输出空间
- **输入**: 工具定义（function schema） + 用户对话上下文
- **LLM 产出**: function_call `{name: "search_web", arguments: {query: "深圳天气"}}`
- **系统执行后返回**: function_result（JSON 或文本）
- **多轮模式**: LLM 可在一轮对话中多次调用工具（并行或串行）

## 正例（≥2 个）
1. **OpenAI Function Calling**: GPT-4 原生支持 function calling——定义工具 schema → LLM 决策调用 → 系统执行 → 结果返回 LLM
2. **AI 伴侣的「帮我查天气」**: 用户说「明天深圳天气怎样」→ LLM 输出 `get_weather(city:"深圳", date:"2026-07-24")` → 系统调用天气 API → LLM 解读结果回复用户

## 反例/边界（≥1 个）
1. **LLM 靠训练数据编造答案**: 用户问「今天天气」，LLM 不调用工具而是用训练数据瞎编——这是幻觉，不是 Tool Calling
2. **边界 — 工具调用失败**: API 超时或返回错误时，LLM 需要能优雅降级（如告知用户调用失败、重试、或用已有知识回答）——这需要 Reflection 机制配合

## 详细解释
Tool Calling 在 Agent 循环中的位置：

```
用户输入 → LLM 推理
              ↓
         需要外部信息？
         ↙        ↘
       是          否
        ↓           ↓
  输出 function_call   直接回复
        ↓
   系统执行工具
        ↓
   结果注入 Working Memory
        ↓
   LLM 再次推理（基于结果）
        ↓
   最终回复
```

关键设计考量：
- **工具粒度**: 太细（一个工具只做一件事）→ 调用次数多、延迟高；太粗 → 不够灵活
- **工具描述质量**: LLM 能否「正确选择」工具，80% 依赖工具描述写得好不好
- **安全边界**: 哪些工具有副作用（发邮件、扣款）需要用户确认，哪些可以自动执行

## 关系
### → 指向
- [[Function Calling]] — Function Calling 是 Tool Calling 在 LLM API 层面的技术实现
- [[Working Memory]] — 工具调用结果注入工作记忆供 LLM 继续推理
- [[AI Agent]] — Agent 通过 Tool Calling 与外部世界交互

### ← 被指向
- [[AI Agent]] — Tool Calling 是 Agent 实现自主行动的核心手段
- [[Planning]] — 规划步骤分解出的每个子任务最终通过 Tool Calling 执行
- [[Reflection]] — 反思机制通过检查工具调用结果来判断执行是否成功
