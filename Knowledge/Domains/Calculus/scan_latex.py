import os, re

os.chdir(os.path.join(os.path.dirname(__file__), "Concepts"))
files = sorted([f for f in os.listdir('.') if f.endswith('.md')])
targets = files[85:114]

print(f"Scanning {len(targets)} files (indices 85-113)...")
print()

for fname in targets:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    issues = []
    
    # Rule 1: double backslash in LaTeX commands like \\int, \\frac
    # Find patterns like \\\\int, \\\\frac, \\\\ln, \\\\lvert, etc.
    matches = re.findall(r'\\\\\\\\(?:int|frac|ln|lvert|sin|cos|tan|log|lim|sum|prod|int_|displaystyle)', content)
    if matches:
        issues.append(f'double backslash ({len(matches)} occurrences)')
    
    # Rule 3: |x| pattern inside LaTeX (not in tables)
    # Find inline math $...$ and display math $$...$$
    inline_math = re.findall(r'\$(?=[^\s])(?:[^$\n]*?)\$', content)
    for m in inline_math:
        # Check for |something| pattern that's NOT \lvert...\rvert
        if re.search(r'(?<![\\lL]vert)\|', m) and re.search(r'\|(?!\s)', m):
            # Check if it looks like absolute value
            if re.search(r'\|[a-zA-Z0-9_{}()^]+?\|', m):
                issues.append('pipe | in inline LaTeX (absolute value)')
                break
    
    # Check display math for |...| 
    display_math = re.findall(r'\$\$(?:[^$]|\n)*?\$\$', content, re.DOTALL)
    for dm in display_math:
        if re.search(r'(?<![\\lL]vert)\|', dm) and re.search(r'\|(?!\s)', dm):
            if re.search(r'\|[a-zA-Z0-9_{}()^]+?\|', dm):
                issues.append('pipe | in display LaTeX (absolute value)')
                break
    
    # Rule 4: missing +C on indefinite integrals
    # Find \int without bounds (indefinite) that doesn't have +C
    indef_count = len(re.findall(r'(?<!\w)\\int\b(?!_[a-zA-Z])', content))
    c_count = len(re.findall(r'\\\\,?\s*dx\s*=\s*[^$]+\+ ?C', content))
    
    if issues or fname == "等价无穷小替换.md":
        print(f"\n=== {fname} ===")
        if issues:
            for iss in issues:
                print(f"  ISSUE: {iss}")
        
        # Show specific issues for 等价无穷小替换.md
        if fname == "等价无穷小替换.md":
            # Count double backslashes
            dbl = re.findall(r'\\\\\\\\(?:int|frac|ln|sin|cos|tan|lim)', content)
            dbl2 = re.findall(r'\\\\\\\\(?:\\[|\\])', content)
            dbl3 = re.findall(r'\\\\\\\\(?:\(|\))', content)
            print(f"  Double backslash LaTeX commands: {len(dbl)}")
            print(f"  Double backslash brackets: {len(dbl2)}")
            print(f"  Double backslash parens: {len(dbl3)}")

print("\nDone scanning.")
