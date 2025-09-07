#!/usr/bin/env python3

import subprocess
import sys

def main():
    print("🚀 Quick Start - YOLO v8 Object Detection")
    print("=" * 50)
    print("Starting object detection with default settings...")
    print("Make sure your IP Camera is running!")
    print()
    
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError:
        print("\n❌ Error running object detection")
        print("Try running: python main.py --ip YOUR_IP_ADDRESS")
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")

if __name__ == "__main__":
    main()
