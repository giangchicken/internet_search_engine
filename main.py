from tools.download_html import fetch_and_save_html
from tools.search import fetch_search_results
import pandas as pd
import os
import json
import time

if __name__ == "__main__":
    # Đọc file Excel chứa danh sách nghị định
    df = pd.read_excel("./resolutions.xlsx")
    df["Ngày hiệu lực"] = pd.to_datetime(df["Ngày hiệu lực"], format="%d/%m/%Y", errors="coerce")
    df["Nghị định số"] = df["Nghị định số"].astype(str)

    # Lọc nghị định có hiệu lực trước 2006
    df = df[(df["Ngày hiệu lực"] > "2005-01-01")]

    # Lấy danh sách nghị định và nội dung
    NDS = df["Nghị định số"].tolist()
    Content = df["Nội dung"].tolist()
    active_date = df["Ngày hiệu lực"].tolist()

    # Thư mục lưu HTML và mapping
    save_dir = "html_pages"
    mapping_filename = "mapping.json"

    # Duyệt từng nghị định
    for idx, (nd, content, date) in enumerate(zip(NDS, Content, active_date)):
        print(f"\n🔍 Đang xử lý: {nd} - {content[:50]}...")

        try:
            # Tìm kiếm Google
            deal, urls = fetch_search_results(deal=nd, context=content, num_results=5, lang="vi")
            thuvienphapluat_urls = [url for url in urls if "thuvienphapluat" in url]

            if not thuvienphapluat_urls:
                print("⚠️ Không tìm thấy URL thuvienphapluat.")
                print(urls)
                continue
            
            

            # Tải URL đầu tiên thỏa mãn
            index_url_tuple = (idx, thuvienphapluat_urls[0])
            result = fetch_and_save_html(index_url_tuple, save_dir=save_dir, mapping_filename=mapping_filename)
            print(f"✅ Đã lưu: {result[1]} cho URL: {result[0]}")
            url, filename = result

            # Sau khi fetch xong thì ghi thêm active_date vào mapping
            mapping_path = os.path.join(save_dir, mapping_filename)

            try:
                with open(mapping_path, "r", encoding="utf-8") as mf:
                    mapping = json.load(mf)
                    mapping[url]["active_date"] = str(date)  # date là biến tương ứng từ vòng lặp

                    with open(mapping_path, "w", encoding="utf-8") as mf:
                        json.dump(mapping, mf, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"❌ Lỗi khi cập nhật active_date cho {url}: {e} : {date}")

        except Exception as e:
            print(f"❌ Lỗi khi xử lý {nd}: {e}")

    # # In đường dẫn tuyệt đối đến thư mục lưu
    # abs_path = os.path.abspath(save_dir)
    # print(f"\n📁 HTML pages và mapping.json đã lưu tại: {abs_path}")
