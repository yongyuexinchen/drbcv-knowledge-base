#!/usr/bin/env python3
"""
Safe LaTeX fix - context-aware approach.

Key insight: Process content line by line. In lines that are NOT markdown
table rows (not starting with |), we can safely do more aggressive replacements.
In table rows, be very careful.

Rules applied:
1. Single backslash only (no \\\\int, \\\\frac, etc.)
2. All | inside $...$ or $$...$$ math → \\lvert...\\rvert  
   (but NOT | that are table cell separators)
3. dx without \\, → \\,dx (in math contexts)
"""
import os
import re

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


def is_table_row(line):
    """Check if line is a markdown table row."""
    s = line.strip()
    return s.startswith('|') and not s.startswith('|---') and not s.startswith('|--')

def fix_double_backslash(content):
    """Replace all double-backslash LaTeX commands with single backslash."""
    # List of LaTeX commands that commonly appear with double backslash
    cmds = [
        'int', 'frac', 'ln', 'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
        'lim', 'displaystyle', 'lvert', 'rvert',
        'arcsin', 'arccos', 'arctan', 'arccot', 'operatorname',
        'begin{cases}', 'end{cases}',
        'begin{vmatrix}', 'end{vmatrix}',
        'begin{bmatrix}', 'end{bmatrix}',
        'sqrt', 'infty', 'to', 'cdot', 'cdots',
        'partial', 'alpha', 'beta', 'gamma', 'theta', 'xi',
        'epsilon', 'delta', 'varphi', 'phi', 'psi',
        'omega', 'pi', 'tau', 'sigma', 'mu', 'lambda',
        'sum', 'prod',
        'text', 'boxed', 'bigl', 'bigr', 'Bigl', 'Bigr',
        'big', 'Big', 'bigg', 'Bigg', 'left', 'right',
        'quad', 'qquad', 'colon',
        'neq', 'leq', 'geq', 'approx', 'sim', 'equiv',
        'times', 'div', 'pm', 'mp',
        'circ', 'bullet', 'cdotp',
        'sinh', 'cosh', 'tanh',
        'log', 'lg',
        'min', 'max', 'sup', 'inf',
        'limsup', 'liminf',
        'Delta', 'nabla', 'nabla',
        'varepsilon', 'vartheta', 'varpi',
        'longrightarrow', 'rightarrow', 'Rightarrow',
        'leftarrow', 'Leftarrow', 'Leftrightarrow',
        'longleftrightarrow', 'mapsto', 'longmapsto',
        'implies', 'iff',
        'subset', 'supset', 'subseteq', 'supseteq',
        'cup', 'cap', 'setminus',
        'in', 'notin',
        'emptyset', 'varnothing',
        'Re', 'Im',
        'angle', 'triangle',
        'exists', 'forall',
        'neg', 'lor', 'land',
        'mid', 'parallel',
        'mod', 'pmod', 'bmod',
        'binom',
        'underset', 'overset',
        'widetilde', 'widehat',
        'overline', 'underline',
        'vec', 'dot', 'ddot',
        'tilde', 'hat', 'check', 'bar',
        'acute', 'grave', 'breve',
        'mathrm', 'mathbf', 'mathit', 'mathbb', 'mathcal',
        'mathscr', 'mathfrak', 'mathsf',
        'rm', 'bf',
        'textstyle', 'scriptstyle', 'scriptscriptstyle',
        'hfill', 'hspace', 'vspace',
        'fbox', 'boxed', 'makebox', 'mbox',
        'color', 'textcolor', 'colorbox',
        'tiny', 'scriptsize', 'footnotesize', 'small',
        'normalsize', 'large', 'Large', 'LARGE', 'huge', 'Huge',
        'sout', 'xout', 'uwave', 'dashuline', 'dotuline',
        'textcircled',
        'csc', 'coth',
        'iint', 'iiint', 'oiint',
        'colon', 'jot',
        'dfrac', 'tfrac',
        'cfrac',
        'smash', 'vphantom', 'hphantom',
        'mathclap', 'mathrlap', 'mathllap',
        'cancel', 'bcancel', 'xcancel',
        'enclose',
        'boldsymbol',
        'textorn', 'textpertenthousand',
        'perthousand',
        'degree',
        'mid',
    ]
    
    count = 0
    for cmd in cmds:
        old = '\\\\' + cmd
        new = '\\' + cmd
        c = content.count(old)
        if c > 0:
            content = content.replace(old, new)
            count += c
    
    return content, count


def fix_math_abs_in_text(line):
    """Fix | inside $...$ math in non-table lines."""
    # Replace |...| with \lvert...\rvert inside $...$
    # Only match balanced | inside math
    
    def replace_inline(m):
        inner = m.group(1)
        # Replace |...| patterns but only those that look like absolute values
        # Pattern: | followed by non-| text followed by |
        new_inner = re.sub(r'(?<!\\)\|([^|]+?)\|', r'\\lvert\1\\rvert', inner)
        return '$' + new_inner + '$'
    
    result = re.sub(r'\$([^$]+)\$', replace_inline, line)
    return result


def fix_math_abs_in_display(line):
    """Fix | inside $$...$$ math."""
    def replace_display(m):
        inner = m.group(1)
        new_inner = re.sub(r'(?<!\\)\|([^|]+?)\|', r'\\lvert\1\\rvert', inner)
        return '$$' + new_inner + '$$'
    
    result = re.sub(r'\$\$([^$]+)\$\$', replace_display, line)
    return result


def fix_dx_in_math(line):
    """Add \, before dx/dy/dt in math mode where missing."""
    # In $...$ inline math
    def fix_inline(m):
        inner = m.group(1)
        # Add \, before standalone dx, dy, dt, dh (but not existing that already have \,)
        inner = re.sub(r'(?<!\\)(\s*)dx\b', r'\,dx', inner)
        inner = re.sub(r'(?<!\\)(\s*)dy\b', r'\,dy', inner)
        inner = re.sub(r'(?<!\\)(\s*)dt\b', r'\,dt', inner)
        inner = re.sub(r'(?<!\\)(\s*)dh\b', r'\,dh', inner)
        # Fix common double-space issue: \, \,  -> \,
        inner = inner.replace(r'\,\,', r'\,')
        inner = inner.replace(r'\, ', r'\,')
        return '$' + inner + '$'
    
    result = re.sub(r'\$([^$]+)\$', fix_inline, line)
    
    # In $$...$$ display math
    def fix_display(m):
        inner = m.group(1)
        inner = re.sub(r'(?<!\\)(\s*)dx\b', r'\,dx', inner)
        inner = re.sub(r'(?<!\\)(\s*)dy\b', r'\,dy', inner)
        inner = re.sub(r'(?<!\\)(\s*)dt\b', r'\,dt', inner)
        inner = re.sub(r'(?<!\\)(\s*)dh\b', r'\,dh', inner)
        inner = inner.replace(r'\,\,', r'\,')
        inner = inner.replace(r'\, ', r'\,')
        return '$$' + inner + '$$'
    
    result = re.sub(r'\$\$([^$]+)\$\$', fix_display, result)
    return result


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = {}
    
    # Step 1: Fix double backslash (global, safe)
    content, db_count = fix_double_backslash(content)
    if db_count > 0:
        changes[f"去双反斜杠命令"] = db_count
    
    # Step 2: Process line by line for math | and dx fixes
    lines = content.split('\n')
    new_lines = []
    
    abs_count = 0
    dx_count = 0
    
    for line in lines:
        is_table = is_table_row(line)
        
        if is_table:
            # For table rows: split by |, fix inside each cell separately
            parts = line.split('|')
            fixed_parts = []
            for i, part in enumerate(parts):
                # Fix math inside each cell 
                part = fix_math_abs_in_text(part)
                part = fix_dx_in_math(part)
                fixed_parts.append(part)
            line = '|'.join(fixed_parts)
        else:
            # For non-table lines: more aggressive fixes
            new_line = line
            # Fix abs in inline math
            new_line = fix_math_abs_in_text(new_line)
            # Fix dx in math
            new_line = fix_dx_in_math(new_line)
            line = new_line
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # Count changes
    abs_count = content.count(r'\lvert') - original.count(r'\lvert')
    dx_count = content.count(r'\,dx') - original.count(r'\,dx')
    
    if abs_count > 0:
        changes["|→\\lvert"] = abs_count
    if dx_count > 0:
        changes["+\\,dx"] = dx_count
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    
    return False, {}


def main():
    modified = {}
    
    for fname in target_files:
        fpath = os.path.join(CONCEPTS_DIR, fname)
        if not os.path.exists(fpath):
            print(f"⚠ NOT FOUND: {fname}")
            continue
        
        ok, changes = fix_file(fpath)
        if ok:
            modified[fname] = changes
            parts = []
            for k, v in changes.items():
                parts.append(f"{k} ({v}处)")
            print(f"  ✅ {fname}: {', '.join(parts)}")
        else:
            print(f"  ○ {fname}: 无需修改")
    
    print(f"\n{'='*60}")
    print(f"修正总结: {len(modified)}/{len(target_files)} 张卡片被修改")
    print(f"{'='*60}")
    for fname, changes in sorted(modified.items()):
        parts = []
        for k, v in changes.items():
            parts.append(f"{k}: {v}处")
        print(f"  📄 {fname}")
        for p in parts:
            print(f"      • {p}")


if __name__ == '__main__':
    main()
