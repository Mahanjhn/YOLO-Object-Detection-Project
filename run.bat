@echo off
title YOLO Object Detection with IP Camera

echo ===================================
echo YOLO Object Detection
echo ===================================
echo.

echo Starting object detection with your IP camera...
echo Make sure your IP Webcam app is running!
echo.

python main.py --ip http://25.21.207.192:8080

echo.
echo Detection stopped.
pause
