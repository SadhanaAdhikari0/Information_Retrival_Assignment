import os
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rss_collector import preprocess_text, train_kmeans

load_dotenv(".env")
MONGO_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["Task2_Clustering"]
col_news = db["news_documents"]
col_meta = db["news_model_runs"]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_text(soup):
    paragraphs = soup.find_all('p')
    # Filter very short paragraphs (usually nav links or captions)
    text = " ".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
    return text

def scrape_category(category_name, seed_url, link_pattern, crawl_pattern, max_articles=180):
    print(f"\n[Scraper] Starting {category_name} from {seed_url}")
    visited = set()
    queue = [seed_url]
    articles = []
    
    while queue and len(articles) < max_articles:
        url = queue.pop(0)
        
        # Normalize url
        url = url.split('#')[0].split('?')[0]
        
        if url in visited:
            continue
        visited.add(url)
        
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                continue
        except Exception as e:
            print(f"  [Error] Failed to fetch {url}")
            continue
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Is this an article page?
        if url != seed_url and re.search(link_pattern, url):
            text = extract_text(soup)
            if len(text) > 300:
                title = soup.title.string if soup.title else url
                title = title.replace("- CNBC", "").replace("- CNN", "").replace("| AP News", "").strip()
                
                fingerprint = hashlib.md5((title.lower() + url.lower()).encode()).hexdigest()
                
                cleaned = preprocess_text(text)
                
                doc = {
                    "title": title,
                    "url": url,
                    "content": text[:4000],
                    "published": datetime.now(timezone.utc).isoformat(),
                    "source": urlparse(seed_url).netloc,
                    "source_url": seed_url,
                    "category": category_name,
                    "fingerprint": fingerprint,
                    "raw_text": title + " " + text,
                    "cleaned_text": cleaned,
                    "collected_at": datetime.now(timezone.utc),
                    "cluster_label": None,
                    "pca_x": None,
                    "pca_y": None,
                    "pca_z": None,
                }
                
                # Deduplicate by fingerprint within this run
                if not any(a["fingerprint"] == fingerprint for a in articles):
                    articles.append(doc)
                    print(f"  [{len(articles)}/{max_articles}] Extracted: {title[:50]}...")
                
        # Enqueue new links
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(url, href)
            full_url = full_url.split('#')[0].split('?')[0]
            
            # Ensure we only crawl links matching our crawl pattern (stay in section)
            if re.search(crawl_pattern, full_url) and full_url not in visited and full_url not in queue:
                queue.append(full_url)
                
        time.sleep(0.5) # Be polite
        
    print(f"[Scraper] Finished {category_name}: {len(articles)} articles collected.")
    return articles

def run():
    print("Clearing previous database documents...")
    col_news.delete_many({})
    
    # 1. Economics - CNBC
    econ_articles = scrape_category(
        "Economics", 
        "https://www.cnbc.com/economy/", 
        r'/202[0-9]/',
        r'cnbc\.com/(economy|202[0-9])',
        180
    )
    if econ_articles:
        col_news.insert_many(econ_articles)
        
    # 2. Politics - AP News
    pol_articles = scrape_category(
        "Politics", 
        "https://apnews.com/politics", 
        r'/article/',
        r'apnews\.com/(politics|article)',
        180
    )
    if pol_articles:
        col_news.insert_many(pol_articles)
        
    # 3. Entertainment - CNN
    ent_articles = scrape_category(
        "Entertainment", 
        "https://edition.cnn.com/entertainment", 
        r'/202[0-9]/',
        r'cnn\.com/(entertainment|202[0-9])',
        180
    )
    if ent_articles:
        col_news.insert_many(ent_articles)
        
    print(f"\nSaved a total of {col_news.count_documents({})} articles to MongoDB.")
    
    print("\nTraining K-Means model on the new dataset...")
    summary = train_kmeans()
    print("\n[Done] Pipeline complete!")
    print(summary)

if __name__ == "__main__":
    run()
