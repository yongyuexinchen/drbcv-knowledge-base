"""Extract all docx course materials to text files for reference."""
import os
import glob
from docx import Document

base = r"C:\Users\53028\.hermes\desktop-attachments"
out_dir = r"D:\Contents\DRBCV-Knowledge\Data-Structures\Sources"
os.makedirs(out_dir, exist_ok=True)

files = sorted(glob.glob(os.path.join(base, "*原文*.docx")))
# Deduplicate by basename
seen = set()
unique = []
for f in files:
    bn = os.path.basename(f)
    if bn not in seen:
        seen.add(bn)
        unique.append(f)

print(f"Total unique files: {len(unique)}")

for f in unique:
    bn = os.path.basename(f).replace(".docx", ".txt")
    out_path = os.path.join(out_dir, bn)
    doc = Document(f)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    # Remove first line (title line) and timestamp line
    text_lines = [p for p in paragraphs if not p.startswith("2026年") and not p.startswith("发言人")]
    text = "\n\n".join(text_lines)
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write(text)
    print(f"  → {bn} ({len(text)} chars)")

print(f"\nDone. {len(unique)} files extracted to {out_dir}")
