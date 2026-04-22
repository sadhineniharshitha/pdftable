#!/usr/bin/env python
"""
Setup script to download and configure Poppler for Windows
Run this script to install poppler-windows
"""

import os
import sys
import zipfile
import urllib.request
from pathlib import Path

def download_poppler():
    """Download poppler-windows"""
    print("📥 Downloading Poppler for Windows...")
    
    url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0/Release-24.08.0.zip"
    appdata = Path(os.environ['APPDATA']) / 'Local'
    zip_path = appdata / 'poppler.zip'
    extract_path = appdata / 'poppler'
    
    try:
        print(f"   URL: {url}")
        urllib.request.urlretrieve(url, str(zip_path))
        print("✓ Download complete")
        
        print("📦 Extracting Poppler...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(str(extract_path))
        print("✓ Extraction complete")
        
        # Update PATH
        bin_path = extract_path / 'Release-24.08.0' / 'Library' / 'bin'
        os.environ['PATH'] = str(bin_path) + os.pathsep + os.environ['PATH']
        
        print(f"✓ Poppler installed to: {bin_path}")
        print("✓ PATH updated successfully!")
        
        # Clean up
        zip_path.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nManual Installation:")
        print("1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/")
        print("2. Extract to: C:\\poppler")
        print("3. Restart the Flask app")
        return False

if __name__ == '__main__':
    success = download_poppler()
    sys.exit(0 if success else 1)
