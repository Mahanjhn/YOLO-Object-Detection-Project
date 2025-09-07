import cv2
import argparse
import time
from ultralytics import YOLO
from config import DEFAULT_IP, MODEL_NAME, CONFIDENCE_THRESHOLD


class SimpleYOLODetector:
    def __init__(self, model_name=MODEL_NAME, conf_threshold=CONFIDENCE_THRESHOLD):
        print(f"Loading YOLO v8 model: {model_name}")
        self.model = YOLO(model_name)
        self.conf_threshold = conf_threshold
        self.fps_counter = 0
        self.start_time = time.time()
    
    def detect_objects(self, frame):
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        return results[0]
    
    def draw_detections(self, frame, result):
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                
                class_name = self.model.names[cls]
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                label = f"{class_name}: {conf:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                             (x1 + label_size[0], y1), (0, 255, 0), -1)
                cv2.putText(frame, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return frame
    
    def calculate_fps(self):
        self.fps_counter += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 1.0:
            fps = self.fps_counter / elapsed_time
            self.fps_counter = 0
            self.start_time = time.time()
            return fps
        return 0


def connect_to_camera(ip_url):
    print(f"Connecting to IP camera: {ip_url}")
    stream_url = f"{ip_url}/video"
    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        print("❌ Failed to connect to IP camera")
        print("Make sure:")
        print("1. IP Webcam app is running on your phone")
        print("2. Phone and computer are on same network")
        print(f"3. IP address is correct: {ip_url}")
        return None
    
    print("✅ Successfully connected to IP camera")
    return cap


def main():
    parser = argparse.ArgumentParser(description='Simple YOLO v8 Object Detection')
    parser.add_argument('--ip', type=str, default=DEFAULT_IP, 
                       help=f'IP camera URL (default: {DEFAULT_IP})')
    parser.add_argument('--conf', type=float, default=CONFIDENCE_THRESHOLD, 
                       help=f'Confidence threshold (default: {CONFIDENCE_THRESHOLD})')
    args = parser.parse_args()
    
    detector = SimpleYOLODetector(conf_threshold=args.conf)
    
    cap = connect_to_camera(args.ip)
    if cap is None:
        return
    
    print("\n🎯 Starting object detection...")
    print("Press 'q' to quit")
    print("-" * 40)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to read frame")
                break
            
            result = detector.detect_objects(frame)
            
            frame = detector.draw_detections(frame, result)
            
            fps = detector.calculate_fps()
            if fps > 0:
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            cv2.imshow('YOLO v8 Object Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Detection stopped by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Cleanup completed")


if __name__ == "__main__":
    main()
