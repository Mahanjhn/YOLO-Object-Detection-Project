#!/usr/bin/env python3
"""
Setup script for YOLO v8 Object Detection Project
Installs all required packages
"""

import subprocess
import sys

def install_packages():
    """Install required packages"""
    print("📦 Installing required packages...")
    print("This may take a few minutes...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("\n✅ Installation completed successfully!")
        print("\nNext steps:")
        print("1. Setup your IP Camera (IP Webcam app)")
        print("2. Update IP address in config.py")
        print("3. Test camera: python test_camera.py")
        print("4. Run detection: python main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed: {e}")
        print("Try running manually: pip install -r requirements.txt")

def main():
    print("🚀 YOLO v8 Object Detection Setup")
    print("=" * 40)
    
    response = input("Install required packages? (y/N): ")
    if response.lower() in ['y', 'yes']:
        install_packages()
    else:
        print("Setup cancelled. You can install manually with:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
