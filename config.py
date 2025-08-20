"""
Configuration file for YOLO Object Detection Project
"""

# Default IP Camera Settings
DEFAULT_IP = "http://25.21.207.192:8080"
DEFAULT_STREAM_URL = "/video"

# YOLO Model Settings
MODEL_NAME = "yolov5s"  # Can be yolov5s, yolov5m, yolov5l, yolov5x
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4

# Video Settings
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_FPS = 20

# Output Settings
OUTPUT_DIR = "outputs"
DEFAULT_OUTPUT_VIDEO = "detection_output.mp4"
FRAME_SAVE_FORMAT = "detection_frame_{timestamp}.jpg"

# Display Settings
BBOX_COLOR = (0, 255, 0)  # Green
BBOX_THICKNESS = 2
FONT_SCALE = 0.5
FONT_THICKNESS = 2
TEXT_COLOR = (0, 0, 0)  # Black
TEXT_BG_COLOR = (0, 255, 0)  # Green

# Performance Settings
MAX_FPS = 30
RESIZE_FRAME = True

# Classes that YOLO can detect (COCO dataset)
YOLO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
    'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
    'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]
