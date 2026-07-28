# 宏观传导发现引擎 — 工程规格书

> 来源: `.hermes/desktop-attachments/ENGINEERING_PLAN.md`
> 配套项目: `E:/macro-warning-system`

## 系统概述

宏观传导发现引擎是一个从"LLM驱动的新闻评分"重构为"数据驱动的因果发现系统"的项目。核心理念：数据是锚（现实），叙事是帆（预期），规律自动发现，贴现率量化缺口。

## 四层架构

1. **基础层 (Phase 1)**: config/schema/YAML配置 — 定义12个资产板块、74个硬指标、40+叙事主题、30+阈值规则
2. **信号层 (Phase 2)**: 数据采集（akshare/FRED/东方财富） + 叙事结构化（新闻→NarrativeSignal，LLM仅做填空题）
3. **发现层 (Phase 3)**: 偏互相关 + Granger因果 + 传递熵 + PCMCI + 结构突变 + 变量自动发现 → 5种方法并行 + 贴现率计算
4. **输出层 (Phase 4)**: 传导图（D3.js力导向图） + 贴现率看板 + 日报 → FastAPI + 飞书推送

## 关键技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 传输熵 | IDTxl | Python原生，比JIDT Java桥接稳定 |
| 因果发现 | Tigramite PCMCI | 学术主流，去中介能力强 |
| 特征选择 | SHAP + XGBoost | 高解释性 |
| LLM角色 | 仅结构化+报告总结 | 不参与评分/传导/推理 |
| 存储 | SQLite + Parquet | 轻量单机 |

## 数据覆盖

- 12个资产板块：美债/中国宏观/A股/黄金/能源/原材料/农产品/中国债券/美股/国内政治/美国政治/国际
- 74个硬指标（来自akshare/FRED）
- 40+叙事主题（topic_taxonomy.yaml）

## 实现状态

2026年7月已实现：全模块代码完成（`E:/macro-warning-system`），包括：
- 5种发现方法全部实现（cross_correlation / granger / transfer_entropy / pcmci / structural_break）
- 贴现率分析器完整实现（DiscountAnalyzer + 历史类似模式匹配）
- Orchestrator 主流水线可跑通
- D3.js 仪表盘 + FastAPI 后端
- 自动化调度（APScheduler）
