import fitz  # PyMuPDF only
import base64
import os
import re
from datetime import datetime


def page_to_base64(pdf_path, page_index):
    doc = fitz.open(pdf_path)
    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    img_bytes = pix.tobytes("png")
    doc.close()
    return base64.standard_b64encode(img_bytes).decode("utf-8")


def extract_text_all_methods(page):
    """Try every PyMuPDF method to get maximum text from a page."""
    results = []

    # Method 1: plain text
    t1 = page.get_text("text").strip()
    if t1: results.append(t1)

    # Method 2: blocks (gets more from complex layouts)
    blocks = page.get_text("blocks")
    t2 = "\n".join([b[4].strip() for b in blocks if b[4].strip()])
    if t2 and t2 not in results: results.append(t2)

    # Method 3: words (catches text missed by other methods)
    words = page.get_text("words")
    t3 = " ".join([w[4] for w in words if w[4].strip()])
    if t3 and len(t3) > len(max(results, default="", key=len)):
        results.append(t3)

    # Return the longest result (most complete)
    return max(results, default="", key=len)


class PDFExtractor:

    def extract_metadata(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            meta = doc.metadata
            result = {
                "title":        meta.get("title")    or "N/A",
                "author":       meta.get("author")   or "N/A",
                "subject":      meta.get("subject")  or "N/A",
                "creator":      meta.get("creator")  or "N/A",
                "producer":     meta.get("producer") or "N/A",
                "total_pages":  len(doc),
                "file_size_mb": round(os.path.getsize(pdf_path) / (1024 * 1024), 2),
                "extracted_at": datetime.now().isoformat()
            }
            doc.close()
            return result
        except Exception as e:
            return {"error": str(e)}

    def _get_page_text(self, pdf_path, page_index):
        doc = fitz.open(pdf_path)
        page = doc[page_index]
        text = extract_text_all_methods(page)
        doc.close()

        if len(text) > 10:
            return text, "native"
        return "(Scanned/handwritten page — see image on the right)", "image-only"

    def extract_from_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            total = len(doc)
            doc.close()
            full_text = ""
            for i in range(total):
                print(f"  Processing page {i+1}/{total}...")
                text, method = self._get_page_text(pdf_path, i)
                label = f"PAGE {i+1}" + (" [scanned]" if method == "image-only" else "")
                full_text += f"--- {label} ---\n{text}\n\n"
            return {"success": True, "text": full_text, "pages": total}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_everything(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            total = len(doc)
            doc.close()
            all_data = {
                "success": True,
                "metadata": self.extract_metadata(pdf_path),
                "total_pages": total,
                "pages": [],
                "extraction_time": datetime.now().isoformat()
            }
            for i in range(total):
                print(f"  Processing page {i+1}/{total}...")
                b64 = page_to_base64(pdf_path, i)
                text, method = self._get_page_text(pdf_path, i)
                table_rows = []
                for line in text.split("\n"):
                    if line.strip():
                        cells = re.split(r"\s{2,}", line.strip())
                        if len(cells) > 1:
                            table_rows.append(cells)
                all_data["pages"].append({
                    "page_number": i + 1,
                    "method": method,
                    "text": text,
                    "tables": table_rows,
                    "image": f"data:image/png;base64,{b64}",
                    "statistics": {
                        "text_length": len(text),
                        "lines": len([l for l in text.split("\n") if l.strip()]),
                        "tables_count": 1 if table_rows else 0
                    }
                })
            return all_data
        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_tables_from_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            total = len(doc)
            doc.close()
            tables_data = []
            for i in range(total):
                print(f"  Processing page {i+1}/{total}...")
                text, _ = self._get_page_text(pdf_path, i)
                table_rows = []
                for line in text.split("\n"):
                    if line.strip():
                        cells = re.split(r"\s{2,}", line.strip())
                        if len(cells) > 1:
                            table_rows.append(cells)
                if table_rows:
                    tables_data.append({"page": i + 1, "rows": table_rows})
            return {"success": True, "tables": tables_data, "pages": total}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_from_image(self, image_path):
        try:
            return {"success": True, "text": "(Image file — see UI to view)"}
        except Exception as e:
            return {"success": False, "error": str(e)}