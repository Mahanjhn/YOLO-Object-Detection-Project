"""
Simple IP Camera Connection Test
"""

import cv2
import requests
import argparse
from config import DEFAULT_IP


def test_ip_camera(ip_url):
    """Test IP camera connection and display video stream"""
    print(f"🔍 Testing IP camera: {ip_url}")
    print("-" * 50)
    
    # Test basic connection
    try:
        response = requests.get(ip_url, timeout=5)
        print(f"✅ Basic connection: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test video stream
    stream_url = f"{ip_url}/video"
    print(f"🎥 Testing video stream: {stream_url}")
    
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("❌ Failed to open video stream")
        return False
    
    print("✅ Video stream connected successfully!")
    print("Press 'q' to quit video test")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break
        
        # Display frame info
        height, width = frame.shape[:2]
        cv2.putText(frame, f"Resolution: {width}x{height}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('IP Camera Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Camera test completed")
    return True


def main():
    parser = argparse.ArgumentParser(description='Test IP Camera Connection')
    parser.add_argument('--ip', type=str, default=DEFAULT_IP,
                       help=f'IP camera URL (default: {DEFAULT_IP})')
    args = parser.parse_args()
    
    print("📱 IP Camera Connection Test")
    print("=" * 50)
    print("Make sure:")
    print("1. IP Webcam app is installed and running on your phone")
    print("2. Your phone and computer are on the same WiFi network")
    print("3. The IP address matches what's shown in the app")
    print()
    
    success = test_ip_camera(args.ip)
    
    if success:
        print("\n🎉 Camera test successful!")
        print("You can now run: python main.py")
    else:
        print("\n❌ Camera test failed!")
        print("Check your IP address and network connection")


if __name__ == "__main__":
    main()
