# 优化后的12周 AI 应用开发工程师学习路线图

> 面向：Python 初学者（会用 ChatGPT 写代码，但无法独立开发）
> 目标：2026年10月底投递深圳 AI 应用开发工程师
> 目标薪资：**20-25K**（对应深圳1-3年经验AI应用开发岗的中位薪资，数据来源：方向A的70条JD分析）
> 参考：深圳AI应用开发岗 中位22K，P25-P75: 16K-38K；经验不限岗中位38K
> 更新：2026-07-27

---

## 修正摘要：当前路径 vs 优化路径

```
你的原计划：
  Docker → Java基础 → AI伴侣项目

优化后：
  [第1-4周] Docker + Prompt工程 + RAG全流程项目
  → [第5-8周] Agent编排 + API工程化 + 企业级RAG
  → [第9-12周] AI伴侣MVP + MCP + 面试冲刺

核心修正：
  ❌ Java基础 → 删除（AI原生岗不需要，3个月也学不到面试水平）
  ❌ AI伴侣作为唯一项目 → 改为3个递增难度的项目
  ✅ 新增 Prompt工程 + RAG + Agent + API工程化
```

---

## 阶段一：地基搭建（第1-4周）
### 目标：能独立搭建一个 RAG 问答系统

> ⚠️ 黑马V6.5预计8月开课（第3周左右）。黑马讲RAG时你已经在做独立RAG项目，互为补充。

### 第1周：Docker 收尾 + Prompt Engineering

| 日期 | 学什么 | 做什么 | 产出 |
|------|--------|--------|------|
| Day 1-2 | Docker Compose 多容器编排 | 用 Compose 起一个 FastAPI + PostgreSQL 双容器 | `docker-compose.yml`（保存到GitHub） |
| Day 3-4 | Prompt 工程基础：角色设定、Few-shot、Chain-of-Thought | 写10个不同场景的 Prompt 模板（分类/摘要/问答/代码/翻译） | `prompts/` 目录下的模板库 |
| Day 5-6 | Prompt 版本管理：模板化 + 变量注入 + A/B测试 | 用 Python 实现一个 PromptManager 类（加载模板、填充变量、调用LLM） | `prompt_manager.py` |
| Day 7 | 本周回顾 | 用 FastAPI 包装 PromptManager 成一个 API | `POST /prompt/generate` |

**里程碑1**：`curl -X POST http://localhost:8000/prompt/generate -d '{"template":"qa","question":"什么是RAG"}'` 返回 LLM 回复。

**每天手写代码**：至少 200 行 Python（不准用 AI 辅助），从 Day 1 就开始。

---

### 第2周：向量数据库 + 文档解析

| 日期 | 学什么 | 做什么 | 产出 |
|------|--------|--------|------|
| Day 1-2 | 向量嵌入原理（不用手写，理解即可）：Embedding 是什么、余弦相似度 | 调用 DeepSeek Embedding API，把10篇文档向量化 | `embedder.py` |
| Day 3-4 | FAISS 入门：IndexFlatIP、IndexIVFFlat | 把上一步的向量存入 FAISS，实现相似检索 | `vector_store.py` |
| Day 5-6 | 文档解析：PyPDF2 / python-docx / markdown | 写一个 DocumentLoader，支持 PDF/Word/Markdown | `document_loader.py` |
| Day 7 | 切片策略：固定长度、滑动窗口、语义切分 | 实现3种切分器，对比效果 | `chunker.py` |

**里程碑2**：把一个 PDF 文档 → 切片 → 向量化 → 存入 FAISS → 输入问题 → 返回最相似的3个文本块。

---

### 第3-4周：RAG 全流程项目（核心！）

**项目名**：「个人知识库问答系统」

```
用户上传 Markdown 笔记（你的 DRBCV 知识库）
→ 文档解析
→ 切片
→ 向量化存入 FAISS
→ 用户提问
→ 检索 Top-5 相关块
→ 拼 Prompt 发给 DeepSeek
→ 返回带引用来源的回答
```

**为什么选这个项目**：
- ✅ 涵盖了 AI 应用开发工程师面试的所有核心问题
- ✅ 你有现成的 DRBCV 知识库（268张卡片），直接当数据集
- ✅ 产出可以在 GitHub 上展示

| 日期 | 任务 | 具体产出 |
|------|------|----------|
| Week3 Day 1-2 | 搭建 FastAPI 服务骨架 | `POST /upload` `POST /query` 两个端点 |
| Week3 Day 3-5 | 实现完整的 RAG 管道 | `rag_pipeline.py`（加载→切片→向量化→检索→生成） |
| Week3 Day 6-7 | 添加引用来源标注 | 回答中标注 `[来源：xxx.md 第N段]` |
| Week4 Day 1-2 | 实现混合检索（向量+关键词） | BM25 + FAISS 双路召回 |
| Week4 Day 3-4 | 加 Rerank 重排序 | 用 BGE-Reranker 对检索结果二次排序 |
| Week4 Day 5-6 | 写测试 + README | 至少10个测试用例，README 包含架构图和 API 文档 |
| Week4 Day 7 | 部署到 Docker | `docker-compose up` 一键启动整个系统 |

**里程碑3**：GitHub 仓库 `personal-rag-qa`，README 中有架构图、API 文档和 10+ 测试用例。面试时可以现场演示。

**不要做的事（省时间）**：
- ❌ 不要手写 Transformer
- ❌ 不要学 PyTorch
- ❌ 不要训练任何模型
- ❌ 不要做前端界面（curl + Swagger 够用）

---

## 阶段二：技能深化（第5-8周）
### 目标：能独立搭建一个多 Agent 协作系统

> 此时黑马V6.5已在讲 RAG 和 Agent 部分。你已做过独立 RAG 项目，黑马的内容会帮你巩固和查漏补缺。

### 第5-6周：Agent 编排项目

**项目名**：「智能客服 Agent 系统」

```
用户问题 →
  路由 Agent（判断意图：退换货/技术咨询/投诉）
  → 退换货Agent（查订单库 + 生成退换流程）
  → 技术Agent（查知识库 + 排查步骤）
  → 投诉Agent（记录 + 生成安抚回复 + 升级人工）
→ 汇总 Agent（整合回复 + 生成工单摘要）
```

| 日期 | 学什么 | 做什么 |
|------|--------|--------|
| Week5 Day 1-2 | Agent 概念：ReAct 模式、Tool Calling、Function Calling | 手动实现一个单 Agent（不用框架） |
| Week5 Day 3-5 | LangChain 基础：Chain、Tool、AgentExecutor | 用 LangChain 重写单 Agent |
| Week5 Day 6-7 | Coze/Dify 低代码平台 | 在 Dify 上搭建一个 Agent 工作流（视觉化理解编排） |
| Week6 Day 1-3 | 多 Agent 编排：LangGraph 状态图 | 实现路由→专业Agent→汇总的完整流程 |
| Week6 Day 4-5 | Agent 记忆：对话历史管理、上下文窗口 | 实现滑动窗口记忆 + 摘要压缩 |
| Week6 Day 6-7 | 测试 + README | 10+ 测试用例，特别是路由逻辑的边界情况 |

**里程碑4**：GitHub 仓库 `multi-agent-cs`，能演示：输入"我的订单3天没发货" → 路由到退换货Agent → 查询模拟订单库 → 返回处理方案。

**关键学习点**（面试一定会问）：
- Agent 为什么会"跑偏"？（幻觉、工具调用失败、无限循环）→ 怎么解决？
- Function Calling vs ReAct 的区别？（前者让LLM决定调用什么工具，后者是固定的思考-行动-观察循环）
- LangGraph 的 StateGraph 如何管理多 Agent 状态？

---

### 第7-8周：API 工程化 + RAG 进阶

| 日期 | 技能 | 做进项目 |
|------|------|----------|
| Week7 Day 1-2 | 异常处理：自定义异常类、全局异常拦截 | 给之前的 RAG 项目加完整异常处理 |
| Week7 Day 3-4 | 并发处理：asyncio、后台任务、连接池 | FastAPI + asyncpg 异步数据库操作 |
| Week7 Day 5-6 | 限流与降级：slowapi 限流、LLM 调用降级策略 | LLM 超时→返回缓存结果或降级回复 |
| Week7 Day 7 | 日志与监控：structlog 结构化日志 | 所有项目统一日志格式 |
| Week8 Day 1-3 | RAG 评估：RAGAS 框架（Faithfulness, Relevance, Precision） | 用 RAGAS 评估你的 RAG 项目效果 |
| Week8 Day 4-5 | Graph RAG 入门：知识图谱 + 向量检索混合 | 用 Neo4j 建一个小型知识图谱做对比实验 |
| Week8 Day 6-7 | 回顾 + 简历项目打磨 | 把 RAG 和 Agent 两个项目写到简历上 |

**里程碑5**：两个项目都加了异常处理、日志、限流，简历上的项目描述不再是"做了个demo"，而是"做了个生产可用的系统"。

---

## 阶段三：整合冲刺（第9-12周）
### 目标：AI 伴侣 MVP + 简历 + 面试准备

> 此时黑马V6.5已讲完核心技术部分。用黑马的内容查漏补缺，重点打磨自己的独立项目。

### 第9-10周：AI 伴侣「永月」MVP

**MVP 范围**（不是完整系统，是可演示的最小核心）：

```
永月 MVP（2周可完成的版本）：
├── 对话引擎：DeepSeek API + 角色 Prompt
├── 短期记忆：最近10轮对话上下文
├── 长期记忆：Memobase 或自建 JSON 存储（3-5条 Profile 信息）
├── 语音输出：edge-tts（免费 TTS）
└── 界面：SillyTavern 前端（你已熟悉）
```

| 日期 | 任务 |
|------|------|
| Week9 Day 1-2 | 搭建基础对话：SillyTavern + DeepSeek + 角色卡 |
| Week9 Day 3-4 | 接入记忆：Memobase（或自建 SQLite 记忆表） |
| Week9 Day 5-6 | 接入语音：edge-tts 文字转语音 + sherpa-onnx 语音识别 |
| Week9 Day 7 | 集成测试：完整对话流程跑通 |
| Week10 Day 1-3 | 情感感知：简单的情感分类（喜怒哀乐）+ 不同回复风格 |
| Week10 Day 4-5 | 人格一致性：长期记忆提取 + 性格标签持久化 |
| Week10 Day 6-7 | 录演示视频 + 写项目 README |

**里程碑6**：一段 3 分钟的演示视频，展示「永月」对话、记忆、语音、情感反馈。

**MVP ≠ 最终产品**：目标是证明"我能做 AI 应用"，不是"我做出了完美的 AI 伴侣"。

---

### 第11周：面试冲刺

| 日期 | 做什么 |
|------|--------|
| Day 1-2 | **简历打磨**：3个项目（RAG问答、多Agent客服、永月MVP），每个项目3-4个 bullet point，突出你做了什么、解决了什么问题 |
| Day 3-4 | **技术面试模拟**：RAG 全流程口述、Agent 编排逻辑、API 设计思路、异常处理策略 |
| Day 5-6 | **算法题**：LeetCode 简单+中等 30题（Python），不追求题量，追求每个题能说清楚思路 |
| Day 7 | **系统设计**：模拟题「设计一个企业知识库问答系统」，画架构图、说技术选型理由 |

**面试自检清单**（每一项都要能流畅回答3分钟）：
- [ ] RAG 的完整流程是什么？每个环节有哪些优化手段？
- [ ] 你做的 RAG 项目遇到了什么问题？怎么解决的？
- [ ] Agent 的路由逻辑怎么实现的？怎么防止 Agent 跑偏？
- [ ] FastAPI 的依赖注入怎么用？异常处理怎么设计？
- [ ] Docker Compose 怎么编排多服务？环境变量怎么管理？
- [ ] 你的 AI 伴侣项目的记忆系统怎么设计的？为什么这样设计？

---

### 第12周：投递 + MCP 学习 + 黑马收尾

| 日期 | 做什么 |
|------|--------|
| Day 1-2 | **MCP 协议入门**：看 DeepLearning.AI 的 MCP 课程（1-2小时），了解 Anthropic 的标准化工具连接协议 |
| Day 3-4 | **投递第一批简历**（10-15份）：BOSS直聘 + 猎聘，关键词「AI应用开发」「RAG工程师」「Agent开发」「大模型应用开发」 |
| Day 5-6 | **根据反馈调整**：如果收到面试邀请 → 优先准备面试；如果石沉大海 → 检查简历关键词是否匹配 JD |
| Day 7 | **12周复盘**：对照最初目标，评估距离「可投递」还有多大差距，制定下一步计划 |

**投递策略**：
- 首选：AI 创业公司、量化金融（Python 路线，薪资 20-35k）
- 次选：互联网公司 AI 部门（Python 路线，薪资 18-28k）
- 排除：传统企业 Java 路线（薪资 15-20k，且你的 Java 达不到要求）

---

## 总时间分配

```
阶段一（第1-4周）  40% — RAG 核心技能（决定能否过简历关）
阶段二（第5-8周）  35% — Agent + 工程化（决定薪资区间）
阶段三（第9-12周） 25% — 作品 + 面试（决定能否拿 offer）
```

---

## 与黑马 V6.5 的关系

```
黑马V6.5（100天，8月开课）是你的"课本"
本路线图是你的"习题集"

不要等黑马讲完再动手：
  黑马讲 Prompt → 你已经在做独立的 Prompt 项目
  黑马讲 RAG → 你已经在优化自己的 RAG 系统
  黑马讲 Agent → 你的 Agent 项目已经跑了2周
  
黑马提供"怎么做"的标准答案
自定计划提供"自己做过"的独立经验
面试官要的是后者
```

---

## 每周检查点

| 周 | 不可跳过的检查项 | 没做到怎么办 |
|----|-----------------|-------------|
| 1 | `POST /prompt/generate` 能正常返回 | 不要进入第2周，Prompt 是所有后续技能的基础 |
| 2 | PDF→向量→检索→返回文本块 全流程跑通 | 不要进入第3周，RAG 90%的问题出在检索层 |
| 3-4 | GitHub 仓库 `personal-rag-qa` 有 README+测试 | 不要进入第5周，这是简历上的核心项目 |
| 5-6 | Agent 能正确路由3种意图 | 不要进入第7周，路由是 Agent 的骨架 |
| 7-8 | RAGAS 评估报告（有数字，不是感觉） | 不要进入第9周，没有评估=不知道系统好不好 |
| 9-10 | 永月 MVP 演示视频 | 不要进入面试，没有作品=没有议价权 |
| 11 | 3个项目写在简历上 + 每个能口述3分钟 | 简历不过关不要投，浪费机会 |

---

## 学习原则

1. **每天 200 行手写 Python**：不依赖 AI，自己打字。面试现场你没有 AI 辅助。
2. **先出效果，再学原理**：先用 DeepSeek API 搭出 RAG，再理解 Embedding 原理。
3. **产出导向**：每学一个模块 = 一个可展示的 GitHub 仓库，不是"笔记"。
4. **黑马是补充，不是主力**：黑马100天覆盖很多，但你的独立项目才是核心竞争力。
5. **不做前端**：curl + Swagger + CLI 够用。前端花时间且面试不考。

---

## 3个月后的你可能面临的面试

**面试官**：「你做的 RAG 项目，检索效果不好你是怎么排查的？」

**3个月后的你**：
> "我的 RAG 系统上线后发现 Top-5 召回准确率只有 60%。我做了三件事：第一，用 RAGAS 框架做了量化评估，发现 Faithfulness 还行但 Context Relevance 低；第二，我把固定长度切块改成了语义切分，Relevance 提到了 72%；第三，我加了 BM25 和向量检索的混合召回 + BGE-Rerank，最终 Top-5 准确率到了 89%。这里面最核心的教训是——切片策略比检索算法对效果的影响更大。"

**现在的你可能只能回答**: "呃...我就是调了 API..."

——这之间的差距，就是这12周要做的事。

---

## 附录：资源速查

### 学习资源（按使用顺序）

| 技能 | 资源 | 耗时 | 费用 |
|------|------|------|------|
| Docker Compose | Docker 官方文档 + 你已经有的基础 | 1-2天 | 免费 |
| Prompt Engineering | DeepLearning.AI "Prompt Engineering for Everyone" | 1小时 | 免费 |
| FAISS | FAISS 官方 Wiki + GitHub examples | 2-3天 | 免费 |
| LangChain | LangChain 官方文档 Quickstart | 1天 | 免费 |
| LangGraph | LangGraph 官方 Tutorial | 2天 | 免费 |
| Dify | dify.ai 在线版 | 半天 | 免费 |
| RAGAS | ragas.io 文档 | 1天 | 免费 |
| MCP | DeepLearning.AI "MCP with Anthropic" | 1-2小时 | 免费 |
| 黑马V6.5 | 已报名（8月开课） | 100天 | 已付 |

### 面试准备

- LeetCode：Python 简单+中等 30题
- 系统设计：参考 System Design Interview 里的 "Design a Chat System" 和 "Design a Web Crawler"
- 项目展示：3个 GitHub 仓库 + 1个演示视频

---

## 相关研究

本路线图是「三线并行研究」方向C的核心产出。配套研究：

- **[方向A] AI应用开发岗位画像** (`../A_job_profile/`)：70条JD → 技能权重排序 → 薪资带（中位22K）→ 公司类型画像
- **[方向B] AI伴侣技术路线** (`../B_ai_companion/`)：6项目全维对比 → 架构深度 → 3套技术方案推荐
- **[综合分析] REPORT.md** (`../REPORT.md`)：三方汇总（由 vb-analyst 产出）
- **[DRBCV知识卡片]**：由 vb-librarian 从三方向提取，存入 D:\DRBCV-Knowledge\
