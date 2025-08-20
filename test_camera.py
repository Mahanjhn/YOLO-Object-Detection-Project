"""
Quick test script for IP camera connection
"""

import cv2
import requests
import sys
import argparse

def test_ip_camera(ip_url):
    """Test IP camera connection"""
    print(f"Testing IP camera at: {ip_url}")
    print("-" * 50)
    
    # Test basic connection
    try:
        response = requests.get(ip_url, timeout=10)
        print(f"✓ Basic connection: Status {response.status_code}")
    except Exception as e:
        print(f"✗ Basic connection failed: {e}")
        return False
    
    # Test video stream
    stream_url = f"{ip_url}/video"
    print(f"Testing video stream: {stream_url}")
    
    cap = cv2.VideoCapture(stream_url)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            print(f"✓ Video stream working! Frame size: {frame.shape[1]}x{frame.shape[0]}")
            print("Press 'q' to quit the test window")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Add test info to frame
                cv2.putText(frame, "Camera Test - Press Q to quit", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"IP: {ip_url}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow('IP Camera Test', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            return True
        else:
            print("✗ Could not read frame from video stream")
    else:
        print("✗ Could not open video stream")
    
    # Test photo stream as alternative
    photo_url = f"{ip_url}/photo.jpg"
    print(f"Testing photo stream: {photo_url}")
    
    try:
        response = requests.get(photo_url, timeout=5)
        if response.status_code == 200:
            print("✓ Photo stream available")
            return True
        else:
            print(f"✗ Photo stream failed: Status {response.status_code}")
    except Exception as e:
        print(f"✗ Photo stream failed: {e}")
    
    return False

def main():
    parser = argparse.ArgumentParser(description='Test IP Camera Connection')
    parser.add_argument('--ip', type=str, default='http://25.21.207.192:8080',
                       help='IP camera URL')
    
    args = parser.parse_args()
    
    print("=== IP Camera Connection Test ===")
    print("Make sure your mobile IP Webcam app is running!")
    print("Default IP: http://25.21.207.192:8080")
    print()
    
    success = test_ip_camera(args.ip)
    
    if success:
        print("\n✓ Camera test successful! You can now run the main detection script.")
        print("Run: python main.py")
    else:
        print("\n✗ Camera test failed!")
        print("\nTroubleshooting:")
        print("1. Check if your phone and computer are on the same network")
        print("2. Make sure IP Webcam app is running and server is started")
        print("3. Check the IP address in the app")
        print("4. Disable firewall temporarily")
        print("5. Try: python test_camera.py --ip http://YOUR_IP:8080")

if __name__ == "__main__":
    main()
