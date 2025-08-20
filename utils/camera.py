"""
Camera utilities for IP Camera stream
"""

import cv2
import requests
import numpy as np
from typing import Tuple, Optional
import time

class IPCameraStream:
    """
    Class to handle IP Camera streaming from mobile devices
    """
    
    def __init__(self, ip_url: str, timeout: int = 10):
        """
        Initialize IP camera stream
        
        Args:
            ip_url: Base IP URL (e.g., http://192.168.1.100:8080)
            timeout: Connection timeout in seconds
        """
        self.ip_url = ip_url.rstrip('/')
        self.stream_url = f"{self.ip_url}/video"
        self.photo_url = f"{self.ip_url}/photo.jpg"
        self.cap = None
        self.timeout = timeout
        self.last_frame_time = time.time()
        
    def test_connection(self) -> bool:
        """
        Test connection to IP camera
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            response = requests.get(self.ip_url, timeout=self.timeout)
            if response.status_code == 200:
                print(f"✓ Successfully connected to IP camera at {self.ip_url}")
                return True
            else:
                print(f"✗ Received status code {response.status_code} from {self.ip_url}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection test failed: {e}")
            return False
    
    def connect(self) -> bool:
        """
        Connect to IP camera video stream
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Test basic connection first
            if not self.test_connection():
                print("Basic connection test failed, but trying video stream anyway...")
            
            # Try to connect to video stream
            self.cap = cv2.VideoCapture(self.stream_url)
            
            if not self.cap.isOpened():
                print(f"✗ Could not open video stream from {self.stream_url}")
                
                # Try alternative method with photo URL
                print("Trying alternative method with photo stream...")
                return self._setup_photo_stream()
            
            # Test if we can read a frame
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print("✗ Could not read frame from video stream")
                self.cap.release()
                return self._setup_photo_stream()
            
            print(f"✓ Video stream opened successfully from {self.stream_url}")
            print(f"Frame size: {frame.shape[1]}x{frame.shape[0]}")
            return True
            
        except Exception as e:
            print(f"✗ Error connecting to camera: {e}")
            return False
    
    def _setup_photo_stream(self) -> bool:
        """
        Setup photo streaming as alternative to video stream
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            # Test photo URL
            response = requests.get(self.photo_url, timeout=5)
            if response.status_code == 200:
                print(f"✓ Photo stream available at {self.photo_url}")
                self.cap = "photo_stream"  # Mark as photo stream mode
                return True
            else:
                print(f"✗ Photo stream not available (status: {response.status_code})")
                return False
        except Exception as e:
            print(f"✗ Photo stream setup failed: {e}")
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read frame from IP camera
        
        Returns:
            Tuple[bool, Optional[np.ndarray]]: (success, frame)
        """
        if self.cap is None:
            return False, None
        
        # Handle photo stream mode
        if self.cap == "photo_stream":
            return self._read_photo_frame()
        
        # Handle video stream mode
        try:
            ret, frame = self.cap.read()
            if ret and frame is not None:
                self.last_frame_time = time.time()
                return True, frame
            else:
                print("Failed to read frame from video stream")
                return False, None
        except Exception as e:
            print(f"Error reading frame: {e}")
            return False, None
    
    def _read_photo_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read frame from photo URL
        
        Returns:
            Tuple[bool, Optional[np.ndarray]]: (success, frame)
        """
        try:
            response = requests.get(self.photo_url, timeout=2)
            if response.status_code == 200:
                # Convert response content to numpy array
                img_array = np.frombuffer(response.content, np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                
                if frame is not None:
                    self.last_frame_time = time.time()
                    return True, frame
                else:
                    return False, None
            else:
                return False, None
        except Exception as e:
            print(f"Error reading photo frame: {e}")
            return False, None
    
    def get_camera_info(self) -> dict:
        """
        Get camera information
        
        Returns:
            dict: Camera information
        """
        info = {
            'ip_url': self.ip_url,
            'stream_url': self.stream_url,
            'photo_url': self.photo_url,
            'connected': self.cap is not None,
            'stream_type': 'video' if isinstance(self.cap, cv2.VideoCapture) else 'photo',
            'last_frame_time': self.last_frame_time
        }
        
        if isinstance(self.cap, cv2.VideoCapture) and self.cap.isOpened():
            info['width'] = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            info['height'] = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            info['fps'] = self.cap.get(cv2.CAP_PROP_FPS)
        
        return info
    
    def release(self):
        """
        Release camera resources
        """
        if isinstance(self.cap, cv2.VideoCapture):
            self.cap.release()
        self.cap = None
        print("Camera resources released")

class CameraManager:
    """
    Manager class for multiple camera sources
    """
    
    def __init__(self):
        self.cameras = {}
        self.active_camera = None
    
    def add_camera(self, name: str, camera: IPCameraStream):
        """Add a camera to the manager"""
        self.cameras[name] = camera
    
    def set_active_camera(self, name: str) -> bool:
        """Set the active camera"""
        if name in self.cameras:
            self.active_camera = name
            return True
        return False
    
    def get_active_camera(self) -> Optional[IPCameraStream]:
        """Get the active camera"""
        if self.active_camera and self.active_camera in self.cameras:
            return self.cameras[self.active_camera]
        return None
    
    def list_cameras(self) -> list:
        """List all available cameras"""
        return list(self.cameras.keys())
    
    def release_all(self):
        """Release all cameras"""
        for camera in self.cameras.values():
            camera.release()
        self.cameras.clear()
        self.active_camera = None
