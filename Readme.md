# 📌 Hướng Dẫn Sử Dụng API Search & Subdomain Extraction

## 1️⃣ Build Docker Image
```bash
docker build -t search_engine .
```

## 2️⃣ Chạy Container
```bash
docker run --rm -p 8000:8888 search_engine
```

## 3️⃣ Gọi API
### 🔹 Dùng curl
```bash
curl "http://127.0.0.1:8000/search/?deals=VinFast IPO&Masan mua lại Phúc Long&num_results=5"
```
### 🔹 Dùng Python (requests)
```bash
import requests

params = {
    "deals": ["VinFast IPO", "Masan mua lại Phúc Long"],
    "num_results": 5
}

response = requests.get("http://127.0.0.1:8888/search/", params=params)
print(response.json())

```

## 4️⃣ Gọi API Lấy Subdomains
### 🔹 Dùng curl
```bash
curl "http://127.0.0.1:8000/subdomains/?urls=https://vnexpress.net&urls=https://tuoitre.vn"
```
### 🔹 Dùng Python (requests)
```bash
import requests

params = {
    "urls": ["https://vnexpress.net", "https://tuoitre.vn"]
}

response = requests.get("http://127.0.0.1:8000/subdomains/", params=params)
print(response.json())

```

