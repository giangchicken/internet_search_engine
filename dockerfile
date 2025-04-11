# 1️⃣ Sử dụng Python 3.10-slim để tối ưu dung lượng
FROM python:3.10-slim

# 2️⃣ Cài đặt các gói hệ thống cần thiết
RUN apt update && apt install -y curl

# 3️⃣ Cài đặt thư viện Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Sao chép mã nguồn
COPY inference.py .

# 5️⃣ Mở cổng API & Chạy FastAPI
EXPOSE 8000
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8888"]
