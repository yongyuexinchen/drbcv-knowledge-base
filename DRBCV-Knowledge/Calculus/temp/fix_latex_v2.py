#!/usr/bin/env python3
"""
Comprehensive LaTeX fix for cards 26-55.
- Fix dx without \, prefix (both $...dx$ and $$...dx$$
- Fix | inside tables (replace with \lvert...\rvert)
- Fix remaining double-backslash commands
- Add \displaystyle to integrals where appropriate
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

def fix_file(filepath):
    """Apply all LaTeX fixes to a file and return list of fixes applied."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = []
    
    # 1. Fix double backslash commands (\\int -> \int, etc.)
    double_bs_cmds = [
        'int', 'frac', 'ln', 'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
        'lim', 'displaystyle', 'lvert', 'rvert',
        'arcsin', 'arccos', 'arctan', 'arccot', 'operatorname',
        'begin{cases}', 'end{cases}',
        'begin{vmatrix}', 'end{vmatrix}',
        'begin{bmatrix}', 'end{bmatrix}',
        'sqrt', 'infty', 'to', 'cdot', 'cdots', 'partial',
        'alpha', 'beta', 'gamma', 'theta', 'xi', 'epsilon', 'delta',
        'varphi', 'phi', 'psi', 'omega', 'pi', 'tau', 'sigma',
        'sum', 'prod', 'iint', 'iiint', 'oiint',
        'text', 'boxed',
        'bigl', 'bigr', 'Bigl', 'Bigr',
        'big', 'Big', 'bigg', 'Bigg',
        'left', 'right',
        'quad', 'qquad',
        'colon',
        'neq', 'leq', 'geq', 'approx', 'sim', 'equiv',
        'times', 'div', 'pm', 'mp',
        'circ', 'bullet',
        'csc', 'cot',
        'sinh', 'cosh', 'tanh',
        'log', 'lg',
        'min', 'max',
        'sup', 'inf',
        'limsup', 'liminf',
        'arccot',
        'Delta', 'nabla',
        'varepsilon', 'vartheta', 'varpi',
        'prod', 'coprod',
        'longrightarrow', 'rightarrow', 'Rightarrow',
        'longrightarrow', 'Leftarrow', 'Leftrightarrow',
        'longleftrightarrow',
        'implies',
        'iff',
        'subset', 'supset', 'subseteq', 'supseteq',
        'cup', 'cap',
        'in', 'notin',
        'emptyset', 'varnothing',
        'Re', 'Im',
        'aleph',
        'nabla', 'partial',
        'angle', 'triangle',
        'exists', 'forall',
        'neg', 'lor', 'land',
        'mid',
        'colon',
        'mod', 'pmod',
        'bmod',
        'binom',
        'choose',
        'atop',
        'underset', 'overset',
        'widetilde', 'widehat',
        'overline', 'underline',
        'vec',
        'dot', 'ddot',
        'tilde', 'hat', 'check', 'bar',
        'acute', 'grave', 'breve', 'dot',
        'mathrm', 'mathbf', 'mathit', 'mathbb', 'mathcal',
        'mathscr', 'mathfrak', 'mathsf',
        'rm', 'bf',
        'displaystyle', 'textstyle', 'scriptstyle',
        'scriptscriptstyle',
        'hfill', 'hspace',
        'vspace',
        'rule',
        'fbox', 'boxed',
        'makebox',
        'mbox',
        'raisebox',
        'resizebox',
        'scalebox',
        'rotatebox',
        'reflectbox',
        'color', 'textcolor', 'colorbox',
        'fcolorbox',
        'definecolor',
        'tiny', 'scriptsize', 'footnotesize', 'small',
        'normalsize', 'large', 'Large', 'LARGE', 'huge', 'Huge',
        'underline', 'overline',
        'sout', 'xout',
        'uwave', 'sout', 'xout', 'dashuline', 'dotuline',
        'textcircled',
        'romannumeral',
        'circled',
    ]
    
    # Check for common double-backslash patterns
    for cmd in ['int', 'frac', 'ln', 'sin', 'cos', 'tan', 'lim', 'displaystyle', 'lvert', 'rvert']:
        old = f'\\\\{cmd}'
        new = f'\\{cmd}'
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            fixes.append(f"\\\\{cmd}→\\{cmd} ({count}×)")
    
    # 2. Fix dx and dy without \, prefix (in math contexts)
    # Pattern: dx$ or dx\ where dx is a differential
    # We need to replace standalone dx/dy/dt/dh in math mode
    
    # Replace $...dx...$ -> $...\,dx...$ (inline math)
    # But be careful: don't replace "dx" when it's part of a word
    
    def fix_dx_inline(m):
        inner = m.group(1)
        # Replace dx that's preceded by something other than \,
        inner = re.sub(r'(?<!\\)(\s*)dx\b', r'\,dx', inner)
        inner = re.sub(r'(?<!\\)(\s*)dy\b', r'\,dy', inner)
        inner = re.sub(r'(?<!\\)(\s*)dt\b', r'\,dt', inner)
        inner = re.sub(r'(?<!\\)(\s*)dh\b', r'\,dh', inner)
        inner = re.sub(r'(?<!\\)(\s*)d\theta\b', r'\,d\\theta', inner)
        return '$' + inner + '$'
    
    # Fix in $$...$$ (display math) 
    def fix_dx_display(m):
        inner = m.group(1)
        inner = re.sub(r'(?<!\\)(\s*)dx\b', r'\,dx', inner)
        inner = re.sub(r'(?<!\\)(\s*)dy\b', r'\,dy', inner)
        inner = re.sub(r'(?<!\\)(\s*)dt\b', r'\,dt', inner)
        inner = re.sub(r'(?<!\\)(\s*)dh\b', r'\,dh', inner)
        inner = re.sub(r'(?<!\\)(\s*)d\theta\b', r'\,d\\theta', inner)
        return '$$' + inner + '$$'
    
    # Apply fixes to math blocks
    content = re.sub(r'\$([^$]+)\$', fix_dx_inline, content)
    content = re.sub(r'\$\$([^$]+)\$\$', fix_dx_display, content)
    
    # 3. Fix | inside table cells (replace | with \lvert...\rvert in LaTeX)
    lines = content.split('\n')
    new_lines = []
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        # Detect table rows
        is_table_row = stripped.startswith('|') and not stripped.startswith('|---')
        
        if is_table_row:
            # Split by | to get cells, but preserve leading/trailing |
            parts = line.split('|')
            new_parts = []
            for i, part in enumerate(parts):
                # Check if this part contains $...$ with | inside
                new_part = re.sub(
                    r'\$([^$]*?)\|([^$]*?)\|([^$]*?)\$',
                    lambda m: '$' + m.group(1) + '\\lvert' + m.group(2) + '\\rvert' + m.group(3) + '$',
                    part
                )
                new_parts.append(new_part)
            line = '|'.join(new_parts)
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # 4. Fix specific patterns like $|x|$ -> $\lvert x\rvert$ in non-table contexts too
    # Only for inline math
    def fix_abs_inline(m):
        inner = m.group(1)
        # Replace |...| with \lvert...\rvert
        inner = re.sub(r'(?<!\\)\|([^|]+?)\|', r'\\lvert\1\\rvert', inner)
        return '$' + inner + '$'
    
    content = re.sub(r'\$([^$]+)\$', fix_abs_inline, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Simplified diff counting
        diff_items = []
        
        # Count \,dx additions
        orig_thinspaces = original.count(r'\,dx')
        new_thinspaces = content.count(r'\,dx')
        if new_thinspaces > orig_thinspaces:
            diff_items.append(f"+\,dx ({new_thinspaces - orig_thinspaces}新增)")
        
        # Count \lvert additions
        orig_lvert = original.count(r'\lvert')
        new_lvert = content.count(r'\lvert')
        if new_lvert > orig_lvert:
            diff_items.append(f"|→\\lvert ({new_lvert - orig_lvert}新增)")
        
        # Count double backslash fixes
        db_count = 0
        for cmd in ['int', 'frac', 'ln', 'sin', 'cos', 'tan', 'lim']:
            orig_db = original.count(f'\\\\{cmd}')
            if orig_db > 0:
                db_count += orig_db
        
        if diff_items or db_count:
            diff_items.append(f"去\\\\命令 ({db_count}处)" if db_count else "")
            diff_items = [d for d in diff_items if d]
            return True, diff_items
        else:
            return True, ["其他LaTeX微调"]
    
    return False, []


def main():
    modified = {}
    
    for fname in target_files:
        fpath = os.path.join(CONCEPTS_DIR, fname)
        if not os.path.exists(fpath):
            print(f"⚠ NOT FOUND: {fname}")
            continue
        
        modified_flag, changes = fix_file(fpath)
        if modified_flag:
            modified[fname] = changes
            print(f"  ✅ {fname}: {', '.join(changes)}")
        else:
            print(f"  ○ {fname}: 无需修改")
    
    print(f"\n{'='*60}")
    print(f"总计修改: {len(modified)} / {len(target_files)} 张卡片")
    print(f"{'='*60}")
    for fname, changes in sorted(modified.items()):
        print(f"  • {fname}")
        for c in changes:
            print(f"      - {c}")

if __name__ == '__main__':
    main()
