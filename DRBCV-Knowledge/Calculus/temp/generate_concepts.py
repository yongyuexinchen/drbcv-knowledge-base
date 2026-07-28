#!/usr/bin/env python3
"""
DRBCV Card-Writer Agent: Batch generate Calculus concept markdown cards.
Reads calculus-merged-selected.json (selected_new field), applies 名词卡片模板.md format,
writes to Concepts/ directory without overwriting existing files.
"""

import json
import os
import re
import sys

# Paths
JSON_PATH = "D:/DRBCV-Knowledge/Calculus/temp/calculus-merged-selected.json"
TEMPLATE_PATH = "D:/DRBCV-Knowledge/Calculus/Templates/名词卡片模板.md"
OUTPUT_DIR = "D:/DRBCV-Knowledge/Calculus/Concepts"

# Type mapping: unify various type strings
TYPE_MAP = {
    "discriminant": "判别型 — 区分/定义概念，建立判断标准",
    "connection": "关联型 — 连接不同概念，揭示等价关系",
    "mixed": "混合型 — 兼具判别和关联特征",
    "procedure": "程序型 — 给出操作步骤/计算方法",
    "definition": "定义型 — 明确术语的数学定义",
    "concept": "定义型 — 明确数学概念",
    "theorem": "关联型 — 定理/命题，揭示条件与结论的逻辑关系",
    "method": "程序型 — 给出明确的操作步骤或解题方法",
    "formula": "程序型 — 公式/计算方法",
    "property": "关联型 — 性质描述，揭示内在特征",
    "概念 (Concept)": "定义型 — 明确数学概念的定义",
    "定理 (Theorem)": "关联型 — 定理/命题，揭示逻辑关系",
    "定理 / 公式 (Theorem / Formula)": "关联型 — 定理与公式的综合描述",
    "定理 (Lemma)": "关联型 — 引理，为后续定理铺垫",
    "方法 (Method)": "程序型 — 操作步骤/计算方法",
    "概念 / 定理 (Concept / Theorem)": "混合型 — 兼有概念定义和定理性质",
    "概念对比 (Concept Comparison)": "判别型 — 对比不同概念，理清异同",
    "公式 (Formula)": "程序型 — 数学公式/计算方法",
    "公式集 (Formula Collection)": "程序型 — 公式集合/工具表",
    "判定准则 (Criterion)": "判别型 — 判定标准/充分条件",
    "法则 (Rule / Method)": "程序型 — 计算法则/操作规则",
    "题型 (Problem Type)": "程序型 — 题型分类/解题策略",
    "体系 (Framework)": "关联型 — 概念体系/关系图谱",
    "性质 (Property)": "关联型 — 性质描述，揭示内在特征",
    "方法论 (Methodology)": "程序型 — 方法论/解题思想",
    "性质": "关联型 — 性质描述，揭示内在特征",
    "定义": "定义型 — 明确术语的数学定义",
    "定理": "关联型 — 定理/命题，揭示逻辑关系",
    "公式": "程序型 — 数学公式/计算方法",
    "方法": "程序型 — 操作步骤/计算方法",
    "概念": "定义型 — 明确数学概念",
    "example": "判别型 — 典型例子/反例说明",
    "证明": "关联型 — 证明过程/逻辑推导",
    "concept": "定义型 — 明确数学概念",
    "定理 (Theorem)": "关联型 — 定理/命题，揭示逻辑关系",
}

def sanitize_filename(name: str) -> str:
    """Extract Chinese name for filename, sanitize for file system."""
    # Remove $...$ math content for filename
    clean = re.sub(r'\$.*?\$', '', name)
    # Remove English in parentheses
    clean = re.sub(r'\s*\(.*?\).*', '', clean).strip()
    # Remove leading/trailing special chars
    clean = clean.strip(' .-')
    # Replace forbidden chars
    clean = clean.replace('/', '·').replace('\\', '·')
    clean = clean.replace(':', '：').replace('*', '·').replace('?', '？')
    clean = clean.replace('"', "'").replace('<', '〈').replace('>', '〉')
    clean = clean.replace('|', '·')
    # Remove consecutive spaces
    clean = re.sub(r'\s+', '', clean)
    # Max length
    if len(clean) > 80:
        clean = clean[:80]
    return clean.strip() + '.md'

def get_type_judgment(concept_type: str) -> str:
    """Map raw type to Chinese type judgment."""
    return TYPE_MAP.get(concept_type, f"混合型 — {concept_type}")

def extract_name_display(name: str) -> str:
    """Extract display name (remove duplicates)."""
    return name

def build_input_output(concept: dict) -> str:
    """Build input-output space section."""
    # Try to infer from definition
    definition = concept.get("definition", concept.get("notes", ""))
    lines = []
    
    if any(kw in concept.get("name", "") for kw in ["函数", "$\\arcsin", "$\\arccos", "$\\arctan", "$\\operatorname{arccot}"]):
        lines.append("- **输入**: 定义域内的自变量值")
        lines.append("- **输出**: 对应的函数值（在值域内）")
        lines.append("- **映射关系**: $x \\mapsto f(x)$，定义域到值域的单值映射")
    elif any(kw in concept.get("name", "") for kw in ["导数", "微分"]):
        lines.append("- **输入**: 函数 $f(x)$ 和点 $x_0$（或区间）")
        lines.append("- **输出**: 导数值 $f'(x_0)$（变化率）或微分 $\\mathrm{d}y$（线性主部）")
        lines.append("- **映射关系**: 从函数到其变化率的映射（微分算子）")
    elif any(kw in concept.get("name", "") for kw in ["积分", "不定积分", "原函数"]):
        lines.append("- **输入**: 函数 $f(x)$（被积函数）")
        lines.append("- **输出**: 原函数族 $F(x)+C$（不定积分）或数值（定积分）")
        lines.append("- **映射关系**: 求导运算的逆映射")
    elif any(kw in concept.get("name", "") for kw in ["极限", "收敛", "发散"]):
        lines.append("- **输入**: 数列 $\\{x_n\\}$ 或函数 $f(x)$")
        lines.append("- **输出**: 极限值 $A$（或判敛结论）")
        lines.append("- **映射关系**: 从序列/函数到其趋近值的映射")
    elif any(kw in concept.get("name", "") for kw in ["定理", "引理"]):
        lines.append("- **输入**: 满足条件的函数 $f(x)$（如连续、可导等）")
        lines.append("- **输出**: 存在性结论（如存在 $\\xi$ 满足等式）")
        lines.append("- **映射关系**: 条件到结论的逻辑蕴含关系")
    elif any(kw in concept.get("name", "") for kw in ["泰勒", "麦克劳林"]):
        lines.append("- **输入**: $n$ 阶可导函数 $f(x)$ 和展开点 $x_0$")
        lines.append("- **输出**: 多项式逼近 $P_n(x)$ + 余项 $R_n(x)$")
        lines.append("- **映射关系**: 函数到其泰勒多项式的逼近映射")
    elif any(kw in concept.get("name", "") for kw in ["取整", "小数部分", "整数部分"]):
        lines.append("- **输入**: 任意实数 $X$")
        lines.append("- **输出**: 整数部分 $\\lfloor X \\rfloor$ 或小数部分 $\\{X\\}$")
        lines.append("- **映射关系**: $X \\mapsto \\lfloor X \\rfloor$（取整映射) 或 $X \\mapsto \\{X\\}$（小数部分映射）")
    elif any(kw in concept.get("name", "") for kw in ["反函数"]):
        lines.append("- **输入**: 原函数值域中的 $y$")
        lines.append("- **输出**: 对应定义域中的 $x$")
        lines.append("- **映射关系**: $y \\mapsto x$（原映射的逆映射）")
    elif any(kw in concept.get("name", "") for kw in ["等价无穷小", "无穷小"]):
        lines.append("- **输入**: 趋于0的变量 $\\alpha, \\beta$")
        lines.append("- **输出**: 比值极限（判断等价性）或等价替换结果")
        lines.append("- **映射关系**: 从无穷小量到其趋零速度的比较")
    elif any(kw in concept.get("name", "") for kw in ["未定式"]):
        lines.append("- **输入**: 极限表达式 $\\lim \\frac{f(x)}{g(x)}$ 等")
        lines.append("- **输出**: 极限值（需变形后求解）")
        lines.append("- **映射关系**: 无法直接映射，需恒等变形")
    elif any(kw in concept.get("name", "") for kw in ["洛必达"]):
        lines.append("- **输入**: $\\frac{0}{0}$ 或 $\\frac{\\infty}{\\infty}$ 型极限")
        lines.append("- **输出**: 求导后极限（若存在）")
        lines.append("- **映射关系**: 原极限 $\\to$ 导数之比的极限")
    elif any(kw in concept.get("name", "") for kw in ["单调", "极值", "最值", "凹凸", "拐点", "渐近"]):
        lines.append("- **输入**: 函数 $f(x)$ 及其导数信息")
        lines.append("- **输出**: 单调区间/极值点/最值/凹凸区间/拐点/渐近线")
        lines.append("- **映射关系**: 导数符号 $\\to$ 函数性态的映射")
    elif any(kw in concept.get("name", "") for kw in ["参数方程", "隐函数", "对数求导", "链式"]):
        lines.append("- **输入**: 复合函数 / 隐函数方程 / 参数方程")
        lines.append("- **输出**: 导数表达式 $\\frac{dy}{dx}$")
        lines.append("- **映射关系**: 函数结构 $\\to$ 导数表达式的变换")
    elif any(kw in concept.get("name", "") for kw in ["有理函数", "分式", "部分分式", "裂项"]):
        lines.append("- **输入**: 有理分式 $\\frac{P(x)}{Q(x)}$")
        lines.append("- **输出**: 最简分式之和 / 积分结果")
        lines.append("- **映射关系**: 复杂有理函数 $\\to$ 简单分式分解")
    elif any(kw in concept.get("name", "") for kw in ["三角代换", "换元", "万能代换", "根式代换", "倒代换"]):
        lines.append("- **输入**: 含根式 / 三角函数的被积函数")
        lines.append("- **输出**: 换元后的有理函数积分形式")
        lines.append("- **映射关系**: $x \\mapsto \\varphi(t)$ 的反向映射")
    elif any(kw in concept.get("name", "") for kw in ["莱布尼茨"]):
        lines.append("- **输入**: 两个 $n$ 阶可导函数 $u(x), v(x)$")
        lines.append("- **输出**: 乘积 $(uv)^{(n)}$ 的 $n$ 阶导数表达式")
        lines.append("- **映射关系**: 从因子到乘积高阶导数的组合映射")
    elif any(kw in concept.get("name", "") for kw in ["定积分", "黎曼"]):
        lines.append("- **输入**: 闭区间 $[a,b]$ 上的有界函数 $f(x)$")
        lines.append("- **输出**: 数值（黎曼和的极限）")
        lines.append("- **映射关系**: 函数 $\\to$ 其下方图形面积的代数和")
    elif any(kw in concept.get("name", "") for kw in ["元素法", "微元法"]):
        lines.append("- **输入**: 分布在区间上的待求总量 $Q$")
        lines.append("- **输出**: 总量 $Q = \\int_a^b f(x)\\,dx$")
        lines.append("- **映射关系**: 微元 $dQ$ 的累加 $\\to$ 定积分")
    elif any(kw in concept.get("name", "") for kw in ["华里士", "Wallis", "点火", "三角函数积分变换"]):
        lines.append("- **输入**: $\\sin^n x$ 或 $\\cos^n x$ 在 $[0,\\pi/2]$ 上的积分")
        lines.append("- **输出**: 用递推公式计算出的精确值")
        lines.append("- **映射关系**: $n$ 次幂积分 $\\to$ 降阶递推")
    elif any(kw in concept.get("name", "") for kw in ["分部积分"]):
        lines.append("- **输入**: 乘积形式的被积函数 $u(x)v'(x)$")
        lines.append("- **输出**: 积分结果 $uv - \\int v\\,du$")
        lines.append("- **映射关系**: $\\int u\\,dv \\to uv - \\int v\\,du$ 的转化映射")
    elif any(kw in concept.get("name", "") for kw in ["凑微分", "第一类换元"]):
        lines.append("- **输入**: 复合函数乘积形式 $f(\\varphi(x))\\varphi'(x)$")
        lines.append("- **输出**: 积分结果 $F(\\varphi(x)) + C$")
        lines.append("- **映射关系**: 复合函数 $\\to$ 外层原函数的链式反演")
    elif any(kw in concept.get("name", "") for kw in ["辅助函数"]):
        lines.append("- **输入**: 待证结论和目标函数")
        lines.append("- **输出**: 满足罗尔定理条件的辅助函数 $F(x)$")
        lines.append("- **映射关系**: 结论形式 $\\to$ 构造函数的设计映射")
    elif any(kw in concept.get("name", "") for kw in ["有限增量"]):
        lines.append("- **输入**: 可导函数 $f(x)$ 和增量 $\\Delta x$")
        lines.append("- **输出**: 精确等式 $f(x_0+\\Delta x)-f(x_0) = f'(x_0+\\theta\\Delta x)\\Delta x$")
        lines.append("- **映射关系**: 增量 $\\to$ 导数与增量乘积的精确表达")
    elif any(kw in concept.get("name", "") for kw in ["中值", "双中值"]):
        lines.append("- **输入**: 满足条件的多个函数和区间")
        lines.append("- **输出**: 存在一个或多个中间点满足等式")
        lines.append("- **映射关系**: 条件 $\\to$ 存在性结论")
    elif any(kw in concept.get("name", "") for kw in ["变上限", "变限积分"]):
        lines.append("- **输入**: 连续函数 $f(x)$ 和变量上限 $x$")
        lines.append("- **输出**: 以 $x$ 为自变量的积分函数 $\\Phi(x)$")
        lines.append("- **映射关系**: 被积函数 $\\to$ 其原函数（变上限积分）")
    elif any(kw in concept.get("name", "") for kw in ["零点"]):
        lines.append("- **输入**: 连续函数 $f(x)$ 和区间 $[a,b]$")
        lines.append("- **输出**: 存在 $\\xi$ 使 $f(\\xi)=0$")
        lines.append("- **映射关系**: 介值定理的特殊情形")
    elif any(kw in concept.get("name", "") for kw in ["介值"]):
        lines.append("- **输入**: 连续函数 $f(x)$ 和区间 $[a,b]$")
        lines.append("- **输出**: 存在 $\\xi$ 取到介值")
        lines.append("- **映射关系**: 连续性 $\\to$ 值域区间覆盖")
    elif any(kw in concept.get("name", "") for kw in ["可导与连续"]):
        lines.append("- **输入**: 函数 $f(x)$ 在 $x_0$ 的可导性")
        lines.append("- **输出**: 连续性结论")
        lines.append("- **映射关系**: 可导 $\\Rightarrow$ 连续（逻辑蕴含）")
    elif any(kw in concept.get("name", "") for kw in ["一点可导"]):
        lines.append("- **输入**: 函数 $f(x)$ 在 $x_0$ 可导")
        lines.append("- **输出**: 局部性质（连续/定义）")
        lines.append("- **映射关系**: 一点可导 $\\to$ 该点性质")
    elif any(kw in concept.get("name", "") for kw in ["可积性"]):
        lines.append("- **输入**: 闭区间上有界函数 $f(x)$")
        lines.append("- **输出**: 可积/不可积的判断")
        lines.append("- **映射关系**: 函数性质 $\\to$ 可积性判断")
    elif any(kw in concept.get("name", "") for kw in ["狄利克雷"]):
        lines.append("- **输入**: 实数 $x$")
        lines.append("- **输出**: $1$（有理数）或 $0$（无理数）")
        lines.append("- **映射关系**: 有理/无理的判别函数")
    elif any(kw in concept.get("name", "") for kw in ["对称", "偶倍奇零"]):
        lines.append("- **输入**: $[-a,a]$ 上的函数 $f(x)$")
        lines.append("- **输出**: 简化后的积分值")
        lines.append("- **映射关系**: 奇偶性 $\\to$ 积分简化")
    elif any(kw in concept.get("name", "") for kw in ["周期"]):
        lines.append("- **输入**: 周期为 $T$ 的函数 $f(x)$")
        lines.append("- **输出**: 任意周期上的定积分值")
        lines.append("- **映射关系**: 周期性 $\\to$ 积分区间可平移")
    elif any(kw in concept.get("name", "") for kw in ["分段"]):
        lines.append("- **输入**: 分段表达的连续/可积函数")
        lines.append("- **输出**: 积分结果（分段积分之和）")
        lines.append("- **映射关系**: 分段点 $\\to$ 区间拆分映射")
    elif any(kw in concept.get("name", "") for kw in ["平均值"]):
        lines.append("- **输入**: 可积函数 $f(x)$ 和区间 $[a,b]$")
        lines.append("- **输出**: 数值 $\\frac{1}{b-a}\\int_a^b f(x)\\,dx$")
        lines.append("- **映射关系**: 函数 $\\to$ 其在区间上的均值")
    elif any(kw in concept.get("name", "") for kw in ["常用凑微分"]):
        lines.append("- **输入**: 被积函数中的复合结构")
        lines.append("- **输出**: 微分形式的变换结果")
        lines.append("- **映射关系**: 微分反向变换对照表")
    elif any(kw in concept.get("name", "") for kw in ["组合法"]):
        lines.append("- **输入**: 二次质因式分母 $\\frac{Bx+C}{x^2+px+q}$")
        lines.append("- **输出**: 对数 + 反正切的积分结果")
        lines.append("- **映射关系**: 裂项映射 $\\to$ 凑微分+配方法")
    elif any(kw in concept.get("name", "") for kw in ["幂函数积分"]):
        lines.append("- **输入**: 幂函数 $x^\\alpha$")
        lines.append("- **输出**: 积分结果 $\\frac{x^{\\alpha+1}}{\\alpha+1}+C$ 或 $\\ln|x|+C$")
        lines.append("- **映射关系**: 幂函数 $\\to$ 其原函数")
    elif any(kw in concept.get("name", "") for kw in ["相关变化率"]):
        lines.append("- **输入**: 相关变量 $x(t), y(t)$ 及其关系 $F(x,y)=0$")
        lines.append("- **输出**: 未知变化率 $\\frac{dy}{dt}$ 或 $\\frac{dx}{dt}$")
        lines.append("- **映射关系**: 已知变化率 $\\to$ 未知变化率通过隐函数求导链传递")
    else:
        lines.append("- **输入**: 概念适用的对象/前提条件")
        lines.append("- **输出**: 概念产生的结果/结论")
        lines.append("- **映射关系**: 从输入到输出的对应关系")
    
    return "\n".join(lines)

def require_content(value, field_name: str, concept_name: str):
    """Fail instead of writing placeholder text into cards."""
    if value is None:
        raise ValueError(f"{concept_name}: missing required field {field_name}")
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{concept_name}: empty required field {field_name}")
    if isinstance(value, list) and not value:
        raise ValueError(f"{concept_name}: empty required field {field_name}")
    return value

def build_examples(examples: list, concept_name: str = "") -> str:
    """Build positive examples section. At least 2."""
    if not examples:
        raise ValueError(f"{concept_name}: examples are required")
    result = []
    for i, ex in enumerate(examples[:4], 1):
        result.append(f"{i}. **场景{i}**: {ex}")
    while len(result) < 2:
        raise ValueError(f"{concept_name}: at least 2 examples are required")
    return "\n".join(result)

def build_counter_examples(counter_examples: list, concept_name: str = "") -> str:
    """Build counter examples section. At least 1."""
    if not counter_examples:
        raise ValueError(f"{concept_name}: counter_examples are required")
    result = []
    for ex in counter_examples[:2]:
        result.append(f"1. **常见误解/边界**: {ex}")
    return "\n".join(result)

def build_derivation(concept: dict) -> str:
    """Build derivation section based on concept type and content."""
    name = concept.get("name", "")
    definition = concept.get("definition", "")
    notes = concept.get("notes", "")
    
    # Use existing notes if they contain derivation info
    if notes and ("推导" in notes or "证明" in notes or "由" in notes):
        return notes[:500]
    
    raise ValueError(f"{name}: derivation/proof notes are required")

def build_corollaries(concept: dict) -> str:
    """Build corollaries section."""
    name = concept.get("name", "")
    notes = concept.get("notes", "")
    
    if notes and ("推出" in notes or "推论" in notes or "可推" in notes or "可导" in notes or "判断" in notes):
        return notes[:400]
    
    raise ValueError(f"{name}: corollaries or application notes are required")

def build_example_problems(concept: dict) -> str:
    """Build at least 2 example problems with solutions."""
    examples = concept.get("examples", [])
    notes = concept.get("notes", "")
    
    # Try to build problems from the examples data
    problems = []
    for ex in examples[:3]:
        problems.append(f"**题目**：{ex}\n**解**：见上方定义、推导过程与适用条件；生成脚本未从原始材料抽取到逐步解答。")
    
    while len(problems) < 2:
        raise ValueError(f"{concept.get('name', '')}: at least 2 example problems are required")
    
    result = []
    for i, prob in enumerate(problems, 1):
        result.append(f"**例题{i}**\n{prob}")
    
    return "\n\n".join(result)

def build_analogy(concept: dict) -> str:
    """Build analogy section with one-sentence analogy and physics mapping."""
    name = concept.get("name", "")
    
    analogies = {
        "取整": ("取整函数就像地板上的格子——你站在哪里不重要，你所在格子的编号是固定的。", [
            ("$\\lfloor X \\rfloor$", "地板上的格子编号"),
            ("$X$", "你在房间里的精确位置"),
            ("$\\{X\\}$", "距离所在格子左边界的距离"),
        ]),
        "反函数": ("反函数就像播放器的倒放键——把输出塞回去，得到原来的输入。", [
            ("原函数 $f$", "正向播放（输入→输出）"),
            ("反函数 $f^{-1}$", "倒放（输出→输入）"),
            ("$Y = X^3$ 与 $Y = \\sqrt[3]{X}$", "平方和平方根的映射关系"),
        ]),
        "极限": ("极限就像你走向一堵墙——你可以无限接近它，但永远碰不到。", [
            ("$x_n \\to A$", "你离墙的距离逐渐缩小"),
            ("$\\varepsilon$", "你设定的逼近容差"),
            ("$N$", "达到这个精度所需的最少步数"),
        ]),
        "导数": ("导数就像汽车的瞬时速度表——每时每刻告诉你变化有多快。", [
            ("$f'(x_0)$", "瞬时速度表读数"),
            ("$\\frac{\\Delta y}{\\Delta x}$", "平均速度（一段路程的平均）"),
            ("切线", "车灯方向——指向运动趋势"),
        ]),
        "微分": ("微分就像用放大镜看曲线——一小段看起来和直线一模一样。", [
            ("$\\Delta y$", "曲线上的实际升高"),
            ("$\\mathrm{d}y$", "用切线估算的升高"),
            ("$\\mathrm{d}y \\approx \\Delta y$", "小范围内以直代曲"),
        ]),
        "积分": ("积分就像把一根绳子切成小段再拼回去——整体由无数微小部分累加而成。", [
            ("$\\int_a^b f(x)\\,dx$", "把图形切成无数细条再求和"),
            ("$f(x_i)\\Delta x_i$", "第 $i$ 个细条的面积"),
            ("$\\Delta x \\to 0$", "细条越来越细，数量越来越多"),
        ]),
        "定理": ("微分中值定理就像高速公路测速——不查每时每刻的速度，只查全程平均速度，就知道至少有一刻的瞬时速度等于平均速度。", [
            ("$f(b)-f(a)$", "全程位移"),
            ("$b-a$", "全程时间"),
            ("$f'(\\xi)$", "至少有一时刻的速度等于平均速度"),
        ]),
        "泰勒": ("泰勒公式就像把一张复杂照片用马赛克拼出来——阶数越高，马赛克越细，越接近原图。", [
            ("$n$ 阶泰勒多项式", "低分辨率马赛克照片"),
            ("余项 $R_n(x)$", "原图与马赛克之间的差异"),
            ("$n \\to \\infty$", "马赛克越来越精细"),
        ]),
        "等价无穷小": ("等价无穷小就像用普通尺子量头发直径——反正都看不见，用什么都差不多。", [
            ("$\\sin x \\sim x$", "两根头发差不多细，直接换用"),
            ("乘除可代换", "尺子类型不影响测量结果"),
            ("加减不可代换", "两种尺子的微小差异在加减中会被放大"),
        ]),
        "不定积分": ("不定积分就像拼乐高的逆过程——给你一堆零件，你要复原出拼装说明书。", [
            ("$f(x)$", "一堆散乱零件（导数结果）"),
            ("$F(x)$", "拼装说明书（原函数）"),
            ("$C$", "不同批次印刷的封面颜色"),
        ]),
        "定积分": ("定积分就像用游标卡尺量弯曲木板的面积——切成小条量，加总就得到总面积。", [
            ("$\\int_a^b f(x)\\,dx$", "弯曲木板的总面积"),
            ("分割 $\\Delta x_i$", "切成 $n$ 个细条"),
            ("$f(\\xi_i)\\Delta x_i$", "第 $i$ 个细条的近似面积"),
        ]),
        "牛顿-莱布尼茨": ("牛顿-莱布尼茨公式就像电梯的楼层按钮——知道起点和终点的高度差，不需要一步步爬楼梯。", [
            ("$\\int_a^b f(x)\\,dx$", "起点 $a$ 到终点 $b$ 的总变化"),
            ("$F(x)$", "楼层计数器（原函数）"),
            ("$F(b)-F(a)$", "终点读数 - 起点读数"),
        ]),
        "洛必达": ("洛必达法则就像两辆赛车比谁快到终点——比的是瞬时速度而不是路程。", [
            ("$\\frac{0}{0}$ 型", "两车同时到达终点，比谁最后冲线快"),
            ("$\\frac{f'(x)}{g'(x)}$", "两车的瞬时速度比"),
            ("求导操作", "看速度表（比变化率）"),
        ]),
        "隐函数": ("隐函数就像藏在方程里的宝藏——$x$ 和 $y$ 纠缠在一起，需要两边求导解开。", [
            ("$F(x,y)=0$", "藏宝图的加密方程"),
            ("两边对 $x$ 求导", "逐步解密的过程"),
            ("$y'$ 的表达式", "最终找到的宝藏坐标"),
        ]),
        "分部积分": ("分部积分就像打球时的互相传球——把球传给更好得分的人。", [
            ("$\\int u\\,dv$", "你拿到了一个不好投的球"),
            ("$u$ 的选择", "传给谁更合适"),
            ("$uv - \\int v\\,du$", "传出去后的得分机会"),
        ]),
        "单调": ("函数的单调性就像爬山的坡度——上坡就是递增，下坡就是递减，平地就是驻点。", [
            ("$f'(x)>0$", "上坡路（递增）"),
            ("$f'(x)<0$", "下坡路（递减）"),
            ("$f'(x)=0$", "平地/山顶/谷底"),
        ]),
        "极值": ("极值就像山峰和山谷——你所在山头的最高点是极大值，山坳的最低点是极小值。", [
            ("极大值点", "周围都是下坡路的山顶"),
            ("极小值点", "周围都是上坡路的谷底"),
            ("$f'(x)=0$ 不是极值", "山脊上的鞍部（左右都是下坡或上坡）"),
        ]),
        "中值": ("中值定理就像期末考试——老师用全班平均分证明至少有一个人考了平均分。", [
            ("$f(b)-f(a)$", "全班总分"),
            ("$b-a$", "全班人数"),
            ("$f'(\\xi)$", "至少有一个人的分数等于平均分"),
        ]),
    }
    
    # Find best matching analogy - check longer/more specific keys first
    best_match = None
    # Priority ordering
    priority_keys = ["中值", "牛顿-莱布尼茨", "等价无穷小", "不定积分", "定积分",
                     "反函数", "泰勒", "导数", "微分", "洛必达", "隐函数",
                     "分部积分", "参数方程", "渐近线", "凹凸", "拐点", "单调",
                     "极值", "取整", "夹逼", "数列极限", "洛必达",
                     "积分", "定理", "极限", "函数"]
    for key in priority_keys:
        if key in analogies and key in name:
            best_match = analogies[key]
            break
    if not best_match:
        for key, (sentence, mapping) in analogies.items():
            if key in name:
                best_match = (sentence, mapping)
                break
    
    if not best_match:
        # Generic analogy
        return """### 一句话比喻
（待补充生活化比喻）

### 物理映射
| 数学对象 | 物理类比 |
|---------|---------|
| （待补充） | （待补充） |
"""
    
    sentence, mapping = best_match
    map_lines = [f"| {m[0]} | {m[1]} |" for m in mapping]
    
    return f"""### 一句话比喻
{sentence}

### 物理映射
| 数学对象 | 物理类比 |
|---------|---------|
{chr(10).join(map_lines)}
"""

def build_relations(concept: dict) -> str:
    """Build relation chain section with [[wikilinks]]."""
    related = concept.get("related_to", [])
    notes = concept.get("notes", "")
    
    # Find concepts in the data that mention this one for "可推导出"
    depends = []
    derives = []
    belongs = []
    
    for r in related:
        if isinstance(r, str):
            # Use as wikilink
            derives.append(f"- [[{r}]] (可推导出/应用)")

    if not derives:
        derives = ["- （待补充推导关系）"]
    
    # Build dependency chain
    return f"""### 由...推导而来（依赖）
- （待补充前置概念）

### 可推导出
{chr(10).join(derives[:6])}

### 属于 / 组成 / 应用
- [[Calculus]] (微积分体系)
"""

def generate_card(concept: dict) -> str:
    """Generate a complete markdown card from concept data."""
    name = concept.get("name", "未命名概念")
    ctype = concept.get("type", "concept")
    definition = concept.get("definition", "")
    examples = concept.get("examples", [])
    counter_examples = concept.get("counter_examples", [])
    notes = concept.get("notes", "")
    related = concept.get("related_to", [])
    sources = concept.get("sources", [])
    
    # Source for frontmatter - use simple concept name
    src_text = "[[Calculus]]"
    # If sources exist and have valid article names, extract short name
    if sources:
        # Try to extract a meaningful short name
        src_text = "[[Calculus 微积分]]"
    
    status = "exploding" if ctype in ("theorem", "定理", "定义", "definition") else "unexplored"
    
    card = f"""---
name: {name}
status: {status}
type: {get_type_judgment(ctype).split('—')[0].strip()}
source: {src_text}
---

# {name}

## 类型判定
{get_type_judgment(ctype)}

## 是什么
{definition if definition else notes[:300]}

## 输入-输出空间
{build_input_output(concept)}

## 正例（至少2个）
{build_examples(examples)}

## 反例/边界（至少1个）
{build_counter_examples(counter_examples)}

## 详细解释
{notes if notes else "（待补充详细解释，填补定义和正反例之间的逻辑链）"}

### 推导过程（★ 数学卡必须）
{build_derivation(concept)}

### 重要推论（★ 数学卡必须）
{build_corollaries(concept)}

## 经典例题（★ 至少2题，含完整解答）
{build_example_problems(concept)}

## 类比

{build_analogy(concept)}

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系（★ 必须用 [[wikilink]] 双向链接）

{build_relations(concept)}
"""
    return card

def main():
    # Load JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get selected_new concepts
    selected_new = data.get("selected_new", {})
    
    if not selected_new:
        print("ERROR: 'selected_new' field not found or empty in JSON")
        # Try new_concepts
        selected_new = data.get("new_concepts", {})
        print(f"Trying 'new_concepts' instead: {len(selected_new)} concepts")
    
    print(f"Found {len(selected_new)} concepts in selected_new")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get existing files
    existing_files = set()
    if os.path.isdir(OUTPUT_DIR):
        existing_files = set(f for f in os.listdir(OUTPUT_DIR) if f.endswith('.md'))
    
    print(f"Existing concept files: {len(existing_files)}")
    
    # Track results
    created = 0
    skipped = 0
    failed = []
    errors = []
    
    for concept_name, concept in selected_new.items():
        try:
            filename = sanitize_filename(concept_name)
            output_path = os.path.join(OUTPUT_DIR, filename)
            
            # Check if exists
            if os.path.exists(output_path):
                print(f"  SKIP (exists): {filename}")
                skipped += 1
                continue
            
            # Generate card
            card_content = generate_card(concept)
            
            # Write file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(card_content)
            
            print(f"  CREATE: {filename}")
            created += 1
            
        except Exception as e:
            error_msg = f"  FAIL: {concept_name} - {str(e)}"
            print(error_msg)
            failed.append(concept_name)
            errors.append(error_msg)
    
    # Summary
    print("\n" + "="*60)
    print(f"SUMMARY")
    print(f"  Total concepts in selected_new: {len(selected_new)}")
    print(f"  Created: {created}")
    print(f"  Skipped (already exists): {skipped}")
    print(f"  Failed: {len(failed)}")
    if failed:
        print(f"  Failed concepts:")
        for f_name in failed:
            print(f"    - {f_name}")
    print("="*60)
    
    return created, len(failed), failed

if __name__ == "__main__":
    main()
