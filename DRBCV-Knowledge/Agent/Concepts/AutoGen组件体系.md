---
name: AutoGen组件体系
type: mixed
status: core
source: "[[Agent多智能体使用教程_原文]]"
domain: Agent
---

# AutoGen组件体系

## 类型判定
多智能体框架中构成群聊式协作的最小功能单元集合，每个组件承担明确的角色或连接职责。

## 类比 ★
### 一句话比喻
就像乐高积木，每块积木都有固定形状和接口，你不需要自己造积木，只需要把正确的积木拼在一起，就能搭出辩论赛、编程助手或知识库客服。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| AutoGen Assistant 组件 | 团队里不同岗位的员工 |
| GroupChat Manager 组件 | 会议主持人 |
| AutoGen User 组件 | 客户的麦克风 |
| Agent Chain 组件 | 流程接线板 |
| AutoGen Coder 组件 | 专门跑代码的技术员 |
| AutoGen RetrieveUserProxy | 能查资料的情报员 |

## 是什么
AutoGen 组件体系是必胜（Bisheng）项目中多智能体工作流的积木式组件库。每个组件从画布左侧拖出，具有特定的输入/输出连接点（红心表示必填），通过配置参数（model name、system message、API key 等）来定制行为。核心组件包括 Assistant（智能体成员）、User（用户代理）、GroupChat Manager（群聊调度）、Coder（代码执行）、Chain（工作链整合）以及可外挂知识库的高级 Retrieve 组件。

## 正例（≥2 个）
1. **辩论赛工作流**：2 个 Assistant（正/反方）+ 1 个 User（主持人）+ 1 个 GroupChat Manager + 1 个 Chain = 5 个组件完成自动辩论。
2. **编程助手工作流**：1 个 Assistant（写代码）+ 1 个 Coder（执行代码）+ 1 个 User + 1 个 Manager + 1 个 Chain = 5 个组件完成写代码并执行。
3. **知识库问答工作流**：多个 RetrieveUserProxy Agent（各自挂载不同向量数据库）+ 向量检索组件 + Manager + Chain = 多知识源智能问答。

## 反例/边界（≥1 个）
1. 单体 Agent 只需要 LLM + Tool + Agent 三个组件，不需要 GroupChat Manager 和 Chain 这些多智能体专属组件。组件选型取决于任务复杂度。

## 详细解释
组件参数说明：
- **model_name**：模型类型（推荐 GPT-4，GPT-3.5 失败率高达 80%）
- **name**：只允许字母、下划线、数字，禁用中文
- **system_message**：角色工作流程和要求限定
- **temperature**：控制输出随机性
- **API Key**：填入 OpenAI 密钥

Chain 组件是从"工作链"区域拖出的整合器，它是多智能体工作流的必选项，连接 User → Chain 和 Manager → Chain。

高级组件 **AutoGen RetrieveUserProxyAgent** 可以外挂向量知识库，使 Agent 具备检索增强能力，配合 embedding 模型进行语义检索。

## 关系
### → 指向
- [[多智能体协作]]
- [[知识库检索增强生成]]
### ← 被指向
- [[多智能体协作]]
