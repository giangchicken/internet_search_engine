from fastapi import FastAPI, Query
from tools.search import *

app = FastAPI()


@app.get("/search/")
def search_ma_deals(deals: list[str] = Query(...), num_results: int = 5, lang: str = "vi", country: str = "VN"):
    """API tìm kiếm M&A trên Google."""
    return googlesearch_parallel(deals, num_results=num_results, lang=lang, country=country)

@app.get("/subdomains/")
def get_subdomains(urls: list[str] = Query(...)):
    """API trích xuất subdomains từ danh sách URL."""
    return extract_subdomains_parallel(urls)
