@echo off
echo ===================================
echo YOLO Object Detection Setup
echo ===================================

echo Installing required packages...
echo.

pip install --upgrade pip

echo Installing PyTorch...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo Installing other requirements...
pip install -r requirements.txt

echo.
echo ===================================
echo Installation completed!
echo ===================================
echo.
echo To test your camera:
echo python test_camera.py
echo.
echo To run object detection:
echo python main.py
echo.
pause
