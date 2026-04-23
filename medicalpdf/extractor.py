import fitz
import re
import easyocr
import numpy as np
from PIL import Image

print("[EasyOCR] Loading...")
reader = easyocr.Reader(['en'], gpu=False)
print("[EasyOCR] Ready")

def _get_page_text(pdf_path, i):
    doc = fitz.open(pdf_path)
    native = doc[i].get_text("text").strip()
    if len(native) > 20:
        doc.close()
        return native, "native"
    pix = doc[i].get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    results = reader.readtext(np.array(img), detail=0, paragraph=True)
    text = "\n".join(results).strip()
    return (text or "(No text found)"), "ocr"

def extract_text(file_path):
    try:
        doc = fitz.open(file_path)
        total = len(doc)
        doc.close()
        pages = []
        for i in range(total):
            text, _ = _get_page_text(file_path, i)
            # Split into rows (lines) and columns (words separated by 2+ spaces)
            rows = [re.split(r"\s{2,}", l.strip()) for l in text.split("\n") if l.strip()]
            pages.append({"page": i+1, "rows": rows})
        return {"success": True, "pages": pages}
    except Exception as e:
        return {"success": False, "error": str(e)}

def extract_tables(file_path):
    return extract_text(file_path)  # unified, since rows are already table-like

def _pdf_to_images(pdf_path, dpi=120):
    doc = fitz.open(pdf_path)
    scale = dpi / 72
    imgs = []
    for p in doc:
        pix = p.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        imgs.append(img)
    doc.close()
    return imgs
