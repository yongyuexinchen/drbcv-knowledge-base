# Calculus 知识库项目记忆

## 项目结构
- `Concepts/` — 112 张数学概念卡（含 83 张曾含「待补充」占位符的卡片，已于 2026-07-17 全量修复）
- `Articles/` — 64 篇源文章
- `Sources/` — 6 个源索引文件（极限与连续、导数与微分、微分中值定理与导数应用、不定积分、定积分、知乎-备战期末定积分方法技巧）
- `Templates/名词卡片模板.md` — 卡片格式标准
- `Systems/` — 系统级配置

## 卡片格式
两种格式共存：
- **旧格式**：frontmatter 含 `type: concept-card`, `title`, `chapter`, `source`, `difficulty`, `status`, `tags`
- **新格式**：frontmatter 含 `name`, `status`, `type`, `source`

卡片必须包含的 section：
1. 类型判定 / 是什么
2. 输入-输出空间
3. 正例（≥2个）/ 反例（≥1个）
4. 详细解释（推导过程 + 重要推论）
5. 经典例题（≥2题，含完整解答）
6. 类比（一句话比喻 + 物理映射表）
7. 关系（[[wikilink]] 双向链接：由...推导而来 / 可推导出 / 属于）

## DRBCV 研究方法
参考 SKILL.md：`C:/Users/53028/AppData/Local/hermes/skills/research/drbcv-research-method/SKILL.md`
版本：V0.5（2026-07-17 升级）
多 Agent 工作流：Orchestrator → Scanner → [验证] → Merger → **Sampler 抽查** → Card-Writer → [占位符自检] → Linker → [双向链接验证] → Reviewer（硬规则脚本 + 语义抽查）
- V0.5 核心改进：分阶段验收、占位符零容忍、Reviewer 硬规则前置检查
- 验证脚本：`scripts/reviewer_check.py`（占位符/frontmatter/wikilink/section/LLM泄露检测）
- 验证清单：`references/reviewer-checklist.md`

## 高等数学六大主题分组
1. 极限与连续（10 个概念）
2. 导数与微分（16 个概念）
3. 微分中值定理与导数应用（20 个概念）
4. 不定积分（21 个概念）
5. 定积分（11 个概念）
6. 反三角函数（5 个概念）
