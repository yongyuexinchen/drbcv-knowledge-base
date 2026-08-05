---
name: Token效率优化
type: discriminant
status: core
source: "[[Hermes Agent 核心概念与优势_原文]]"
domain: Hermes
---

# Token效率优化

## 类型判定
Hermes Agent 通过精巧的上下文加载机制和 Skill 缓存来降低每轮对话 Token 消耗的设计策略。

## 类比 ★
### 一句话比喻
就像你去办事，别人每次都要从头填表、复印全部材料再排队，而Hermes帮你建了档案——常用信息已经存档，每次只带变化的部分，进门刷脸就行，省时省纸。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 传统 Agent（全量上下文加载） | 每次办事都带一整箱文件 |
| Hermes 渐进式上下文加载 | 只带今天需要的两张纸 |
| Skill 自动缓存 | 常办业务已有档案，刷脸就行 |
| 重复描述同一流程 | 每次都要重新解释怎么办 |
| Hermes 自动复用 Skill | 系统自动识别"又是这事儿" |

## 是什么
Token 效率优化是 Hermes Agent 相对于 OpenCode 等同类产品的核心竞争力。它通过两层机制节省 Token：① **渐进式上下文加载**——Agent 启动时只加载 Skill 的元数据（轻量 YAML），用到时才加载完整步骤，用到外部文件时才加载引用文件，避免上下文膨胀；② **Skill 自动缓存**——Agent 将用户反复执行的操作流程自动封装为 Skill，后续调用时无需重新描述整个流程，直接触发已缓存的 Skill。实测使用相同模型时，Hermes 的 Token 消耗显著低于 OpenCode。

## 正例（≥2 个）
1. **渐进式加载**：用户安装了 50 个 Skill，但本次对话只需要用到"科技新闻总结"一个 Skill → Hermes 启动时只加载所有 Skill 的元数据（名称+简短描述），确定要用到这个 Skill 时才加载它的完整步骤内容。
2. **流程复用**：用户第一次说"搜索大模型新闻→总结→保存到桌面"，Hermes 执行完毕；第二次说同样的命令，Hermes 直接调用封装好的 Skill，不再重新推理步骤。

## 反例/边界（≥1 个）
1. **OpenCode 的全量加载模式**：每次对话都把全部 Skill 和工具描述塞进上下文，导致上下文快速膨胀，Token 消耗是 Hermes 的数倍。
2. **首次使用某一 Skill**：虽然渐进式加载节省了启动时的 Token，但首次调用某个 Skill 时仍需加载完整内容——Token 节省体现在"不需要加载所有 Skill"而非"完全零成本"。

## 详细解释
Token 节省的两大支柱：
1. **渐进式披露（Progressive Disclosure）**：
   - 第一层：启动时只加载 Skill 的 YAML 元数据（name、description、触发条件）
   - 第二层：确定使用某个 Skill 后，才加载该 Skill 的 SKILL.md 正文（具体步骤）
   - 第三层：步骤中引用了外部脚本/文件时，才加载这些外部资源
   - 效果：避免 50 个 Skill 全部塞进上下文

2. **Skill 缓存与复用**：
   - Agent 在对话中自动识别重复性操作模式
   - 将操作流程封装为可复用的 Skill
   - 后续类似任务直接触发 Skill，无需重新描述

经济性：使用 DeepSeek V4 Pro（6 元/百万 Token）运行 Hermes，一次复杂任务的 Token 成本约为 1-2 元，而同等任务在 OpenCode 上约为 4-8 元。

## 关系
### → 指向
- [[Skill渐进式披露]]
- [[Hermes Agent框架]]
### ← 被指向
- [[Hermes Agent框架]]
