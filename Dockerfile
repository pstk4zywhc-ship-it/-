# استخدام نسخة بايثون رسمية ومستقرة تماماً
FROM python:3.11-slim

# تحديد مجلد العمل داخل السيرفر
WORKDIR /app

# نسخ ملف المكتبات أولاً لتثبيتها
COPY requirements.txt .

# تثبيت المكتبات المطلوبة للبوت
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات البوت (بما فيها قاعدة البيانات والكود)
COPY . .

# الأمر المسؤول عن تشغيل البوت
CMD ["python", "bot.py"]
