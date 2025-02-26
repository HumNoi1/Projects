FROM python:3.11.9-slim

WORKDIR /app

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# สร้างโฟลเดอร์สำหรับอัปโหลดไฟล์
RUN mkdir -p uploads

# ทำการเริ่มต้นระบบ
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]