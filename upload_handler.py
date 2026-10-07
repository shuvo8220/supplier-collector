"""
Image Upload Handler
Supports: Sample pics, product pics, factory pics, price list pics, document scans
"""
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path

# Upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create upload directories
UPLOAD_CATEGORIES = {
    'sample': 'uploads/samples',
    'product': 'uploads/products',
    'factory': 'uploads/factory',
    'price_list': 'uploads/price_lists',
    'document': 'uploads/documents',
    'catalog': 'uploads/catalogs'
}

def init_upload_folders():
    """Create upload directories if they don't exist"""
    for category, folder in UPLOAD_CATEGORIES.items():
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✓ Upload folders initialized")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    """Get file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(original_filename):
    """Generate unique filename with timestamp and UUID"""
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}.{ext}"

def save_uploaded_file(file, category, company_name=None):
    """
    Save uploaded file to appropriate category folder
    
    Args:
        file: FileStorage object from Flask request
        category: One of: sample, product, factory, price_list, document, catalog
        company_name: Optional company name for organizing files
    
    Returns:
        dict: {success: bool, filepath: str, error: str}
    """
    try:
        # Validate category
        if category not in UPLOAD_CATEGORIES:
            return {
                'success': False,
                'error': f'Invalid category. Must be one of: {list(UPLOAD_CATEGORIES.keys())}'
            }
        
        # Check if file exists
        if not file or file.filename == '':
            return {
                'success': False,
                'error': 'No file provided'
            }
        
        # Validate file extension
        if not allowed_file(file.filename):
            return {
                'success': False,
                'error': f'Invalid file type. Allowed: {ALLOWED_EXTENSIONS}'
            }
        
        # Generate unique filename
        unique_filename = generate_unique_filename(file.filename)
        
        # Get category folder
        category_folder = UPLOAD_CATEGORIES[category]
        
        # Add company subfolder if provided
        if company_name:
            safe_company_name = secure_filename(company_name)
            category_folder = os.path.join(category_folder, safe_company_name)
            Path(category_folder).mkdir(parents=True, exist_ok=True)
        
        # Full file path
        filepath = os.path.join(category_folder, unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Get file size
        file_size = os.path.getsize(filepath)
        
        return {
            'success': True,
            'filepath': filepath,
            'filename': unique_filename,
            'original_filename': file.filename,
            'size': file_size,
            'category': category
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def delete_uploaded_file(filepath):
    """Delete uploaded file"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return {'success': True}
        else:
            return {'success': False, 'error': 'File not found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_file_url(filepath):
    """Convert file path to URL for serving"""
    # Replace backslashes with forward slashes for web URLs
    return filepath.replace('\\', '/')

def validate_file_size(file):
    """Check if file size is within limit"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset file pointer
    return size <= MAX_FILE_SIZE

# Image processing utilities (optional, for future optimization)
def get_image_info(filepath):
    """Get image dimensions and metadata"""
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode
            }
    except ImportError:
        return {'error': 'PIL not installed'}
    except Exception as e:
        return {'error': str(e)}

def create_thumbnail(filepath, max_size=(300, 300)):
    """Create thumbnail of image (requires PIL)"""
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            img.thumbnail(max_size)
            thumb_path = filepath.rsplit('.', 1)[0] + '_thumb.' + filepath.rsplit('.', 1)[1]
            img.save(thumb_path)
            return {'success': True, 'thumbnail': thumb_path}
    except ImportError:
        return {'success': False, 'error': 'PIL not installed'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Initialize upload folders
    init_upload_folders()
    print("\n✓ Upload handler ready")
    print(f"✓ Allowed extensions: {ALLOWED_EXTENSIONS}")
    print(f"✓ Max file size: {MAX_FILE_SIZE / (1024*1024):.1f} MB")
    print(f"✓ Categories: {list(UPLOAD_CATEGORIES.keys())}")
