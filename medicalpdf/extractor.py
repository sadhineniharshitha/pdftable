import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import re
import sys
import io
import base64
from datetime import datetime

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

# Try to find poppler in common locations
poppler_paths = [
    r"C:\poppler\Library\bin",
    r"C:\Program Files\poppler\Library\bin",
    r"C:\Program Files (x86)\poppler\Library\bin",
    os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'poppler', 'Release-24.08.0', 'Library', 'bin'),
]

def setup_poppler():
    """Setup poppler path if it exists in common locations"""
    for path in poppler_paths:
        if os.path.exists(path):
            os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
            return True
    return False

setup_poppler()

class PDFExtractor:
    def __init__(self, tesseract_path=None):
        """Initialize the PDF extractor with optional Tesseract path"""
        if tesseract_path:
            pytesseract.pytesseract.pytesseract_cmd = tesseract_path
    
    def extract_metadata(self, pdf_path):
        """Extract PDF metadata"""
        try:
            if not HAS_PYPDF2:
                return {}
            
            metadata = {}
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                if reader.metadata:
                    metadata = {
                        'title': reader.metadata.get('/Title', 'N/A'),
                        'author': reader.metadata.get('/Author', 'N/A'),
                        'subject': reader.metadata.get('/Subject', 'N/A'),
                        'creator': reader.metadata.get('/Creator', 'N/A'),
                        'producer': reader.metadata.get('/Producer', 'N/A'),
                        'created': str(reader.metadata.get('/CreationDate', 'N/A')),
                        'modified': str(reader.metadata.get('/ModDate', 'N/A')),
                    }
            return metadata
        except Exception as e:
            return {'error': str(e)}
    
    def extract_images_from_pdf(self, pdf_path):
        """Extract images from PDF pages"""
        try:
            images = convert_from_path(pdf_path)
            images_data = []
            
            for page_num, image in enumerate(images, 1):
                # Convert PIL image to base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                images_data.append({
                    'page': page_num,
                    'image': f'data:image/png;base64,{img_base64}',
                    'width': image.width,
                    'height': image.height,
                    'format': 'PNG'
                })
            
            return {
                'success': True,
                'images': images_data,
                'total_pages': len(images)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_everything(self, pdf_path):
        """Comprehensive extraction: text, tables, images, metadata"""
        try:
            images = convert_from_path(pdf_path)
            all_data = {
                'success': True,
                'pages': [],
                'metadata': self.extract_metadata(pdf_path),
                'total_pages': len(images),
                'file_size_mb': os.path.getsize(pdf_path) / (1024 * 1024),
                'extraction_time': datetime.now().isoformat()
            }
            
            for page_num, image in enumerate(images, 1):
                page_data = {
                    'page_number': page_num,
                    'text': '',
                    'tables': [],
                    'image': None,
                    'statistics': {
                        'text_length': 0,
                        'lines': 0,
                        'tables_count': 0
                    }
                }
                
                # Extract text using OCR
                text = pytesseract.image_to_string(image)
                page_data['text'] = text
                page_data['statistics']['text_length'] = len(text)
                page_data['statistics']['lines'] = len([l for l in text.split('\n') if l.strip()])
                
                # Extract tables
                lines = text.strip().split('\n')
                table_rows = []
                for line in lines:
                    if line.strip():
                        cells = re.split(r'\s{2,}', line.strip())
                        if len(cells) > 1:
                            table_rows.append(cells)
                
                if table_rows:
                    page_data['tables'] = table_rows
                    page_data['statistics']['tables_count'] = 1
                
                # Convert image to base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                page_data['image'] = f'data:image/png;base64,{img_base64}'
                
                all_data['pages'].append(page_data)
            
            return all_data
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_from_pdf(self, pdf_path):
        """Extract text from a scanned PDF"""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            extracted_text = ""
            
            for page_num, image in enumerate(images, 1):
                # Extract text using OCR
                text = pytesseract.image_to_string(image)
                extracted_text += f"--- PAGE {page_num} ---\n{text}\n\n"
            
            return {
                "success": True,
                "text": extracted_text,
                "pages": len(images)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_tables_from_pdf(self, pdf_path):
        """Extract table-like data from scanned PDF"""
        try:
            images = convert_from_path(pdf_path)
            tables_data = []
            
            for page_num, image in enumerate(images, 1):
                text = pytesseract.image_to_string(image)
                lines = text.strip().split('\n')
                
                # Parse lines as table rows
                table_rows = []
                for line in lines:
                    if line.strip():
                        # Split by multiple spaces (common in scanned tables)
                        cells = re.split(r'\s{2,}', line.strip())
                        if len(cells) > 1:
                            table_rows.append(cells)
                
                if table_rows:
                    tables_data.append({
                        "page": page_num,
                        "rows": table_rows
                    })
            
            return {
                "success": True,
                "tables": tables_data,
                "pages": len(images)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_from_image(self, image_path):
        """Extract text from an image directly"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            return {
                "success": True,
                "text": text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
