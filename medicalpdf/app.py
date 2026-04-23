from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from extractor import PDFExtractor
import os
from werkzeug.utils import secure_filename

# Paths — templates and static are one level up from medicalpdf/
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(parent_dir, 'templates')
static_dir = os.path.join(parent_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

extractor = PDFExtractor()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    """Save uploaded file and return its path."""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath


def handle_error(e):
    """Return a clean JSON error response."""
    return jsonify({'success': False, 'error': str(e)}), 500


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})


@app.route('/api/extract', methods=['POST'])
def extract_data():
    """Extract text from an uploaded PDF or image."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if not file.filename or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid or unsupported file type'}), 400

        filepath = save_file(file)

        if filepath.lower().endswith('.pdf'):
            result = extractor.extract_from_pdf(filepath)
        else:
            result = extractor.extract_from_image(filepath)

        os.remove(filepath)
        return jsonify(result)

    except Exception as e:
        return handle_error(e)


@app.route('/api/extract-all', methods=['POST'])
def extract_all():
    """Extract text, tables, images and metadata from a PDF."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please upload a PDF file'}), 400

        filepath = save_file(file)
        result = extractor.extract_everything(filepath)
        os.remove(filepath)
        return jsonify(result)

    except Exception as e:
        return handle_error(e)


@app.route('/api/extract-tables', methods=['POST'])
def extract_tables():
    """Extract structured table data from a PDF."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please upload a PDF file'}), 400

        filepath = save_file(file)
        result = extractor.extract_tables_from_pdf(filepath)
        os.remove(filepath)
        return jsonify(result)

    except Exception as e:
        return handle_error(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)