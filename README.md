# PDF Scanned Document Extractor 📄

Extract text and data from scanned PDFs using OCR (Tesseract) and display results in a beautiful web interface.

## 🌟 Features

- **Text Extraction**: Extract all text from scanned PDFs and images using OCR
- **Table Parsing**: Automatically detect and extract table structures
- **Drag & Drop UI**: Easy file upload with visual feedback
- **Export Options**: Copy to clipboard or download as .txt
- **Multi-format Support**: PDF, PNG, JPG, BMP, TIFF
- **Real-time Processing**: See results immediately

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- Windows/Mac/Linux

### 2. Installation

```bash
# Clone or navigate to project directory
cd c:\Users\pinky\OneDrive\Desktop\pdftable

# Install Python dependencies
pip install -r medicalpdf/requirements.txt
```

### 3. Install System Dependencies

**Poppler (Required for PDF processing):**
- **Automated:** `python install_poppler_auto.py`
- **Manual:** Download from https://github.com/oschwartz10612/poppler-windows/releases/ and extract to `C:\poppler`

**Tesseract OCR (Optional but recommended for better text extraction):**
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Choose Windows installer and run

### 4. Run Application

```bash
cd medicalpdf
python app.py
```

Open browser: **http://localhost:5000**

## 📖 Usage

1. **Upload PDF:**
   - Drag & drop into the upload box OR
   - Click to browse and select

2. **Extract:**
   - Click "🔍 Extract Text" for OCR extraction
   - Click "📊 Extract Tables" for structured data

3. **Export:**
   - 📋 Copy to clipboard
   - ⬇️ Download as .txt
   - ✕ Clear for new file

## 📁 Project Structure

```
pdftable/
├── medicalpdf/
│   ├── app.py              # Flask backend
│   ├── extractor.py        # OCR extraction logic
│   └── requirements.txt
├── templates/
│   └── index.html          # Web UI
├── static/
│   ├── style.css
│   ├── script.js
│── uploads/                # Temporary file storage
├── install_poppler_auto.py # Auto-installer
└── SETUP_GUIDE.md          # Detailed setup instructions
```

## 🔧 Troubleshooting

### Error: "Poppler is not installed"
```bash
# Automated installation
python install_poppler_auto.py

# Or manual: download and extract to C:\poppler
```

### Error: "Tesseract is not installed"
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location: `C:\Program Files\Tesseract-OCR`

### Poor OCR Results
- Use scans with 300+ DPI
- Ensure good contrast (black text on white)
- Try uploading a clearer image

## 📊 API Endpoints

- `GET /` - Web interface
- `POST /api/extract` - Extract text from PDF/image
- `POST /api/extract-tables` - Extract table data from PDF

## 🛠️ Tech Stack

- **Backend:** Flask, Python
- **OCR:** Tesseract, pytesseract
- **PDF Processing:** pdf2image, Poppler
- **Frontend:** HTML5, CSS3, JavaScript
- **Images:** Pillow

## 📝 Requirements

See [requirements.txt](medicalpdf/requirements.txt)

## 💡 Tips

- **Large PDFs:** Processing takes ~2-5 seconds per page
- **File Size Limit:** 50MB max
- **Best Format:** Clean B&W scans, high contrast
- **Languages:** Tesseract supports 100+ languages

## 🎯 Next Steps

1. Install Poppler: `python install_poppler_auto.py`
2. Start app: `python medicalpdf/app.py`
3. Open: http://localhost:5000
4. Upload a sample scanned PDF!

## 📄 See Also

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
- [Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)
- [Poppler Windows](https://github.com/oschwartz10612/poppler-windows/releases)

---

**Created:** April 2026  
**Python Version:** 3.9+  
**License:** MIT
