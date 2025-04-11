import requests
import os
import multiprocessing
import json
import time
import random

def fetch_and_save_html(index_url_tuple, save_dir="html_pages", mapping_filename="mapping.json"):
    """Tải HTML từ URL và lưu với tên dạng page_{index}.html, đồng thời cập nhật mapping.json."""
    import shutil
    index, url = index_url_tuple
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(random.uniform(5, 10))
        response.raise_for_status()

        # Tạo thư mục nếu chưa có
        os.makedirs(save_dir, exist_ok=True)

        # Tạo tên file html
        filename = f"page_{index+1}.html"
        filepath = os.path.join(save_dir, filename)

        # Ghi file HTML
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Đường dẫn mapping.json
        mapping_path = os.path.join(save_dir, mapping_filename)

        # Tải hoặc khởi tạo file mapping
        mapping = {}
        if os.path.exists(mapping_path):
            try:
                with open(mapping_path, "r", encoding="utf-8") as mf:
                    mapping = json.load(mf)
            except json.JSONDecodeError as e:
                print(f"⚠️ mapping.json bị lỗi: {e}")
                # Backup file lỗi
                shutil.copy(mapping_path, mapping_path + ".bak")
                print(f"🛟 Đã sao lưu file lỗi thành {mapping_path}.bak")
                mapping = {}

        # Cập nhật và ghi lại
        mapping[url] = {
            "filename": filename
        }
        with open(mapping_path, "w", encoding="utf-8") as mf:
            json.dump(mapping, mf, ensure_ascii=False, indent=2)

        return (url, filename)

    except Exception as e:
        return (url, f"Error: {e}")

# def download_html_and_save_mapping(urls, save_dir="html_pages", mapping_file="mapping.json", num_workers=4):
#     """Tải HTML từ các URL và lưu ánh xạ URL -> tên file."""
#     indexed_urls = list(enumerate(urls))

#     with multiprocessing.Pool(num_workers) as pool:
#         results = pool.map(fetch_and_save_html, indexed_urls)

#     # Lọc kết quả thành công để lưu mapping
#     mapping = {url: filename for url, filename in results if not filename.startswith("Error")}

#     # Lưu mapping ra file JSON
#     os.makedirs(save_dir, exist_ok=True)
#     with open(os.path.join(save_dir, mapping_file), "w", encoding="utf-8") as f:
#         json.dump(mapping, f, ensure_ascii=False, indent=2)

#     return results
