---
name: RAG
type: procedure
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-智能管道
---

# RAG（Retrieval Augmented Generation，检索增强生成）

## 类型判定
过程型 — 一套「先检索、再增强、后生成」的知识注入流水线。

## 类比 ★
### 一句话比喻
RAG 像给 LLM 配了一个随身图书管理员——用户问「永月喜欢什么颜色」，管理员立刻从档案室翻出用户偏好记录递给 LLM，LLM 看完回答「她喜欢月白色」。没有管理员，LLM 只能瞎猜。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| RAG 整体 | 给 LLM 配的随身图书管理员——你问问题，管理员翻档案递给 LLM 参考 |
| Embedding + 向量库 | 档案室的智能书架——按语义找，不是按标题找 |
| Chunking + Retrieval | 把厚书拆成页，管理员挑 3 页最相关的递进去 |

## 是什么
RAG 是一种**给 LLM 外挂知识库**的模式。流程：① 离线阶段：将知识文档切片 → 向量化（Embedding） → 存入向量数据库；② 在线阶段：用户提问 → 向量检索 top-k 相关片段 → 将检索结果注入 Prompt → LLM 生成回答。它解决了 LLM 的两大痛点：知识截止日期（训练数据是旧的）和幻觉（没有依据时瞎编）。

## 输入-输出空间
- **输入（离线）**: 知识文档（Markdown、PDF、数据库记录等）
- **输入（在线）**: 用户查询文本
- **输出**: 基于检索到的知识片段生成的回答（带引用来源）
- **关键参数**: chunk_size（切片大小）、top_k（检索数量）、embedding_model（向量化模型）

## 正例（≥2 个）
1. **ChatGPT 知识库问答**: 用户上传 PDF → 系统切片+向量化 → 用户提问时检索相关段落 → GPT 基于原文回答
2. **AI 伴侣记忆检索**: 用户的聊天记录、偏好、事件存入向量库 → 对话时检索相关记忆 → LLM 基于记忆生成个性化回应

## 反例/边界（≥1 个）
1. **纯 LLM 对话**: 没有检索步骤，LLM 只靠训练数据回答——这不是 RAG
2. **边界 1 — 检索失败**: 如果知识库没有相关内容，RAG 退化为纯 LLM 回答（可能幻觉）
3. **边界 2 — 切片不当**: chunk 太大则检索精度低，太小则丢失上下文——需要在语义完整性和检索精度间取舍

## 详细解释
RAG 的核心公式可以理解为：
$$\text{Answer} = \text{LLM}(\text{Query} \oplus \text{Retrieve}(\text{Query}, \text{KnowledgeBase}))$$

即：回答 = LLM（问题 + 从知识库检索到的相关内容）。

在 AI 伴侣架构中，RAG 位于 Memory 和 LLM 之间：
```
用户输入 → Memory（检索相关记忆）→ RAG（检索外部知识）→ Prompt组装 → LLM
```
RAG 负责「外部知识」，Memory 负责「用户个人历史」，两者共同构成 LLM 的上下文来源。

## 关系
### → 指向
- [[Embedding]] — Embedding 是 RAG 的「翻译官」，把文本变成向量
- [[Vector Database]] — 向量数据库是 RAG 的存储和检索引擎
- [[Similarity Search]] — 相似度搜索是检索步骤的核心算法

### ← 被指向
- [[LLM]] — RAG 为 LLM 注入知识
- [[Long-term Memory]] — 长期记忆是 RAG 在 AI 伴侣中的具体应用场景
- [[AI Agent]] — Agent 用 RAG 获取工具执行所需的知识
