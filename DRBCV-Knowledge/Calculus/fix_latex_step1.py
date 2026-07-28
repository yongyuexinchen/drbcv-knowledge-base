import os, re

os.chdir(os.path.join(os.path.dirname(__file__), "Concepts"))

# Fix 等价无穷小替换.md
fname = "等价无穷小替换.md"
with open(fname, 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences
print(f"=== {fname} ===")

# Replace \\[ and \\] (display math delimiters) with $$ and $$
before_count = content.count('\\\\[')
content = content.replace('\\\\[', '$$')
content = content.replace('\\\\]', '$$')
print(f"  Replaced \\\\[ -> $$: {before_count} occurrences")

# Replace \\( and \\) (inline math delimiters) with $ and $
before_count = content.count('\\\\(')
content = content.replace('\\(', '$')
content = content.replace('\\)', '$')
print(f"  Replaced \\( -> $: {before_count} occurrences")

# Fix double backslash in LaTeX commands: \\lim -> \lim, \\frac -> \frac, etc.
# These appear as \\\\lim, \\\\frac in the raw text (doubled due to escaping)
# Actually, after the above replacements, we need to check what remains
# Pattern: \\\\ followed by a letter = \\command
# In the raw text, \\\\[ became $$, so \\\\lim would be the remaining pattern

# Let's check: in the original file, \\( and \\) became $, and \\[ and \\] became $$
# But inside the math, there were also \\lim, \\frac, \\sin etc.
# After fixing the delimiters, those still have double backslashes

# Count remaining double backslashes in LaTeX commands
double_cmds = re.findall(r'\\\\\\\\[a-z]', content)
print(f"  Remaining double-backslash LaTeX commands: {len(double_cmds)}")
for cmd in set(double_cmds):
    print(f"    {cmd}: {double_cmds.count(cmd)} times")

# Fix common LaTeX commands with double backslash
for cmd in ['lim', 'frac', 'sin', 'cos', 'tan', 'ln', 'sim', 'to', 'cdot', 
            'int', 'infty', 'Rightarrow', 'alpha', 'beta', 'gamma',
            'text', 'quad', 'sqrt', 'lim_', 'log', 'max', 'min']:
    old = f'\\\\{cmd}'
    new = f'\\{cmd}'
    c = content.count(old)
    if c > 0:
        content = content.replace(old, new)
        print(f"  Replaced \\\\{cmd} -> \\{cmd}: {c} occurrences")

# Now check for any remaining \\ that should be single backslash
# This might also fix \\\\n (double backslash followed by letter)  
# But be careful: \\\\n in raw is \\n in displayed, which we want as \n
# Actually the \\\\ is the raw representation of \\, so we need to check

with open(fname, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"  Saved {fname}")
print()
