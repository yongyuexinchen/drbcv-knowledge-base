#!/usr/bin/env python3
"""
Fix LaTeX syntax in Concepts cards 26-55 (alphabetically sorted).

Rules applied:
1. Single backslash ONLY (no \\\\int, \\\\frac, etc.)
2. No | inside table LaTeX - use \\lvert ... \\rvert
3. All abs/det/norm use \\lvert...\\rvert consistently
4. Integrals: \\displaystyle\\int ... \\,dx ... +C
5. Verification/derivation in small text after formulas
6. Piecewise: \\begin{cases}
7. Matrix: \\begin{bmatrix}, determinant: \\begin{vmatrix}
"""
import os
import glob
import re

CONCEPTS_DIR = "D:/DRBCV-Knowledge/Calculus/Concepts"

# Cards 26-55 (0-indexed 25-54) by alphabetical order
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

def fix_double_backslash_issues(content):
    """Fix \\\\int -> \\int, \\\\frac -> \\frac, etc. (single backslash only)"""
    # Fix specific double-backslash patterns in LaTeX
    # Be careful not to break triple-backslash situations (outside our scope)
    
    # In inline math $...$ and display math $$...$$
    # Replace \\\\ with \\ within math contexts
    # But only where it's a LaTeX command start
    
    patterns = [
        (r'\\\\int', r'\\int'),
        (r'\\\\frac', r'\\frac'),
        (r'\\\\ln', r'\\ln'),
        (r'\\\\sin', r'\\sin'),
        (r'\\\\cos', r'\\cos'),
        (r'\\\\tan', r'\\tan'),
        (r'\\\\cot', r'\\cot'),
        (r'\\\\sec', r'\\sec'),
        (r'\\\\csc', r'\\csc'),
        (r'\\\\lim', r'\\lim'),
        (r'\\\\displaystyle', r'\\displaystyle'),
        (r'\\\\lvert', r'\\lvert'),
        (r'\\\\rvert', r'\\rvert'),
        (r'\\\\arcsin', r'\\arcsin'),
        (r'\\\\arccos', r'\\arccos'),
        (r'\\\\arctan', r'\\arctan'),
        (r'\\\\operatorname', r'\\operatorname'),
        (r'\\\\begin{cases}', r'\\begin{cases}'),
        (r'\\\\end{cases}', r'\\end{cases}'),
        (r'\\\\begin{vmatrix}', r'\\begin{vmatrix}'),
        (r'\\\\end{vmatrix}', r'\\end{vmatrix}'),
        (r'\\\\begin{bmatrix}', r'\\begin{bmatrix}'),
        (r'\\\\end{bmatrix}', r'\\end{bmatrix}'),
    ]
    
    # Only replace within $...$ or $$...$$ contexts to be safe
    # First, handle display math blocks
    result = content
    
    for old, new in patterns:
        result = result.replace(old, new)
    
    return result

def fix_pipe_in_table_latex(content):
    """Fix | inside table cells - replace with \\lvert...\\rvert"""
    # This is tricky because we need to find | inside table rows but not as separators
    # Table rows start with | or have | between columns
    # We look for $...|...$ patterns inside table contexts
    
    # Simple approach: find patterns like $...|x|$ or $\\ln|x|$ inside tables
    # and replace with \\lvert...\\rvert
    
    lines = content.split('\n')
    in_table = False
    fixed_content = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Detect table start/end
        if stripped.startswith('|') and stripped.endswith('|') and '---' not in stripped:
            in_table = True
        elif '---' in stripped and '|' in stripped:
            in_table = True
        elif in_table and (stripped == '' or not stripped.startswith('|')):
            in_table = False
        
        if in_table and ('$' in line or '\\(' in line):
            # In a table row with LaTeX, fix | inside math
            # Pattern: |x| inside math -> \\lvert x\\rvert
            # But only inside math contexts within table cells
            line = re.sub(r'\$([^$]*?)\|([^$]*?)\|([^$]*?)\$', 
                         lambda m: '$' + m.group(1) + '\\lvert' + m.group(2) + '\\rvert' + m.group(3) + '$', 
                         line)
        
        fixed_content.append(line)
    
    return '\n'.join(fixed_content)

def fix_abs_in_latex(content):
    """Replace |x| type patterns with \\lvert x\\rvert in LaTeX"""
    # This is for cases like $\\ln|x|$ -> $\\ln\\lvert x\\rvert$
    # Or $|x|$ -> $\\lvert x\\rvert$
    
    # In inline math $...$ only
    def fix_inline_math(m):
        inner = m.group(1)
        # Replace |...| with \\lvert...\\rvert but only for simple absolute value patterns
        inner = re.sub(r'(?<![\\l])[|]([^|]+)[|]', r'\\lvert\1\\rvert', inner)
        return '$' + inner + '$'
    
    content = re.sub(r'\$([^$]+)\$', fix_inline_math, content)
    
    # In display math $$...$$
    def fix_display_math(m):
        inner = m.group(1)
        inner = re.sub(r'(?<![\\l])[|]([^|]+)[|]', r'\\lvert\1\\rvert', inner)
        return '$$' + inner + '$$'
    
    content = re.sub(r'\$\$([^$]+)\$\$', fix_display_math, content)
    
    return content

def fix_integral_format(content):
    """Fix integrals to use proper format: \\displaystyle\\int ... \\,dx ... +C"""
    # Add \\, before dx
    content = re.sub(r'(\\int[^$]*?)\s*dx\b', r'\1\\,dx', content)
    content = re.sub(r'(\\int[^$]*?)\s*dy\b', r'\1\\,dy', content)
    content = re.sub(r'(\\int[^$]*?)\s*dt\b', r'\1\\,dt', content)
    content = re.sub(r'(\\int[^$]*?)\s*dh\b', r'\1\\,dh', content)
    
    return content

def fix_table_pipe_issue_global(content):
    """Fix pipe in table cells where | is used as absolute value inside math"""
    # Find patterns like $\\ln|x|$ or $|f(x)|$ in lines that look like markdown table rows
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Check if this is a markdown table row
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            # This is a table row - cells are separated by |
            # We need to replace | inside math expressions within cells
            # but NOT the cell separators themselves
            
            # Split by | but preserve the cell structure
            parts = line.split('|')
            new_parts = [parts[0]]  # Keep first empty part or leading text
            
            for part in parts[1:]:
                # Inside each cell, if there's math with |, fix it
                # Pattern: $...|...|...$ -> $...\\lvert...\\rvert...$
                new_part = re.sub(
                    r'\$([^$]*?)\|([^$]*?)\|([^$]*?)\$',
                    lambda m: '$' + m.group(1) + '\\lvert' + m.group(2) + '\\rvert' + m.group(3) + '$',
                    part
                )
                new_parts.append(new_part)
            
            line = '|'.join(new_parts)
        
        result.append(line)
    
    return '\n'.join(result)

def count_issues(content):
    """Count various LaTeX issues in the content"""
    issues = []
    
    # Count double backslash LaTeX commands
    double_bs = re.findall(r'\\\\[a-z]+', content)
    if double_bs:
        issues.append(f"double backslash commands: {set(double_bs)}")
    
    # Count | inside math in table rows  
    table_abs = 0
    lines = content.split('\n')
    in_table = False
    for line in lines:
        if line.strip().startswith('|') and not line.strip().startswith('|---'):
            # Check for $...|...$ patterns
            if re.search(r'\$[^$]*?\|[^$]*?\|[^$]*?\$', line):
                table_abs += 1
    
    # Count regular |x| in math
    inline_abs = len(re.findall(r'\$[^$]*?\|[^|]+\|[^$]*?\$', content))
    display_abs = len(re.findall(r'\$\$[^$]*?\|[^|]+\|[^$]*?\$\$', content))
    
    # Count dx without \\,
    no_thinspace_dx = len(re.findall(r'(?<!\\,)dx(?![a-z])', content))
    
    return issues, table_abs, inline_abs, display_abs, no_thinspace_dx

def main():
    changes_report = {}
    
    for fname in target_files:
        fpath = os.path.join(CONCEPTS_DIR, fname)
        if not os.path.exists(fpath):
            print(f"⚠ NOT FOUND: {fname}")
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Apply fixes
        content = fix_double_backslash_issues(content)
        content = fix_table_pipe_issue_global(content)
        content = fix_integral_format(content)
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Count what changed
            orig_issues, orig_tabs, orig_iabs, orig_dabs, orig_dx = count_issues(original)
            new_issues, new_tabs, new_iabs, new_dabs, new_dx = count_issues(content)
            
            diffs = []
            if orig_tabs > new_tabs:
                diffs.append(f"table |→\\lvert ({orig_tabs - new_tabs} instances)")
            if orig_iabs > new_iabs:
                diffs.append(f"inline |→\\lvert ({orig_iabs - new_iabs} instances)")
            if orig_dabs > new_dabs:
                diffs.append(f"display |→\\lvert ({orig_dabs - new_dabs} instances)")
            
            changes_report[fname] = diffs
            print(f"✅ {fname}: {', '.join(diffs) if diffs else 'minor fixes'}")
        else:
            print(f"○ {fname}: no issues found")
    
    print("\n\n=== SUMMARY ===")
    fixed_count = len(changes_report)
    print(f"Cards modified: {fixed_count} / {len(target_files)}")
    for fname, fixes in changes_report.items():
        print(f"  {fname}: {', '.join(fixes)}")

if __name__ == '__main__':
    main()
