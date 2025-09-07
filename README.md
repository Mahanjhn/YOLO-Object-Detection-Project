# Simple YOLO v8 Object Detection with IP Camera

پروژه ساده و بهینه شده برای تشخیص اشیاء در زمان واقعی با استفاده از YOLO v8 و دوربین موبایل.

## ویژگی‌ها

✅ تشخیص اشیاء در زمان واقعی با **YOLO v8**  
✅ استفاده از دوربین موبایل به عنوان IP Camera  
✅ نمایش FPS و اطلاعات تشخیص  
✅ ساختار ساده و قابل فهم  

## نصب و راه‌اندازی

### 1. نصب پکیج‌ها
```bash
pip install -r requirements.txt
```

### 2. راه‌اندازی دوربین موبایل
1. برنامه **IP Webcam** را از Google Play نصب کنید
2. برنامه را اجرا کرده و **Start Server** را بزنید  
3. IP address نمایش داده شده را یادداشت کنید (مثل: `http://192.168.1.100:8080`)
4. آدرس IP را در فایل `config.py` تغییر دهید

### 3. تست اتصال
```bash
python test_camera.py --ip http://YOUR_IP:8080
```

### 4. اجرای تشخیص اشیاء
```bash
# اجرای ساده
python main.py

# با IP سفارشی
python main.py --ip http://YOUR_IP:8080

# با آستانه اطمینان سفارشی
python main.py --conf 0.6
```

## پارامترها

- `--ip`: آدرس IP دوربین (پیش‌فرض: مقدار در config.py)
- `--conf`: آستانه اطمینان (پیش‌فرض: 0.5)

## فایل‌های پروژه

- `main.py` - برنامه اصلی تشخیص اشیاء
- `test_camera.py` - تست اتصال دوربین  
- `config.py` - تنظیمات پروژه
- `requirements.txt` - پکیج‌های مورد نیاز

## کلیدهای کنترل

- `q` - خروج از برنامه

## مشکلات رایج

**❌ اتصال به دوربین ناموفق:**
- مطمئن شوید موبایل و کامپیوتر در شبکه یکسان هستند
- IP address را بررسی کنید
- فایروال را غیرفعال کنید

**❌ FPS پایین:**
- از مدل `yolov8n.pt` (nano) استفاده کنید
- رزولوشن دوربین را کاهش دهید
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
