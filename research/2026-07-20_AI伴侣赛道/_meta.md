# 研究元信息

| 字段 | 值 |
|------|-----|
| 主题 | AI伴侣赛道调研 |
| 日期 | 2026-07-20 |
| 状态 | completed |
| 触发词 | 研究 AI 伴侣赛道 |
| 综合评分 | 7.2/10（市场需求8+技术成熟度7+竞争程度6+个人匹配度7+差异化9+变现潜力6，A/B级推荐） |

## Phase 进度

- [x] Phase 1: 领域扫描（行业地图、核心玩家、技术趋势） — vb-researcher 完成
- [x] Phase 2: GitHub 扫描（开源项目15个，深度分析12个） — vb-gh-explorer 完成
- [x] Phase 3: 竞品拆解（5个商业产品深度分析） — vb-researcher 完成
- [x] Phase 4: 机会分析（DRBCV方法评估） — vb-analyst 完成，A/B级推荐
- [x] Phase 5: 知识卡片汇总 & 索引更新 — vb-librarian 完成

## 产出文件

| 文件 | 大小 | 来源 |
|------|------|------|
| industry.md | 行业地图（全球+中国，5种商业模式，5个技术趋势） | vb-researcher |
| competitor.md | 竞品深度分析（Character.AI/Replika/Talkie/小冰/Nomi.ai） | vb-researcher |
| github_analysis.md | 开源扫描报告（15项目，12深度分析，7直接竞品） | vb-gh-explorer |
| _github_raw_data.json | 原始扫描数据 | vb-gh-explorer |
| opportunity.md | DRBCV五维机会分析（Domain/Research/Boundary/Comparison/Value） | vb-analyst |
| mvp_blueprint.md | companion-core 人格引擎 MVP 蓝图 | vb-analyst |
| summary.md | 研究结论摘要（300-500字，面向决策者） | vb-librarian |
| knowledge_cards/ | 14张DRBCV知识卡片 | 混合来源 |

### 知识卡片清单

| 类型 | 卡片 | 来源 |
|------|------|------|
| Industry | industry_ai_companion.md | vb-researcher |
| Product | product_character_ai.md | vb-researcher |
| Product | product_replika.md | vb-researcher |
| Product | product_talkie_minimax.md | vb-researcher |
| Product | product_xiaoice.md | vb-researcher |
| Product | product_nomi_ai.md | vb-researcher |
| Project | project_memobase.md | vb-gh-explorer |
| Project | project_shikigami_protocol.md | vb-gh-explorer |
| Project | project_front_porch.md | vb-gh-explorer |
| Project | project_soul_of_waifu.md | vb-gh-explorer |
| Project | project_sillytavern.md | vb-librarian |
| Opportunity | opportunity_ai_companion.md | vb-analyst |
| Opportunity | opportunity_ecosystem_gaps.md | vb-gh-explorer |
| Architecture | architecture_companion_stack.md | vb-librarian |

## 核心结论

- **赛道本质**：AI伴侣是「关系容器」而非「聊天工具」
- **最大空白**：人格引擎层 — 全赛道无人真正解决人格一致性长期记忆
- **避坑方向**：不做完整AI伴侣产品（正面竞争Character.AI/MiniMax），不做NSFW平台（中国政策风险）
- **推荐方向**：companion-core 人格引擎中间件（pip install companion-core），v0.1 = Persona + 情绪状态机 + 三层记忆，工期~3周，零成本
- **差异化路径**：正交竞争 — 在大厂因商业模式和监管无法进入的「本地隐私+独立人格+开源生态」维度建立不可替代性
