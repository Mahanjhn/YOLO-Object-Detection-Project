"""
YOLO Object Detection with IP Camera
Uses mobile camera via IP webcam app
Enhanced version with better error handling and features
"""

import cv2
import numpy as np
import time
import argparse
import sys
import os
from pathlib import Path

# Import our custom modules
from utils.camera import IPCameraStream
from utils.detector import YOLODetector
import config

def display_info(frame, detector_stats, camera_info, detection_results):
    """Display information overlay on frame"""
    # FPS and detection info
    fps = detector_stats.get('estimated_fps', 0)
    num_detections = detection_results.get('num_detections', 0)
    inference_time = detection_results.get('inference_time', 0)
    
    # Add text overlays
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Objects: {num_detections}", (10, 70), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Inference: {inference_time*1000:.1f}ms", (10, 110), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Camera info
    stream_type = camera_info.get('stream_type', 'unknown')
    cv2.putText(frame, f"Stream: {stream_type}", (10, 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return frame

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='YOLO Object Detection with IP Camera')
    parser.add_argument('--ip', type=str, default=config.DEFAULT_IP, 
                       help=f'IP camera URL (default: {config.DEFAULT_IP})')
    parser.add_argument('--conf', type=float, default=config.CONFIDENCE_THRESHOLD, 
                       help=f'Confidence threshold (default: {config.CONFIDENCE_THRESHOLD})')
    parser.add_argument('--nms', type=float, default=config.NMS_THRESHOLD, 
                       help=f'NMS threshold (default: {config.NMS_THRESHOLD})')
    parser.add_argument('--model', type=str, default=config.MODEL_NAME, 
                       help=f'YOLO model name (default: {config.MODEL_NAME})')
    parser.add_argument('--save', action='store_true', 
                       help='Save output video')
    parser.add_argument('--output', type=str, default=config.DEFAULT_OUTPUT_VIDEO, 
                       help=f'Output video filename (default: {config.DEFAULT_OUTPUT_VIDEO})')
    parser.add_argument('--width', type=int, default=config.DEFAULT_WIDTH, 
                       help=f'Frame width (default: {config.DEFAULT_WIDTH})')
    parser.add_argument('--height', type=int, default=config.DEFAULT_HEIGHT, 
                       help=f'Frame height (default: {config.DEFAULT_HEIGHT})')
    
    args = parser.parse_args()
    
    print("=== YOLO Object Detection with IP Camera ===")
    print(f"Camera IP: {args.ip}")
    print(f"Model: {args.model}")
    print(f"Confidence threshold: {args.conf}")
    print(f"NMS threshold: {args.nms}")
    print(f"Frame size: {args.width}x{args.height}")
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Save current frame")
    print("  '+' - Increase confidence threshold")
    print("  '-' - Decrease confidence threshold")
    print("=" * 50)
    
    # Create output directory
    if args.save:
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(config.OUTPUT_DIR, args.output)
    else:
        output_path = args.output
    
    # Initialize YOLO detector
    print("Initializing YOLO detector...")
    detector = YOLODetector(
        model_name=args.model,
        conf_threshold=args.conf, 
        nms_threshold=args.nms
    )
    
    # Initialize IP camera
    print("Connecting to IP camera...")
    camera = IPCameraStream(args.ip)
    
    if not camera.connect():
        print("✗ Failed to connect to IP camera. Exiting...")
        print("\nTroubleshooting:")
        print("1. Make sure IP Webcam app is running on your phone")
        print("2. Check if phone and computer are on same network")
        print("3. Try running: python test_camera.py")
        return
    
    # Get camera info
    camera_info = camera.get_camera_info()
    print(f"✓ Camera connected: {camera_info['stream_type']} stream")
    
    # Initialize video writer if saving output
    writer = None
    if args.save:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, config.DEFAULT_FPS, 
                               (args.width, args.height))
        print(f"✓ Video will be saved to: {output_path}")
    
    # Performance tracking
    frame_count = 0
    start_time = time.time()
    
    try:
        print("✓ Starting detection... Press 'q' to quit")
        
        while True:
            # Read frame from IP camera
            ret, frame = camera.read_frame()
            
            if not ret:
                print("Warning: Failed to read frame from camera")
                time.sleep(0.1)
                continue
            
            # Resize frame
            if config.RESIZE_FRAME:
                frame = cv2.resize(frame, (args.width, args.height))
            
            # Detect objects
            detection_results = detector.detect_objects(frame)
            
            # Draw detections
            frame_with_detections = detector.draw_detections(frame, detection_results)
            
            # Get statistics
            detector_stats = detector.get_statistics()
            
            # Add information overlay
            frame_with_detections = display_info(
                frame_with_detections, detector_stats, camera_info, detection_results
            )
            
            # Save frame if required
            if writer is not None:
                writer.write(frame_with_detections)
            
            # Display frame
            cv2.imshow('YOLO Object Detection - IP Camera', frame_with_detections)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save current frame
                timestamp = int(time.time())
                frame_path = os.path.join(
                    config.OUTPUT_DIR if args.save else ".",
                    config.FRAME_SAVE_FORMAT.format(timestamp=timestamp)
                )
                os.makedirs(os.path.dirname(frame_path), exist_ok=True)
                cv2.imwrite(frame_path, frame_with_detections)
                print(f"✓ Frame saved: {frame_path}")
            elif key == ord('+') or key == ord('='):
                # Increase confidence threshold
                new_conf = min(detector.conf_threshold + 0.05, 0.95)
                detector.update_thresholds(conf_threshold=new_conf)
                print(f"Confidence threshold: {new_conf:.2f}")
            elif key == ord('-'):
                # Decrease confidence threshold
                new_conf = max(detector.conf_threshold - 0.05, 0.05)
                detector.update_thresholds(conf_threshold=new_conf)
                print(f"Confidence threshold: {new_conf:.2f}")
            
            frame_count += 1
            
            # Print statistics every 100 frames
            if frame_count % 100 == 0:
                elapsed_time = time.time() - start_time
                avg_fps = frame_count / elapsed_time
                stats = detector.get_statistics()
                print(f"Processed {frame_count} frames, "
                      f"Average FPS: {avg_fps:.1f}, "
                      f"Total detections: {stats['total_detections']}")
    
    except KeyboardInterrupt:
        print("\n✓ Interrupted by user")
    
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("Cleaning up...")
        camera.release()
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()
        
        # Final statistics
        total_time = time.time() - start_time
        if frame_count > 0:
            print(f"\nFinal Statistics:")
            print(f"Total frames processed: {frame_count}")
            print(f"Total time: {total_time:.1f} seconds")
            print(f"Average FPS: {frame_count/total_time:.1f}")
            
            stats = detector.get_statistics()
            print(f"Total detections: {stats['total_detections']}")
            print(f"Average inference time: {stats['avg_inference_time']*1000:.1f}ms")
        
        print("✓ Cleanup completed")

if __name__ == "__main__":
    main()
