"""
YOLO detector utilities
"""

import cv2
import torch
import numpy as np
import time
from typing import List, Tuple, Dict, Any
import sys

class YOLODetector:
    """
    YOLO object detection class using YOLOv5
    """
    
    def __init__(self, 
                 model_name: str = "yolov5s", 
                 conf_threshold: float = 0.5, 
                 nms_threshold: float = 0.4,
                 device: str = "auto"):
        """
        Initialize YOLO detector
        
        Args:
            model_name: YOLOv5 model name (yolov5s, yolov5m, yolov5l, yolov5x)
            conf_threshold: Confidence threshold for detections
            nms_threshold: Non-Maximum Suppression threshold
            device: Device to run inference on ('cpu', 'cuda', 'auto')
        """
        self.model_name = model_name
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold
        self.device = self._setup_device(device)
        self.model = None
        self.class_names = []
        
        # Performance tracking
        self.inference_times = []
        self.total_detections = 0
        
        self._load_model()
    
    def _setup_device(self, device: str) -> str:
        """Setup computation device"""
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                print("✓ CUDA available, using GPU")
            else:
                device = "cpu"
                print("✓ Using CPU for inference")
        
        print(f"Device: {device}")
        return device
    
    def _load_model(self):
        """Load YOLO model"""
        try:
            print(f"Loading {self.model_name} model...")
            
            # Load model from torch hub
            self.model = torch.hub.load('ultralytics/yolov5', self.model_name, pretrained=True)
            
            # Configure model
            self.model.conf = self.conf_threshold
            self.model.iou = self.nms_threshold
            self.model.to(self.device)
            
            # Get class names
            self.class_names = self.model.names
            
            print(f"✓ {self.model_name} model loaded successfully!")
            print(f"✓ Model can detect {len(self.class_names)} classes")
            print(f"✓ Running on: {self.device}")
            
        except Exception as e:
            print(f"✗ Error loading YOLO model: {e}")
            print("Make sure you have internet connection for first-time model download")
            sys.exit(1)
    
    def detect_objects(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Detect objects in frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dict containing detection results
        """
        start_time = time.time()
        
        try:
            # Run inference
            results = self.model(frame)
            
            # Parse results
            detections = results.pandas().xyxy[0]
            
            # Calculate inference time
            inference_time = time.time() - start_time
            self.inference_times.append(inference_time)
            
            # Keep only last 100 inference times for average calculation
            if len(self.inference_times) > 100:
                self.inference_times.pop(0)
            
            self.total_detections += len(detections)
            
            return {
                'detections': detections,
                'inference_time': inference_time,
                'num_detections': len(detections),
                'frame_shape': frame.shape
            }
            
        except Exception as e:
            print(f"Error in object detection: {e}")
            return {
                'detections': [],
                'inference_time': 0,
                'num_detections': 0,
                'frame_shape': frame.shape
            }
    
    def draw_detections(self, frame: np.ndarray, results: Dict[str, Any]) -> np.ndarray:
        """
        Draw detection results on frame
        
        Args:
            frame: Input frame
            results: Detection results from detect_objects()
            
        Returns:
            Frame with drawn detections
        """
        frame_copy = frame.copy()
        detections = results['detections']
        
        # Color map for different classes
        colors = self._generate_colors(len(self.class_names))
        
        for idx, detection in detections.iterrows():
            x1, y1, x2, y2 = int(detection['xmin']), int(detection['ymin']), \
                           int(detection['xmax']), int(detection['ymax'])
            confidence = detection['confidence']
            class_id = int(detection['class'])
            class_name = detection['name']
            
            # Get color for this class
            color = colors[class_id % len(colors)]
            
            # Draw bounding box
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)
            
            # Prepare label
            label = f"{class_name}: {confidence:.2f}"
            
            # Get text size
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Draw label background
            cv2.rectangle(frame_copy, 
                         (x1, y1 - text_height - baseline - 10), 
                         (x1 + text_width, y1), 
                         color, -1)
            
            # Draw label text
            cv2.putText(frame_copy, label, (x1, y1 - baseline - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame_copy
    
    def _generate_colors(self, num_classes: int) -> List[Tuple[int, int, int]]:
        """Generate colors for different classes"""
        np.random.seed(42)  # For consistent colors
        colors = []
        for i in range(num_classes):
            color = tuple(np.random.randint(0, 255, 3).tolist())
            colors.append(color)
        return colors
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get detection statistics"""
        avg_inference_time = np.mean(self.inference_times) if self.inference_times else 0
        fps = 1.0 / avg_inference_time if avg_inference_time > 0 else 0
        
        return {
            'total_detections': self.total_detections,
            'avg_inference_time': avg_inference_time,
            'estimated_fps': fps,
            'num_classes': len(self.class_names),
            'model_name': self.model_name,
            'device': self.device
        }
    
    def get_class_names(self) -> List[str]:
        """Get list of class names the model can detect"""
        return list(self.class_names.values()) if isinstance(self.class_names, dict) else self.class_names
    
    def update_thresholds(self, conf_threshold: float = None, nms_threshold: float = None):
        """Update detection thresholds"""
        if conf_threshold is not None:
            self.conf_threshold = conf_threshold
            self.model.conf = conf_threshold
            print(f"Confidence threshold updated to: {conf_threshold}")
        
        if nms_threshold is not None:
            self.nms_threshold = nms_threshold
            self.model.iou = nms_threshold
            print(f"NMS threshold updated to: {nms_threshold}")

class DetectionTracker:
    """
    Simple object tracking for detections
    """
    
    def __init__(self, max_disappeared: int = 10):
        """
        Initialize tracker
        
        Args:
            max_disappeared: Maximum frames an object can be lost before being removed
        """
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared
    
    def register(self, centroid: Tuple[int, int], detection_info: Dict):
        """Register a new object"""
        self.objects[self.next_object_id] = {
            'centroid': centroid,
            'info': detection_info
        }
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1
    
    def deregister(self, object_id: int):
        """Deregister an object"""
        del self.objects[object_id]
        del self.disappeared[object_id]
    
    def update(self, detections: List[Dict]) -> Dict[int, Dict]:
        """
        Update tracker with new detections
        
        Args:
            detections: List of detection dictionaries
            
        Returns:
            Dictionary of tracked objects
        """
        # If no detections, mark all as disappeared
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects
        
        # Calculate centroids for new detections
        input_centroids = []
        for detection in detections:
            cx = int((detection['xmin'] + detection['xmax']) / 2)
            cy = int((detection['ymin'] + detection['ymax']) / 2)
            input_centroids.append((cx, cy))
        
        # If no existing objects, register all detections as new
        if len(self.objects) == 0:
            for i, centroid in enumerate(input_centroids):
                self.register(centroid, detections[i])
        else:
            # Match existing objects with new detections
            object_centroids = [obj['centroid'] for obj in self.objects.values()]
            object_ids = list(self.objects.keys())
            
            # Compute distance matrix
            D = np.linalg.norm(np.array(object_centroids)[:, np.newaxis] - 
                             np.array(input_centroids), axis=2)
            
            # Find minimum distance matches
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            used_row_indices = set()
            used_col_indices = set()
            
            for (row, col) in zip(rows, cols):
                if row in used_row_indices or col in used_col_indices:
                    continue
                
                # Update object
                object_id = object_ids[row]
                self.objects[object_id]['centroid'] = input_centroids[col]
                self.objects[object_id]['info'] = detections[col]
                self.disappeared[object_id] = 0
                
                used_row_indices.add(row)
                used_col_indices.add(col)
            
            # Handle unmatched detections and objects
            unused_row_indices = set(range(0, D.shape[0])).difference(used_row_indices)
            unused_col_indices = set(range(0, D.shape[1])).difference(used_col_indices)
            
            # Mark unmatched objects as disappeared
            for row in unused_row_indices:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            # Register new objects
            for col in unused_col_indices:
                self.register(input_centroids[col], detections[col])
        
        return self.objects
