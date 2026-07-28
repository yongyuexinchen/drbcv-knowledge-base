# AI应用开发工程师 —— 典型一天工作画像

> 基于深圳 70 条真实 Boss 直聘 AI 应用开发岗 JD 提炼
> 不是笼统描述，而是具体到「你会打开什么工具、写什么代码、和谁开会」

---

## ☀️ 上午 9:00-12:00：效果优化 & 模型调优

### 9:00—站会 & 看板
- 打开 Jira/飞书多维表格，回顾昨天卡住的 issue
- 和产品经理对一遍今天要上的功能点：「昨天那个 Agent 的工具调用顺序对了吗？」

### 9:30—Prompt 效果调优
- 打开你常用的 LLM Playground（公司自建的或 LangSmith），跑一组 Prompt 对比实验
- 昨天产品反馈「用户问"帮我查上周的订单"时，Agent 老去查知识库而不是调 SQL 工具」
  → 你会：修改 System Prompt 里的工具选择规则，加一条「涉及时间+数据查询时优先 SQL 工具」
  → 跑 20 条测试 case，确认准确率从 73% 提到 91%
- 工具：Python + LangChain/LlamaIndex + 公司内部的 Prompt 管理平台

### 10:30—RAG 召回率排查
- 打开 Grafana 看板，发现某个知识库的召回率从昨天的 85% 掉到 72%
- 你会：拉最近新增的文档切片日志 → 发现新文档的 chunk size 异常大
  → 改文档解析 pipeline 的分块策略 → 重新入库 → 跑 Ragas 评测
- 工具：Python + 向量数据库（Milvus/Weaviate）+ Ragas 评测框架

---

## 🌤 下午 13:30-18:00：功能开发 & 联调

### 13:30—Agent 逻辑开发
- 接到需求：「让 Agent 支持多轮对话中的上下文纠正」
  → 比如用户说"不对，我说的是上周三不是上周二"→ Agent 要能理解并修正参数
- 你会：设计对话状态管理的数据结构 → 实现一个 ContextRevisionHandler
  → 写单元测试 → 在开发环境跑一遍完整对话流
- 工具：Python + FastAPI + LangGraph（状态机编排）+ Pytest

### 15:00—API 联调
- 和后端/前端在测试环境联调新接口
- 你会：确认 API 返回结构、处理异常情况（模型超时返回什么？Token 超限怎么降级？）
- 用 Postman/curl 调接口 → 看日志 → 修 bug

### 16:00—模型路由 & 成本优化
- 检查昨天的 API 调用成本报表（OpenAI / Claude / 国内模型各花了多少）
- 你会：调整模型路由策略 → 简单问答切到便宜模型（DeepSeek/通义千问）
  → 复杂推理保留贵模型（Claude）→ 预期月省 30% 成本
- 代码提交 → PR → 等 Code Review

---

## 🌙 晚上 19:00-21:00（不强制，但常见）

### 19:00—技术方案文档
- 写明天要评审的技术方案：「多 Agent 协作架构设计」
- 画架构图 → 列技术选型对比 → 写接口定义 → 评估风险点
- 工具：Notion/飞书文档 + Draw.io/Excalidraw

### 20:00—Code Review
- 评审同事的 PR：「RAG 检索模块重构」
- 关注： 切片逻辑有没有边界 case？ 向量维度切换后兼容吗？ 有没有性能回退？

### 20:30—学习 & 实验
- 刷一下 Arxiv/Hugging Face/X 上今天有什么新东西
- 试着跑一下最近很火的 MCP 协议 demo，看能不能用到项目里
- 或者：黑马程序员 AI 大模型课看一节（你正在跟的阶段四）

---

## 🔧 你的工具箱（真的每天都要用）

| 层级 | 工具/技能 | 频率 |
|------|----------|------|
| **写代码** | Python（绝对主力）, FastAPI/Flask | 每天 |
| **Prompt 调试** | LangSmith, 公司自建平台, OpenAI Playground | 每天 |
| **向量/RAG** | Milvus/Weaviate/Chroma, 文档解析, 切片策略 | 每周 3-4 次 |
| **Agent 框架** | LangChain, LangGraph, LlamaIndex, CrewAI | 每周 3-4 次 |
| **模型接口** | OpenAI API, Anthropic API, 国内模型 API | 每天 |
| **评测** | Ragas, 自建测试集, A/B 实验 | 每周 2-3 次 |
| **部署/容器** | Docker, K8s（看公司规模） | 有发布时 |
| **查文档** | 官方文档, GitHub Issues, 技术博客 | 每天无数次 |

---

## 💡 一句话总结

> 「你不是在训模型，你是在**把模型用起来**——让它能查知识库、调 API、理解上下文、不出错。
> 你的核心技能是：Python + Prompt Engineering + RAG + Agent 编排。」
