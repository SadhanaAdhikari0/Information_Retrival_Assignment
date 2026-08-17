import csv
import os
from datetime import datetime, timezone
import hashlib
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
db = MongoClient(os.environ["MONGODB_URI"])["Task2_Clustering"]
col_news = db["news_documents"]

def doc_fingerprint(title, content):
    return hashlib.md5((title + content).encode('utf-8')).hexdigest()

from rss_collector import preprocess_text, train_kmeans

with open("../task2_dataset.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    for row in reader:
        if len(row) < 2: continue
        text = row[0]
        cat = row[1]
        
        fingerprint = doc_fingerprint(text[:50], text)
        if col_news.find_one({"fingerprint": fingerprint}):
            continue
            
        cleaned = preprocess_text(text)
        
        col_news.insert_one({
            "title": text[:60] + "...",
            "url": "",
            "content": text,
            "published": datetime.now(timezone.utc).isoformat(),
            "source": "CSV",
            "category": cat,
            "fingerprint": fingerprint,
            "raw_text": text,
            "cleaned_text": cleaned,
            "collected_at": datetime.now(timezone.utc),
            "cluster_label": None,
            "pca_x": None,
            "pca_y": None,
        })
        
print(f"Total docs in DB: {col_news.count_documents({})}")
print("Training K-Means...")
summary = train_kmeans()
print(summary)
