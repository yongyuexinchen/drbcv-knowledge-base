---
name: Skill渐进式披露
type: procedure
status: core
source: "[[Skill 技能开发与使用_原文]]"
domain: Hermes
---

# Skill渐进式披露

## 类型判定
Skill 文件的分层加载机制——Agent 先看摘要，用到时才看详情，用到外部资源时才加载外部资源，避免上下文膨胀。

## 类比 ★
### 一句话比喻
就像餐厅菜单——你进门先看到菜名和一句话简介（元数据），决定要点这道菜时服务员才拿来详细做法（SKILL.md 正文），需要特殊酱料时才去后厨取（外部脚本/文件），而不是一进门就把整个后厨搬到桌上。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| YAML 元数据（第一层） | 菜单上的菜名 + 一句话简介 |
| SKILL.md 正文（第二层） | 服务员拿来的详细菜谱 |
| 外部脚本/文件（第三层） | 后厨的特殊酱料和工具 |
| 渐进式披露 | 需要什么看什么，不一次性全堆上来 |
| 上下文膨胀 | 把所有菜谱全摊在桌上导致桌面堆满 |

## 是什么
渐进式披露（Progressive Disclosure）是 Skill 文件的核心加载机制。一个 SKILL.md 文件由三部分组成：① YAML 元数据（用三个横杠包裹，描述 Skill 名称、触发场景、禁触发场景）；② 正文步骤（Agent 用到的具体执行逻辑）；③ 外部引用（脚本、模板、参考文档）。Agent 采用三层递进加载：第一层启动时只看元数据；第二层决定调用该 Skill 时才加载正文；第三层执行中需要外部文件时才加载外部资源。这与"工具绑定"无关，纯粹是一种上下文优化策略。

## 正例（≥2 个）
1. **tech-news Skill 加载**：Hermes 启动 → 扫描 skill/ 目录 → 加载 tech-news 的元数据"搜索并总结过去24小时关于指定关键字的全球科技新闻" → 用户说"斜杠tech-news 大模型" → Agent 判定匹配 → 加载完整步骤（搜索哪些网站、输出格式、文件保存路径）。
2. **百度热搜 Skill**：从 ClawdHub 下载的 Skill 包含 Python 脚本和 SQLite 数据库初始化文件 → Agent 只在需要采集热搜时加载脚本，在首次使用时初始化数据库。

## 反例/边界（≥1 个）
1. **全量上下文加载**（非渐进式）：Agent 启动时就把所有 Skill 的完整内容塞进上下文——50 个 Skill 全部展开导致 Token 消耗爆炸，对话很快触及上下文窗口上限。
2. **元数据描述不准确**：如果 YAML 元数据中 description 写得太模糊，Agent 无法正确判断何时调用该 Skill——渐进式披露的前提是第一层元数据足够精确。

## 详细解释
SKILL.md 文件结构：
```markdown
---
name: tech-news
description: 搜索并总结过去24小时关于指定关键字的全球科技新闻
triggers: 用户询问科技新闻、行业动态
no_triggers: 非科技类新闻、娱乐八卦
---
# 具体步骤
1. 解析用户意图，提取关键字
2. 搜索新闻网站...
3. 合成简报，保存到 desktop/news_*.md
```

目录组织：
- `~/.hermes/skill/` — Skill 根目录
- `~/.hermes/skill/news/tech-news/` — 按类别分组的 Skill（news 是类别，tech-news 是 Skill 名）
- `~/.hermes/skill/tech-news/` — 无类别的独立 Skill 也可直接放根目录
- 每个 Skill 目录下包含：`SKILL.md` + 可选的 `references/`、`templates/`、`scripts/`

版本管理：目前无内置版本管理工具，建议通过 Git 自行维护 Skill 版本，或将旧版改名存档。

## 关系
### → 指向
- [[Skill工作流封装]]
- [[Token效率优化]]
- [[Hermes Agent框架]]
### ← 被指向
- [[Token效率优化]]
- [[Skill工作流封装]]
