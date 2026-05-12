FROM python:3.11-slim

# منع مشاكل buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# تثبيت dependencies الأول (أفضل للكاش)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# نسخ المشروع
COPY . .

# فتح بورت streamlit
EXPOSE 8501

# تشغيل التطبيق
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]