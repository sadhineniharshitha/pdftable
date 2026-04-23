import os, base64
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from extractor import extract_text, extract_tables, _pdf_to_images
from PIL import Image

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload(file):
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return path

def cleanup(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def attach_images(file_path, result):
    pages = result.get('pages', [])
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            images = _pdf_to_images(file_path, dpi=120)
        else:
            images = [Image.open(file_path)]
    except Exception:
        images = []
    for i, page in enumerate(pages):
        if i < len(images):
            buf = BytesIO()
            img = images[i].copy()
            img.thumbnail((400, 600))
            img.save(buf, format='PNG')
            page['image'] = base64.b64encode(buf.getvalue()).decode()
        else:
            page['image'] = None
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def api_extract():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    file = request.files['file']
    if not file.filename or not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type"}), 400
    path = save_upload(file)
    try:
        result = extract_text(path)
        if result.get('success'):
            result = attach_images(path, result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        cleanup(path)

@app.route('/api/extract-tables', methods=['POST'])
def api_extract_tables():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    file = request.files['file']
    if not file.filename or not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type"}), 400
    path = save_upload(file)
    try:
        result = extract_tables(path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        cleanup(path)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "ocr": "EasyOCR"})

if __name__ == '__main__':
    print("🚀 Starting Medical PDF Extractor...")
    print("📍 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
