#!/usr/bin/env python3
"""
Automated Poppler Installer for Windows
Downloads and installs poppler-windows, then updates PATH
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import urllib.request
import urllib.error
import zipfile

def download_file(url, dest_file, timeout=30):
    """Download file with progress indication"""
    print(f"📥 Downloading from: {url}")
    try:
        urllib.request.urlretrieve(url, dest_file)
        print(f"✓ Download complete: {dest_file}")
        return True
    except urllib.error.URLError as e:
        print(f"❌ Download failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_poppler():
    """Main setup function"""
    print("=" * 60)
    print("🔧 Poppler Installer for Windows")
    print("=" * 60)
    print()
    
    # Poppler version and URL
    POPPLER_VERSION = "24.08.0"
    DOWNLOAD_URL = f"https://github.com/oschwartz10612/poppler-windows/releases/download/v{POPPLER_VERSION}/Release-{POPPLER_VERSION}.zip"
    
    # Installation paths
    install_dir = Path("C:") / "poppler"
    extract_dir = install_dir / f"Release-{POPPLER_VERSION}"
    bin_dir = extract_dir / "Library" / "bin"
    
    print(f"Installation directory: {install_dir}")
    print(f"Poppler version: {POPPLER_VERSION}")
    print()
    
    # Step 1: Create directory
    print("📁 Creating installation directory...")
    try:
        install_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory ready: {install_dir}")
    except Exception as e:
        print(f"❌ Failed to create directory: {e}")
        print(f"   Try running as Administrator")
        return False
    
    # Step 2: Download
    print()
    print("📥 Downloading Poppler...")
    zip_file = install_dir / f"Release-{POPPLER_VERSION}.zip"
    
    if not download_file(DOWNLOAD_URL, str(zip_file)):
        # Try alternate URL
        alt_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0/Release-24.08.0.zip"
        print("   Trying alternate URL...")
        if not download_file(alt_url, str(zip_file)):
            print()
            print("❌ Download failed. Manual installation required:")
            print(f"   1. Visit: {DOWNLOAD_URL}")
            print(f"   2. Download Release-{POPPLER_VERSION}.zip")
            print(f"   3. Extract to: {install_dir}")
            return False
    
    # Step 3: Extract
    print()
    print("📦 Extracting Poppler...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(str(install_dir))
        print(f"✓ Extracted successfully")
        zip_file.unlink()  # Remove zip file
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False
    
    # Step 4: Verify
    print()
    print("✓ Verifying installation...")
    pdftoppm = bin_dir / "pdftoppm.exe"
    if pdftoppm.exists():
        print(f"✓ Found: {pdftoppm}")
    else:
        print(f"❌ Not found: {pdftoppm}")
        return False
    
    # Step 5: Update PATH
    print()
    print("🔗 Adding to Windows PATH...")
    try:
        path_value = str(bin_dir)
        current_path = os.environ.get('PATH', '')
        
        if path_value not in current_path:
            # Update user PATH
            os.system(f'setx PATH "{path_value};{current_path}"')
            print(f"✓ PATH updated: {path_value}")
        else:
            print(f"✓ Already in PATH: {path_value}")
    except Exception as e:
        print(f"⚠️  Could not update PATH automatically: {e}")
        print(f"   Manual update required:")
        print(f"   Add to PATH: {bin_dir}")
    
    # Success!
    print()
    print("=" * 60)
    print("✅ POPPLER INSTALLATION COMPLETE!")
    print("=" * 60)
    print()
    print("📝 Next Steps:")
    print("1. Close this terminal")
    print("2. Open a NEW terminal (to reload PATH)")
    print("3. Restart Flask app: python app.py")
    print("4. Reload browser: http://localhost:5000")
    print()
    
    return True

if __name__ == '__main__':
    try:
        success = setup_poppler()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
