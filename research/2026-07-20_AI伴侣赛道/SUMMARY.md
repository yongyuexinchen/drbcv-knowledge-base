# AI 伴侣赛道调研 · 总结

> 日期：2026-07-20 | 5 Phase 全流程完成 | 产出 1,459 行 + 14 张知识卡片

---

## 一、赛道全景

全球 AI 伴侣市场 ~$28 亿，年增长 35%，DAU 超 5000 万。核心玩家：Character.AI（被 Google $2.7B 收购）、Replika（3000 万用户）、MiniMax/Talkie（港股 IPO）。

## 二、开源生态 5 层模型

```
硬件载体 (ESP32) → 前端 UI (SillyTavern 30k⭐) → 角色引擎 (Soul-of-Waifu) → 记忆系统 (Memobase 蓝海) → LLM 推理 (Ollama/LocalAI)
```

关键发现：**记忆层是蓝海**（最大项目仅 2.8k⭐），人格引擎层是新兴（最大 800⭐）。这两层正是大厂盲区。

## 三、竞品致命缺陷

| 竞品 | 致命缺陷 | 我们的机会 |
|------|---------|-----------|
| Character.AI | 云端 + 闭源 + 收购后边缘化 | 本地优先 |
| Replika | 云端 + NSFW 政策反复 + 无独立人格 | 独立人格引擎 |
| SillyTavern | 前端工具，不提供人格 | companion-core 填补 |

## 四、核心判断

> **"不要做更好的 Character.AI，做 Character.AI 做不到的事。"**

少女项目不是在大厂主场比赛，而是在大厂盲区（本地隐私 + 独立人格 + 开源生态）建立不可替代性。这是**正交竞争**，不是颠覆式创新。

## 五、A 级推荐：companion-core 人格记忆引擎

```
pip install companion-core
```

**v0.1 三模块（工期 ~3 周，零成本）：**

| 模块 | 功能 | 技术 |
|------|------|------|
| Persona | 角色定义、多角色管理 | YAML/JSON 配置文件 |
| 情绪状态机 | 情绪维度、衰减曲线、触发规则 | Python 状态机 |
| 三层记忆 | 短期（会话）/ 中期（摘要）/ 长期（画像） | Memobase 式 profile memory |

**不做的**：前端 UI（借 SillyTavern）、模型推理（调 API/Ollama）、移动端 App、硬件。

## 六、产出清单

```
E:\research\2026-07-20_ai-companion-track\
├── industry.md             (178 行) — 市场 $28亿，12 家玩家
├── github_analysis.md      (609 行) — 51 项目，12 深度分析
├── competitor.md           (325 行) — Character.AI/Replika/Talkie/星野 拆解
├── opportunity.md          (318 行) — DRBCV 分析，A 级推荐人格引擎
└── knowledge_cards/        (14 张) — 已同步至 D:\DRBCV-Knowledge\Venture\
```

## 七、下一步

1. 验证 Memobase — `git clone` + `docker compose up` 跑通记忆系统
2. 设计 companion-core 的 Persona schema（人格卡片模板）
3. 实现 v0.1 情绪状态机原型（Python，100 行以内）
