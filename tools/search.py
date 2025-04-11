from googlesearch import search
import requests
from bs4 import BeautifulSoup
import tldextract
import multiprocessing


def fetch_search_results(deal, context="thương vụ mua bán sáp nhập", **kwargs):
    """Tìm kiếm thương vụ M&A trên Google."""
    query = f"{context} {deal}"
    return deal, list(search(query, **kwargs))

def googlesearch_parallel(deals, num_workers=4, **kwargs):
    """Tìm kiếm nhiều thương vụ M&A song song bằng multiprocessing."""
    with multiprocessing.Pool(num_workers) as pool:
        results = dict(pool.starmap(fetch_search_results, [(deal, ) + (kwargs,) for deal in deals]))
    return results

def extract_subdomains(url):
    """Trích xuất subdomains từ một URL."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        base_domain = tldextract.extract(url).domain
        subdomains = set()

        for link in soup.find_all('a', href=True):
            link_url = link['href']
            if link_url.startswith("http"):
                subdomains.add(link_url)
            elif link_url.startswith("/"):
                subdomains.add(f'{url.rstrip("/")}{link_url}')
        
        return {url: [i for i in subdomains if tldextract.extract(i).domain == base_domain]}
    
    except requests.RequestException:
        return {url: []}


def extract_subdomains_parallel(urls, num_workers=4):
    """Chạy song song việc tìm subdomains cho nhiều URL."""
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(extract_subdomains, urls)
    
    # Gộp kết quả thành dictionary
    merged_results = {}
    for result in results:
        merged_results.update(result)
    
    return merged_results