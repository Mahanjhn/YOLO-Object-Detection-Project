# YOLO Object Detection with IP Camera

این پروژه امکان تشخیص اشیاء در زمان واقعی با استفاده از دوربین موبایل و الگوریتم YOLO را فراهم می‌کند.

## ویژگی‌ها

- تشخیص اشیاء در زمان واقعی با YOLO v5
- استفاده از دوربین موبایل از طریق IP Camera
- نمایش تعداد اشیاء تشخیص داده شده
- محاسبه FPS
- امکان ذخیره ویدئو
- امکان ذخیره فریم‌ها

## نصب و راه‌اندازی

### 1. نصب پکیج‌های مورد نیاز

```bash
pip install -r requirements.txt
```

### 2. راه‌اندازی دوربین موبایل

1. برنامه IP Webcam را روی موبایل نصب کنید
2. برنامه را اجرا کرده و Start Server را بزنید
3. IP address ارائه شده را یادداشت کنید (مثال: http://25.21.207.192:8080)

### 3. اجرای پروژه

#### اجرای ساده:
```bash
python main.py
```

#### با تنظیمات سفارشی:
```bash
python main.py --ip http://YOUR_IP:8080 --conf 0.6 --save --output my_video.mp4
```

## پارامترهای قابل تنظیم

- `--ip`: آدرس IP دوربین (پیش‌فرض: http://25.21.207.192:8080)
- `--conf`: آستانه اطمینان (پیش‌فرض: 0.5)
- `--nms`: آستانه NMS (پیش‌فرض: 0.4)
- `--save`: ذخیره ویدئو خروجی
- `--output`: نام فایل خروجی (پیش‌فرض: output.mp4)

## کلیدهای میانبر

- `q`: خروج از برنامه
- `s`: ذخیره فریم فعلی

## عیب‌یابی

### خطای اتصال به دوربین:
1. اطمینان حاصل کنید که موبایل و کامپیوتر در یک شبکه هستند
2. IP address را بررسی کنید
3. فایروال را غیرفعال کنید

### خطای نصب torch:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### خطای OpenCV:
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python
```

## مثال‌های استفاده

### اجرا با IP مختلف:
```bash
python main.py --ip http://192.168.1.100:8080
```

### تنظیم حساسیت بالا:
```bash
python main.py --conf 0.3
```

### ذخیره ویدئو:
```bash
python main.py --save --output detection_output.mp4
```

## نتایج

پروژه قادر است اشیاء مختلف از جمله:
- افراد (Person)
- ماشین (Car)
- دوچرخه (Bicycle)
- حیوانات (Cat, Dog, Bird)
- و 80 کلاس دیگر...

را با دقت بالا تشخیص دهد.

## ساختار پروژه

```
YOLO-Object-Detection-Project/
├── main.py              # فایل اصلی برنامه
├── requirements.txt     # پکیج‌های مورد نیاز
├── README.md           # راهنمای استفاده
├── config.py           # تنظیمات پروژه
└── utils/              # توابع کمکی
    ├── __init__.py
    ├── camera.py       # کلاس‌های مربوط به دوربین
    └── detector.py     # کلاس‌های تشخیص
```

## مشارکت

برای مشارکت در این پروژه:
1. Fork کنید
2. یک branch جدید ایجاد کنید
3. تغییرات خود را commit کنید
4. Pull request ارسال کنید

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.
