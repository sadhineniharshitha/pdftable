from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from extractor import PDFExtractor
import os
from werkzeug.utils import secure_filename

# Get the parent directory path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(parent_dir, 'templates')
static_dir = os.path.join(parent_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# Configuration
UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize PDF Extractor
# Set Tesseract path if needed (adjust path based on your installation)
extractor = PDFExtractor()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def extract_data():
    """Extract text from uploaded PDF or image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use PDF, PNG, JPG, etc.'}), 400
        
        # Save file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract data based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'pdf':
            result = extractor.extract_from_pdf(filepath)
        else:
            result = extractor.extract_from_image(filepath)
        
        # Clean up
        os.remove(filepath)
        
        if not result.get('success', False):
            error_msg = result.get('error', 'Unknown error')
            if 'poppler' in error_msg.lower():
                return jsonify({
                    'error': '⚠️ Poppler is not installed. ' +
                             'Download from: https://github.com/oschwartz10612/poppler-windows/releases/ ' +
                             'and extract to C:\\poppler'
                }), 500
            return jsonify(result), 500
        
        return jsonify(result)
    
    except Exception as e:
        error_msg = str(e)
        if 'poppler' in error_msg.lower():
            return jsonify({
                'error': '⚠️ Poppler is not installed. ' +
                         'Download from: https://github.com/oschwartz10612/poppler-windows/releases/ ' +
                         'and extract to C:\\poppler'
            }), 500
        return jsonify({'error': error_msg}), 500

@app.route('/api/extract-all', methods=['POST'])
def extract_all():
    """Extract everything from PDF: text, tables, images, metadata"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '' or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please upload a PDF file'}), 400
        
        # Save file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract everything
        result = extractor.extract_everything(filepath)
        
        # Clean up
        os.remove(filepath)
        
        if not result.get('success', False):
            error_msg = result.get('error', 'Unknown error')
            if 'poppler' in error_msg.lower():
                return jsonify({
                    'error': '⚠️ Poppler is not installed. ' +
                             'Download from: https://github.com/oschwartz10612/poppler-windows/releases/ ' +
                             'and extract to C:\\poppler'
                }), 500
            return jsonify(result), 500
        
        return jsonify(result)
    
    except Exception as e:
        error_msg = str(e)
        if 'poppler' in error_msg.lower():
            return jsonify({
                'error': '⚠️ Poppler is not installed. ' +
                         'Download from: https://github.com/oschwartz10612/poppler-windows/releases/ ' +
                         'and extract to C:\\poppler'
            }), 500
        return jsonify({'error': error_msg}), 500

@app.route('/api/extract-tables', methods=['POST'])
def extract_tables():
    """Extract structured table data from PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '' or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please upload a PDF file'}), 400
        
        # Save file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract tables
        result = extractor.extract_tables_from_pdf(filepath)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
