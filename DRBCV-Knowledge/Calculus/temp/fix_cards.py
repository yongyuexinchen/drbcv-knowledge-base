#!/usr/bin/env python3
"""Quick fix: update specific problematic concept cards."""
import glob
import os

CONCEPTS_DIR = "D:/DRBCV-Knowledge/Calculus/Concepts"

# Cards that need IO/analogy fixes
fixes = {}

# 定积分中值定理 - fix IO and analogy
fixes["定积分中值定理.md"] = [
    ("- **输入**: 函数 $f(x)$（被积函数）\n- **输出**: 原函数族 $F(x)+C$（不定积分）或数值（定积分）\n- **映射关系**: 求导运算的逆映射",
     "- **输入**: 闭区间 $[a,b]$ 上的连续函数 $f(x)$\n- **输出**: 存在 $\\xi \\in [a,b]$ 使 $\\int_a^b f(x)\\,dx = f(\\xi)(b-a)$\n- **映射关系**: 连续函数 → 某点函数值等于积分平均值"),
    ("积分就像把一根绳子切成小段再拼回去——整体由无数微小部分累加而成。",
     "中值定理就像期末考试——老师用全班平均分证明至少有一个人考了平均分。"),
    ("| $\\int_a^b f(x)\\,dx$ | 把图形切成无数细条再求和 |",
     "| $\\int_a^b f(x)\\,dx = f(\\xi)(b-a)$ | 全班总分 = 平均分 × 人数 |"),
    ("| $f(x_i)\\Delta x_i$ | 第 $i$ 个细条的面积 |",
     "| $f(\\xi)$ | 至少有一个人的分数等于平均分 |"),
    ("| $\\Delta x \\to 0$ | 细条越来越细，数量越来越多 |",
     "| $b-a$ | 全班人数 |"),
]

for fname, changes in fixes.items():
    fpath = os.path.join(CONCEPTS_DIR, fname)
    if not os.path.exists(fpath):
        print(f"NOT FOUND: {fpath}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in changes:
        if old in content:
            content = content.replace(old, new)
            print(f"  FIXED in {fname}: {old[:40]}...")
        else:
            print(f"  NOT FOUND in {fname}: {old[:40]}...")
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("\nDone fixing specific cards.")