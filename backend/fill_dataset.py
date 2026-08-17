import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone
import time
import hashlib

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

MONGO_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["vertical_search_engine"]
col_news = db["news_documents"]

def doc_fingerprint(title, url):
    key = (title.strip().lower() + url.strip().lower()).encode()
    return hashlib.md5(key).hexdigest()

def fetch_wikipedia_category(category_name, target_category, limit=150):
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category_name}&cmlimit=500&format=json"
    headers = {"User-Agent": "ST7071CEM-IR-Bot/1.0 (Student Project)"}
    print(f"Fetching {category_name}...")
    resp = requests.get(url, headers=headers).json()
    members = resp.get('query', {}).get('categorymembers', [])
    
    count = col_news.count_documents({'category': target_category})
    needed = limit - count
    if needed <= 0:
        print(f"{target_category} already has {count} documents.")
        return
        
    print(f"Need {needed} more for {target_category}.")
    
    added = 0
    for member in members:
        if added >= needed:
            break
        if member['ns'] != 0: # only articles
            continue
        
        pageid = member['pageid']
        title = member['title']
        page_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=True&explaintext=True&pageids={pageid}&format=json"
        
        try:
            page_resp = requests.get(page_url, headers=headers).json()
            extract = page_resp['query']['pages'][str(pageid)]['extract']
            if len(extract) < 200: # skip very short ones
                continue
                
            doc_url = f"https://en.wikipedia.org/?curid={pageid}"
            fingerprint = doc_fingerprint(title, doc_url)
            
            if col_news.find_one({"fingerprint": fingerprint}):
                continue
                
            from rss_collector import preprocess_text
            cleaned = preprocess_text(title + " " + extract)
            
            col_news.insert_one({
                "title": title,
                "url": doc_url,
                "content": extract,
                "published": datetime.now(timezone.utc).isoformat(),
                "source": "Wikipedia",
                "category": target_category,
                "fingerprint": fingerprint,
                "raw_text": title + " " + extract,
                "cleaned_text": cleaned,
                "collected_at": datetime.now(timezone.utc),
                "cluster_label": None,
                "pca_x": None,
                "pca_y": None,
            })
            added += 1
            print(f"Added {title} ({added}/{needed})")
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching {title}: {e}")

if __name__ == "__main__":
    fetch_wikipedia_category("Economics", "Economics", 150)
    fetch_wikipedia_category("Entertainment", "Entertainment", 150)
    fetch_wikipedia_category("Politics", "Politics", 150)
    
    print("Final counts:")
    for cat in ["Economics", "Entertainment", "Politics"]:
        print(f"{cat}: {col_news.count_documents({'category': cat})}")
