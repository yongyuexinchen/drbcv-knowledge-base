# -*- coding: utf-8 -*-
"""验收三张寻址卡：CRLF 统一 + 8 章节 + frontmatter + 生活映射 3 行"""
import os, re

base = r"D:/Contents/Knowledge/Domains/Computer-Organization/Concepts"
import sys
files = sys.argv[1:] if len(sys.argv) > 1 else [
    "编址方式与寻址空间.md", "指令寻址.md", "数据寻址方式.md",
]
sections = ["## 类型判定", "## 类比 ★", "## 生活映射", "## 是什么",
            "## 正例", "## 反例/边界", "## 详细解释", "## 关系", "## 备注"]

ok = True
for fn in files:
    p = os.path.join(base, fn)
    raw = open(p, "rb").read()
    # CRLF 统一
    s = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    if s != raw:
        open(p, "wb").write(s)
    text = s.decode("utf-8")
    text_n = re.sub(r"\r\n", "\n", text)  # 归一化后再验证
    print(f"== {fn}")
    # 8 章节
    for sec in sections:
        if sec not in text_n:
            print(f"  MISS {sec}"); ok = False
    # frontmatter
    fm = len(re.findall(r"^---$", text_n, re.M))
    print(f"  frontmatter 分隔符: {fm} (应为2), type: {re.search(r'^type: (.+)$', text_n, re.M).group(1)}")
    # 生活映射行数（## 类比 ★ 之后、## 是什么 之前）
    m = re.search(r"### 生活映射\n(.*?)\n## 是什么", text_n, re.S)
    total_rows = len(re.findall(r"^\|", m.group(1), re.M)) if m else -1
    rows = total_rows - 2 if total_rows > 0 else total_rows  # 去掉表头+分隔行
    print(f"  生活映射数据行: {rows} (应为3, 含表头共{total_rows})")
    if rows != 3: ok = False

print("ALL OK" if ok else "HAS ISSUES")
