---
title: "AI应用开发工程师-岗位画像"
type: "概念"
category: "AI-Job-Market"
tags: [岗位画像, 日常工作, Python, 深圳]
created: 2026-07-27
---

# AI应用开发工程师-岗位画像

## 是什么（What）

AI 应用开发工程师不是训练大模型的人，而是**把模型用起来**的人 — 让 LLM 能查知识库、调 API、理解上下文、不出错。日常工作分三块：Prompt 调优、RAG 召回排查、Agent 编排开发。

这就像餐厅厨师 vs 使用料理包的人：模型训练工程师是"从原材料做菜的厨师"，AI 应用开发工程师是"用现成料理包组合出不同的菜品"。

## 为什么重要（Why）

- 对用户的意义：这是目前深圳 AI 岗位中需求量最大、入门门槛最低的方向 — 不需要博士学历、不需要会训练模型
- 在技术体系中的位置：处于 LLM 和用户需求之间的"翻译层"，决定 AI 产品是否真的能用
- 70条深圳JD分析显示：典型一天 = Prompt调优(上午) + Agent开发/API联调(下午) + Code Review/学习(晚上)

## 怎么做（How）

### 日常工作流

```
9:00  — 站会，看Jira/飞书看板
9:30  — Prompt 效果调优（LangSmith跑对比实验）
10:30 — RAG 召回率排查（Grafana看数据，修chunk策略）
13:30 — Agent 逻辑开发（LangGraph状态机编排）
15:00 — API 联调（FastAPI + Postman）
16:00 — 模型路由 & 成本优化（便宜模型处理简单问答）
19:00 — 技术方案文档 + Code Review
```

### 每天必用的工具

| 层级 | 工具 | 频率 |
|------|------|------|
| 写代码 | Python + FastAPI | 每天 |
| Prompt调试 | LangSmith / OpenAI Playground | 每天 |
| 向量/RAG | Milvus/Chroma + 文档解析 | 每周3-4次 |
| Agent框架 | LangChain/LangGraph/LlamaIndex | 每周3-4次 |
| 模型接口 | OpenAI/Anthropic/国产API | 每天 |
| 部署 | Docker | 发布时 |

## 与其他卡片的关系

- [[AI应用开发-必备技能清单]] → 岗位需要的具体技能
- [[深圳AI岗位-薪资分布]] → 这个岗位值多少钱
- [[AI应用开发-公司类型选择]] → 去哪类公司做这个岗位
- [[AI应用开发-3个月求职策略]] → 怎么3个月内拿到offer

## 个人见解（留空待填）

<!-- 你对这个岗位的真实感受是什么？你觉得自己最匹配哪部分工作？最怕哪部分？ -->

## 信息来源

- 来源：Boss直聘 70条深圳JD分析（2026-07-27）
- 来自研究：2026-07-27 AI-job-and-path → A_job_profile/02_jd_template.md
