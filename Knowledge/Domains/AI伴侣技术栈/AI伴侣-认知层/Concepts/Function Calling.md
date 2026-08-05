---
name: Function Calling
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-认知层
---

# Function Calling

## 类型判定
判别型 — LLM 从「说话」升级为「做事」的机制，AI Agent 的「手」。

## 类比 ★
### 一句话比喻
Function Calling 像给实习生配了一台万能遥控器——你跟他说「把空调调到 26 度」，他不再只是说「好的，建议您把空调调到 26 度」，而是直接拿起遥控器按了下去。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 工具定义（Tool Schema） | 遥控器上的按钮说明——每个按钮叫什么、按了有什么用、需要什么参数 |
| LLM 决定调用哪个工具 | 实习生听完你的话，自己判断「需要按空调遥控器上的温度按钮」 |
| 工具执行结果返回 LLM | 实习生按完遥控器回来报告「已经调到 26 度了」，你再给下一步指示 |

## 是什么
Function Calling 是 LLM 的一项能力：给定一组工具（Function）的定义（名称、描述、参数 JSON Schema），LLM 在推理过程中判断「这个问题需要调用哪个工具、传什么参数」，输出结构化的函数调用请求而非自然语言。外部系统执行该函数，将结果返回给 LLM，LLM 再基于结果生成最终回答。这是 AI Agent 的基础——让 LLM 从纯文本生成器变成可以操作外部世界的智能体。

## 输入-输出空间
- **输入**: 用户消息 + 工具定义列表（name, description, parameters JSON Schema）
- **LLM 输出（二选一）**: ① 普通文本回复 ② 函数调用请求（function_name + JSON arguments）
- **外部执行后**: 函数返回结果再次输入 LLM，LLM 基于结果生成最终回复

## 正例（≥2 个）
1. **AI 伴侣查天气**: 用户「明天杭州天气怎么样」→ LLM 输出 `call get_weather(city="杭州", date="明天")` → 外部执行 → 返回「晴, 25°C」 → LLM：「明天杭州晴天，25°C，适合出门哦～」
2. **AI 伴侣管理日程**: 用户「帮我约明天下午 3 点开会」→ LLM 调用 `create_event(title="开会", time="明天15:00")` → 日历创建成功 → LLM：「已帮你约好了，需要我提前提醒你吗？」

## 反例/边界（≥1 个）
1. **纯文本 LLM（无工具）**: 用户问天气，LLM 只能回答「抱歉我不知道，建议您打开天气 App」——不是 Function Calling，是文字建议
2. **边界 — 工具幻觉**: LLM 可能调用不存在的工具，或传错误的参数格式——需要严格的 Schema 校验和错误处理

## 详细解释
Function Calling 的完整流程：
```
用户: 「明天杭州天气？」

LLM推理: 这需要调用 get_weather 工具
  → 输出: {function: "get_weather", arguments: {city: "杭州", date: "2026-07-24"}}
  
外部系统: 调用天气 API → 返回 {weather: "晴", temp: 25}

再次调用 LLM:
  System: 用户问天气
  工具返回: {weather: "晴", temp: 25}
  
LLM: 「明天杭州晴天，25°C，天气不错哦，要出去走走吗？」
```

在 AI 伴侣中，Function Calling 是 Agent 的基石：
```
用户消息
  → LLM 判断：闲聊？or 需要做事？
  → 做事：调用工具（查天气/设提醒/搜记忆/控制智能家居）
  → 工具返回结果
  → LLM 整合生成自然回复
```

## 关系
### → 指向
- [[LLM]] — Function Calling 是 LLM 的高级能力，依赖模型对工具定义的理解
- [[Prompt Engineering]] — 工具定义的描述质量直接影响 LLM 调用准确率
- [[REST API]] — 外部工具通常以 REST API 形式暴露，Function Calling 调用它们

### ← 被指向
- [[AI Agent]] — Agent 的核心就是「LLM + Function Calling + 循环决策」
- [[RAG]] — 检索也可以封装为一个 Tool（`search_knowledge_base`），LLM 通过 Function Calling 触发检索
