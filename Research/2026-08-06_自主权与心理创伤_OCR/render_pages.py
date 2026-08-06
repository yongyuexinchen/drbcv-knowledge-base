"""渲染 PDF 258 页为灰度 PNG（200 DPI）"""
import pymupdf, os, time

src = r"C:/Users/53028/Desktop/个人/自主权与心理创伤.pdf"
outdir = r"D:/Contents/research/2026-08-06_自主权与心理创伤_OCR/pages"
os.makedirs(outdir, exist_ok=True)

t0 = time.time()
doc = pymupdf.open(src)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200, colorspace=pymupdf.csGRAY)
    pix.save(os.path.join(outdir, f"p{i+1:03d}.png"))
    if (i + 1) % 50 == 0:
        print(f"rendered {i+1}/{doc.page_count} {time.time()-t0:.0f}s", flush=True)
print(f"DONE rendered {doc.page_count} pages in {time.time()-t0:.0f}s")
