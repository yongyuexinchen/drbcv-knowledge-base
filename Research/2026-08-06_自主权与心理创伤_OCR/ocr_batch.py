"""PaddleOCR 批量识别 258 页（ocr_venv 运行）"""
import os
os.environ['PYTHONPATH'] = ''
import glob, time
from paddleocr import PaddleOCR

PAGES = r"D:/Contents/research/2026-08-06_自主权与心理创伤_OCR/pages"
OUT = r"D:/Contents/research/2026-08-06_自主权与心理创伤_OCR/ocr"
os.makedirs(OUT, exist_ok=True)

ocr = PaddleOCR(
    lang='ch',
    use_doc_orientation_classify=False,  # 书是正立的，跳过方向分类提速
    use_doc_unwarping=False,
    use_textline_orientation=True,
)

pages = sorted(glob.glob(os.path.join(PAGES, "*.png")))
print(f"pages to OCR: {len(pages)}", flush=True)
t0 = time.time()
fail = []
for i, p in enumerate(pages):
    try:
        raw = ocr.predict(p)
        lines = []
        for item in raw:
            for t, s in zip(item.get('rec_texts', []), item.get('rec_scores', [])):
                if s >= 0.5:
                    lines.append(t)
        out = os.path.join(OUT, os.path.basename(p).replace('.png', '.txt'))
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        fail.append(os.path.basename(p))
        print(f"[FAIL] {os.path.basename(p)}: {e}", flush=True)
    if (i + 1) % 25 == 0:
        el = time.time() - t0
        print(f"progress {i+1}/{len(pages)} elapsed {el:.0f}s eta {el/(i+1)*(len(pages)-i-1):.0f}s", flush=True)

print(f"DONE {len(pages)-len(fail)}/{len(pages)} in {time.time()-t0:.0f}s, failed: {fail}", flush=True)
