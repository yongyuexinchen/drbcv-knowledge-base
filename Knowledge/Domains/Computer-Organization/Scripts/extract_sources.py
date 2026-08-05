# -*- coding: utf-8 -*-
"""批量提取计组 docx 原文 → DRBCV-Knowledge/Computer-Organization/Sources/*.md"""
from docx import Document
import os, glob, re

SRC = r"D:\download"
OUT = r"D:\Contents\DRBCV-Knowledge\Computer-Organization\Sources"
os.makedirs(OUT, exist_ok=True)

# 计组文件：两位编号（02-91）开头，排除 FastAPI / 行列式 / 数据结构三位编号
pat = re.compile(r"^(0[2-9]|[1-8][0-9]|9[01]) ")
files = []
for f in sorted(glob.glob(os.path.join(SRC, "*.docx"))):
    bn = os.path.basename(f)
    m = pat.match(bn)
    if m and "_原文" in bn:
        files.append(f)

print(f"匹配到 {len(files)} 个计组文件")

ok, fail = 0, []
for f in files:
    bn = os.path.basename(f).replace(".docx", ".md")
    out_path = os.path.join(OUT, bn)
    if os.path.exists(out_path):
        ok += 1
        continue
    try:
        doc = Document(f)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        text_lines = [
            p for p in paragraphs
            if not re.match(r"^\d{4}[-\/]", p) and not p.startswith("发言人")
        ]
        text = "\n\n".join(text_lines)
        with open(out_path, "w", encoding="utf-8") as fout:
            fout.write(text)
        ok += 1
    except Exception as e:
        fail.append((bn, str(e)))

print(f"成功: {ok}, 失败: {len(fail)}")
for bn, err in fail:
    print(f"  FAIL {bn}: {err}")

# 验证：统计输出文件数和总行数
out_files = glob.glob(os.path.join(OUT, "*.md"))
print(f"\nSources 目录共 {len(out_files)} 个 .md 文件")
total_lines = sum(sum(1 for _ in open(p, encoding="utf-8")) for p in out_files)
print(f"总行数: {total_lines}")
