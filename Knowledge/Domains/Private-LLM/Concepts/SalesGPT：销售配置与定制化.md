---
name: SalesGPT：销售配置与定制化
type: procedure
status: exploding
source: "[[智能销售大模型（如何使用）上_原文]] / [[智能销售大模型（如何使用）下_原文]]"
domain: Private-LLM
---

# SalesGPT：销售配置与定制化

## 类型判定
[Procedure — 核心是「如何修改配置文件来定制不同企业/产品的销售代理」，包含配置文件结构、提示词模板机制和 API 模式配置]

## 类比 ★
### 一句话比喻
> 给销冠机器人换「剧本」——老婆饼店就换成「张阿姨，酥皮老婆饼传承人，饼皮 18 层」，健身房就换成「李教练，5 年私教经验，增肌减脂双证」——换一个配置文件就像给机器人换一套人设和产品目录，代码一行不用改。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 配置文件 (examples/config_CN) | 销售员的人设档案——姓名、职位、公司、话术 |
| 产品知识库 (product_catalog) | 销售员手里的产品目录——每个产品的卖点和价格 |
| 提示词模板 (prompts/prompts_CN) | 销售的「战术手册」——8 个阶段该说什么、怎么推进 |
| use_tools 参数 | 是否允许销售员「翻目录」——True=可以查产品信息，False=只能靠脑子 |
| 提示词中的花括号变量 | 剧本里的填空——{{company_name}} 替换成「老王烧饼铺」|
| API 模式 vs 终端模式 | 远程操控 vs 当面演示——API 能嵌入企业系统，终端只能命令行聊 |
| max_turns（最大轮次） | 防骚扰开关——聊够 20 轮自动挂电话，别跟客户废话 |

## 是什么
SalesGPT 通过三个层级的配置文件实现高度定制化：(1) 销售人设配置（`examples/`目录下的 YAML 文件，定义姓名/公司/产品/销售目的/沟通方式）；(2) 提示词模板（`prompts/` 目录，内置三套模板——有工具版、无工具版、阶段判断版）；(3) 产品知识库（文本文件，定义产品名称-卖点-价格）。所有花括号变量在启动时自动替换，形成完整 System Prompt。还支持 API 模式启动，供企业前端系统调用。

## 输入-输出空间
- **输入**: 自定义的销售配置 YAML + 产品知识库文档 + 提示词模板选择 + 模型选择
- **输出**: 个性化的 AI 销售代理（终端对话或 API 端点）
- **前置条件**: Jupyter Notebook 已安装（用于可视化编辑）；`agents.py` 中需注释掉特定行；`run.py` 中 model_name 建议设为 GPT-4

## 正例（≥2 个）
1. **床垫公司→律师事务所快速切换**: 修改配置文件：`salesperson_name: 王律师` → `company_name: 正和法律事务所` → `company_business: 企业法律顾问服务` → 产品文档替换为「常年法律顾问 3万/年」「合同审核 500元/份」→ 启动后 AI 自动以律师身份推销法律服务。
2. **API 模式嵌入电话系统**: 修改 `run_api.py` 中 `model_name` 为 GPT-4 → `config_path` 指向中文配置 → 启动 API → 企业前端调用 API 端点，客户电话接入后 AI 自动接听并按 8 阶段流程推进——真人只接有意向的高质量线索。

## 反例/边界（≥1 个）
1. **随意修改提示词模板可能导致 Agent 行为异常**: `prompts_CN` 中的提示词是经过测试的最优版本，尤其是花括号变量部分——只建议修改示例对话（Example 1/2）中的中文内容，特殊符号和变量名绝对不能动，否则启动报错。
2. **不使用工具时需删除 use_tools 参数**: 如果配置文件中有 `use_tools: true` 但没有提供 `product_catalog` 路径，Agent 会尝试搜索不存在的文档导致报错——不使用工具就直接删除 `use_tools` 参数。
3. **英文模板在 Tool-Use 上更优**: 即使目标对话是中文，工具调用（搜索产品文档）的部分建议使用英文模板（prompts 而非 prompts_CN），因为英文模板在思维链推理上表现更好——在配置文件里设置回复语言为中文即可。

## 详细解释

### 三层配置结构
```
SalesGPT/
├── examples/
│   ├── config_CN          ← 【L1】销售人设配置（YAML）
│   │   ├── salesperson_name: 张三
│   │   ├── company_name: Sleep Haven
│   │   ├── company_business: 高级床垫公司
│   │   ├── company_values: 提供最佳睡眠解决方案
│   │   ├── conversation_purpose: 了解客户是否想购买床垫
│   │   ├── conversation_type: phone call
│   │   ├── use_tools: true
│   │   └── product_catalog: examples/product_catalog.txt
│   └── product_catalog.txt ← 【产品知识库】
│       ├── Product 1: LuminaDream 记忆海绵床垫
│       │   - 特色: 3层记忆海绵+凝胶散热
│       │   - 价格: $999
│       └── Product 2: ElysiumRest 凝胶床垫 ...
├── prompts/
│   ├── prompts_CN         ← 【L2】中文提示词模板
│   ├── prompts            ← 【L2】英文提示词模板（工具调用更优）
│   └── stage_analyzer     ← 【L2】阶段判断模板
└── agents/
    └── sales_agent.py     ← 【L3】模板选择入口
```

### 关键配置参数
| 参数 | 作用 | 修改建议 |
|------|------|----------|
| `salesperson_name` | 销售名字 | 根据企业实际销售人员命名 |
| `company_business` | 主营业务 | 一句话概括，如「智能家居解决方案」 |
| `company_values` | 公司价值观 | 影响 AI 推荐产品时的语气和侧重点 |
| `conversation_purpose` | 销售目的 | 引流线下 / 直接成交 / 预约演示 |
| `conversation_type` | 沟通方式 | phone call / text message |
| `use_tools` | 启用产品搜索 | 有产品文档就 `true`，纯话术销售就删掉 |
| `product_catalog` | 产品文档路径 | 格式建议：产品名 + 卖点 + 价格 |

### API 模式启动流程
```
① 编辑 run_api.py:
   - model_name = "gpt-4"
   - config_path = "examples/config_CN"（或英文版）

② 终端启动 API:
   python3 run_api.py

③ 另开终端测试:
   curl -X POST http://localhost:5000/chat -d '{"message": "你好"}'

④ 嵌入企业系统: 企业前端调用 API 端点即可
```

### 提示词模板替换机制
```
原始模板:
"你的名字是 {{salesperson_name}}，在 {{company_name}} 担任 {{salesperson_role}}"

读取配置 → 替换变量 → 最终 Prompt:
"你的名字是 张三，在 Sleep Haven 担任 销售代表"
```

## 关系
### → 指向
- [[私有化大模型项目通用部署流程]] (SalesGPT 的服务器选配和基础环境搭建参考通用部署流程)

### ← 被指向
- [[SalesGPT：AI 销售代理概述与部署]] (先部署项目，再进行个性化配置)
