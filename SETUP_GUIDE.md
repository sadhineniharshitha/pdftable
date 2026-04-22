# 🎯 PDF Scanned Document Extractor - Setup Guide

## ✅ What's Been Done

Your Flask application is running with:
- ✓ OCR text extraction using Tesseract
- ✓ Table data parsing
- ✓ Beautiful web UI with drag-and-drop
- ✓ Export functionality

**App Running At:** http://localhost:5000

---

## ⚠️ IMPORTANT: Install Poppler (Required)

**Error:** "Unable to get page count. Is poppler installed and in PATH?"

This error means Poppler is not installed. Poppler is needed to convert PDFs to images for OCR processing.

### 📥 Installation Steps

#### **Option 1: Quick Manual Download (Recommended)**

1. **Download Poppler:**
   - Visit: https://github.com/oschwartz10612/poppler-windows/releases/
   - Download the latest **Release-X.X.X.zip** file
   - Example: `Release-24.08.0.zip`

2. **Extract to C:\poppler:**
   - Right-click the ZIP file
   - Select "Extract All..."
   - Extract to: `C:\poppler`
   - After extraction, you should have: `C:\poppler\Release-24.08.0\Library\bin\pdftoppm.exe`

3. **Add Poppler to Windows PATH:**
   
   **Method A: Using Settings (Easiest)**
   - Press `Windows Key + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables" button
   - Under "User variables for [YourName]", click "New"
   - Variable name: `PATH`
   - Variable value: `C:\poppler\Release-24.08.0\Library\bin`
   - Click "OK" three times
   - **Restart your computer** or restart the terminal

   **Method B: Using PowerShell**
   ```powershell
   [Environment]::SetEnvironmentVariable('PATH', 'C:\poppler\Release-24.08.0\Library\bin;' + [Environment]::GetEnvironmentVariable('PATH', 'User'), 'User')
   ```

4. **Verify Installation:**
   - Open Command Prompt or PowerShell
   - Type: `pdftoppm -v`
   - Should show version information

5. **Restart Flask App:**
   - Stop the terminal running Flask (Ctrl+C)
   - Run: `python app.py` again
   - Reload the browser: http://localhost:5000

---

## 🚀 How to Use

1. **Open:** http://localhost:5000

2. **Upload PDF:**
   - Drag and drop a scanned PDF onto the upload area, OR
   - Click the upload box to browse and select a file

3. **Extract:**
   - Click **"🔍 Extract Text"** to get all text from the PDF
   - Click **"📊 Extract Tables"** to extract structured table data

4. **Download Results:**
   - Click 📋 to copy extracted text to clipboard
   - Click ⬇️ to download as .txt file
   - Click ✕ to clear and upload a new file

---

## 📋 System Requirements

- **Python 3.9+** ✓
- **Flask** ✓
- **Tesseract OCR** (for reading text from images)
- **Poppler** (for PDF to image conversion) ← **NEEDS INSTALLATION**
- **pdf2image** ✓
- **Pillow** ✓
- **pytesseract** ✓

---

## 🔧 Troubleshooting

### Error: "Unable to get page count. Is poppler installed and in PATH?"
**Solution:** Install Poppler (see Installation Steps above)

### Error: "Tesseract is not installed"
**Solution:** Download from https://github.com/UB-Mannheim/tesseract/wiki
- Choose Windows installer
- Install to default location: `C:\Program Files\Tesseract-OCR`

### App won't start
**Solution:** 
- Check all packages are installed: `pip install -r medicalpdf/requirements.txt`
- Verify you're in the right directory: `c:\Users\pinky\OneDrive\Desktop\pdftable\medicalpdf`

### Extracted text is gibberish
**Solution:** 
- The PDF quality may be too low
- Try adjusting image preprocessing
- Tesseract works better with cleaner scans (>300 DPI)

---

## 📂 Project Structure

```
pdftable/
├── medicalpdf/
│   ├── app.py              # Flask backend
│   ├── extractor.py        # OCR logic
│   └── requirements.txt     # Python packages
├── templates/
│   └── index.html          # Web UI
├── static/
│   ├── style.css           # Styling
│   └── script.js           # JavaScript
└── uploads/                # Temp file storage
```

---

## 💡 Tips

- **Better OCR Results:**
  - Use scans with at least 300 DPI
  - Ensure good contrast (not too light/dark)
  - Black text on white background works best

- **Large PDFs:**
  - Max file size: 50MB
  - Processing time depends on page count
  - Each page takes ~2-5 seconds

---

## 🎉 You're All Set!

Once you **install Poppler**, everything should work perfectly!

Questions? Check the terminal output for detailed error messages.
