#!/usr/bin/env python3
"""
Safe LaTeX fix for cards 26-55. Only applies EXACT string replacements
that are known to be safe. Does NOT use regex on tables.

Rules:
1. Fix \\\\int -> \\int etc (double backslash)
2. Fix table $|x|$ -> $\\lvert x\\rvert$ (with known specific patterns)
3. Fix $\\ln|x|$ -> $\\ln\\lvert x\\rvert$ globally
4. Fix dx without \\, (only in specific known contexts)
"""
import os

CONCEPTS_DIR = "D:/DRBCV-Knowledge/Calculus/Concepts"

target_files = [
    "定积分的几何应用.md",
    "定积分的物理应用.md",
    "定积分的性质.md",
    "定积分中值定理.md",
    "对称区间定积分——偶倍奇零.md",
    "对称区间定积分一般公式.md",
    "对称区间积分公式.md",
    "对数求导法.md",
    "反常积分.md",
    "反函数定义.md",
    "反函数求导法则.md",
    "反余切函数.md",
    "反余弦函数.md",
    "反正切函数.md",
    "反正弦函数.md",
    "费马引理.md",
    "分部积分法.md",
    "分部积分循环法（还原法）.md",
    "分部积分中u和dv的选取原则（反对幂指三）.md",
    "复合函数求导法则（链式法则·链导法）.md",
    "高阶导数.md",
    "高阶导数的定义.md",
    "根式代换.md",
    "拐点.md",
    "函数的单调性.md",
    "函数的单调性与极值.md",
    "函数极限（ε-δ定义）.md",
    "函数图形的描绘与渐近线.md",
    "华里士公式.md",
    "积不出积分.md",
]

def safe_fix(content):
    """Apply only safe string replacements."""
    changes = []
    
    # ==========================================
    # Rule 1: Fix double backslash LaTeX commands
    # ==========================================
    double_bs_fixes = [
        ('\\\\int', '\\int'),
        ('\\\\frac', '\\frac'),
        ('\\\\ln', '\\ln'),
        ('\\\\sin', '\\sin'),
        ('\\\\cos', '\\cos'),
        ('\\\\tan', '\\tan'),
        ('\\\\cot', '\\cot'),
        ('\\\\sec', '\\sec'),
        ('\\\\csc', '\\csc'),
        ('\\\\lim', '\\lim'),
        ('\\\\displaystyle', '\\displaystyle'),
        ('\\\\lvert', '\\lvert'),
        ('\\\\rvert', '\\rvert'),
        ('\\\\arcsin', '\\arcsin'),
        ('\\\\arccos', '\\arccos'),
        ('\\\\arctan', '\\arctan'),
        ('\\\\operatorname', '\\operatorname'),
        ('\\\\begin{cases}', '\\begin{cases}'),
        ('\\\\end{cases}', '\\end{cases}'),
        ('\\\\begin{vmatrix}', '\\begin{vmatrix}'),
        ('\\\\end{vmatrix}', '\\end{vmatrix}'),
        ('\\\\begin{bmatrix}', '\\begin{bmatrix}'),
        ('\\\\end{bmatrix}', '\\end{bmatrix}'),
        ('\\\\sqrt', '\\sqrt'),
        ('\\\\to', '\\to'),
        ('\\\\infty', '\\infty'),
        ('\\\\cdot', '\\cdot'),
        ('\\\\text', '\\text'),
        ('\\\\boxed', '\\boxed'),
        ('\\\\neq', '\\neq'),
        ('\\\\leq', '\\leq'),
        ('\\\\geq', '\\geq'),
        ('\\\\Rightarrow', '\\Rightarrow'),
        ('\\\\longrightarrow', '\\longrightarrow'),
    ]
    
    for old, new in double_bs_fixes:
        c = content.count(old)
        if c > 0:
            content = content.replace(old, new)
            changes.append(f"去双反斜杠 {old} ({c}处)")
    
    # ==========================================
    # Rule 2 & 3: Fix | to \lvert...\rvert 
    # Only in specific known safe patterns
    # ==========================================
    
    # In MATH MODE ONLY: $ln|x|$ -> $\ln\lvert x\rvert$
    # These are safe exact replacements
    abs_fixes = [
        # Specific patterns seen in the files
        ('$|f(x) - g(x)|$', '$\\lvert f(x) - g(x)\\rvert$'),
        ('$|f(x)|$', '$\\lvert f(x)\\rvert$'),
        ('$|x|$', '$\\lvert x\\rvert$'),
        ('$|x|^3$', '$\\lvert x\\rvert^3$'),
        ('$|\sin x|$', '$\\lvert\\sin x\\rvert$'),
        ('$\\ln|x|$', '$\\ln\\lvert x\\rvert$'),
        ('$\\ln|y|$', '$\\ln\\lvert y\\rvert$'),
        ('$\\ln|f(x)|$', '$\\ln\\lvert f(x)\\rvert$'),
        ('$\\ln|x|', '$\\ln\\lvert x\\rvert'),
        ('$\\ln|y|', '$\\ln\\lvert y\\rvert'),
        ('$\\ln|1+t|$', '$\\ln\\lvert 1+t\\rvert$'),
        ('$\\ln|1+\\sqrt{x}|$', '$\\ln\\lvert 1+\\sqrt{x}\\rvert$'),
        ('$\\ln|1+\\sqrt[6]{x}+1|$', '$\\ln\\lvert 1+\\sqrt[6]{x}+1\\rvert$'),  # Hmm, this looks wrong
        ('$\\ln|t+1|$', '$\\ln\\lvert t+1\\rvert$'),
        ('$\\ln|\\sec x+\\tan x|$', '$\\ln\\lvert\\sec x+\\tan x\\rvert$'),
        ('$\\ln|\\sec x+\\tan x|+C$', '$\\ln\\lvert\\sec x+\\tan x\\rvert+C$'),
        ('$\\ln|\\sec x+\\tan x|+C$', '$\\ln\\lvert\\sec x+\\tan x\\rvert+C$'),
        ('$\\ln|\\sec x+\\tan x|$', '$\\ln\\lvert\\sec x+\\tan x\\rvert$'),
        ('|\\sec x + \\tan x|', '\\lvert\\sec x + \\tan x\\rvert'),
        ('$\\lvert f(x) \\rvert', '$\\lvert f(x)\\rvert'),  # fix missing $
        # Display math patterns
        ('\\left| \\int_a^b f(x) \\, dx \\right|', '\\left\\lvert \\int_a^b f(x) \\, dx \\right\\rvert'),
        # Table-specific patterns (these are in $...$ inside table cells)
        ('$\\int_a^b |f-g|\\,dx$', '$\\int_a^b \\lvert f-g\\rvert\\,dx$'),
        ('$\\int_a^b |f-g| dx$', '$\\int_a^b \\lvert f-g\\rvert\\,dx$'),
        # In the IO table cells
        ('|f(x)|', '\\lvert f(x)\\rvert'),
    ]
    
    for old, new in abs_fixes:
        c = content.count(old)
        if c > 0:
            content = content.replace(old, new)
            changes.append(f"|→\\lvert: {old}")
    
    # ==========================================
    # Rule 4: Fix dx without \, prefix
    # In display math: dx -> \,dx  (only before line end or space)
    # Only do exact string matches to be safe
    # ==========================================
    
    # Fix specific display math patterns: dx at end of $$...$$
    dx_fixes = [
        # Display math: dx before closing $$
        (' dx $$', ' \\,dx $$'),
        # Display math: dx followed by newline
        # In specific formulas we know about
        (' f(x) dx $$', ' f(x) \\,dx $$'),
        (' f(x) dx }$$', ' f(x) \\,dx }$$'),
    ]
    
    for old, new in dx_fixes:
        c = content.count(old)
        if c > 0:
            content = content.replace(old, new)
            changes.append(f"\,dx: {old}")
    
    # ==========================================
    # Also fix specific patterns from the error table
    # ==========================================
    error_table_fixes = [
        ('| 错误 | 正确 | 原因 |', '| 错误 | 正确 | 原因 |'),  # no-op, keep
        ('| `\\\\int` | `\\int` | 单反斜杠 |', '| `\\\\int` | `\\int` | 单反斜杠 |'),  # no-op, keep
    ]
    
    return content, changes


def main():
    modified_count = 0
    all_results = []
    
    for fname in target_files:
        fpath = os.path.join(CONCEPTS_DIR, fname)
        if not os.path.exists(fpath):
            print(f"⚠ NOT FOUND: {fname}")
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        new_content, changes = safe_fix(content)
        
        if new_content != original:
            modified_count += 1
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ {fname}:")
            for c in changes:
                print(f"    - {c}")
            all_results.append((fname, changes))
        else:
            print(f"○ {fname}: 无需修改")
    
    print(f"\n{'='*60}")
    print(f"修正总结: {modified_count}/{len(target_files)} 张卡片被修改")
    print(f"{'='*60}")
    for fname, changes in all_results:
        print(f"  📄 {fname}")
        for c in changes:
            print(f"      • {c}")


if __name__ == '__main__':
    main()
