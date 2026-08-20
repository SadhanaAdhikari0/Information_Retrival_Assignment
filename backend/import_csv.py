import csv
import os
import sys
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

# Ensure we can import from backend modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rss_collector import preprocess_text, train_kmeans, doc_fingerprint

load_dotenv(".env")
MONGO_URI = os.environ.get("MONGODB_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_URI is not set in backend/.env")

client = MongoClient(MONGO_URI)
db = client["Task2_Clustering"]
col_news = db["news_documents"]

def load_csv(filepath):
    print(f"Loading data from {filepath}...")
    col_news.delete_many({})
    print("Cleared existing news_documents collection.")
    
    count = 0
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            document = row.get("document", "").strip()
            category = row.get("true_category", "").strip()
            
            if not document or not category:
                continue
                
            # Create a mock title (first 10 words)
            words = document.split()
            title = " ".join(words[:10]) + "..." if len(words) > 10 else document
            
            fingerprint = doc_fingerprint(title, "")
            cleaned = preprocess_text(document)
            
            col_news.insert_one({
                "title": title,
                "url": "",
                "content": document,
                "published": datetime.now(timezone.utc).isoformat(),
                "source": "task2_dataset.csv",
                "source_url": "",
                "category": category,
                "fingerprint": fingerprint,
                "raw_text": document,
                "cleaned_text": cleaned,
                "collected_at": datetime.now(timezone.utc),
                "cluster_label": None,
                "pca_x": None,
                "pca_y": None,
            })
            count += 1
            
    print(f"Loaded {count} documents from CSV into MongoDB.")
    
    print("Training K-Means model on newly loaded dataset...")
    summary = train_kmeans()
    print("Training Complete!")
    print(summary)

if __name__ == "__main__":
    # Path to the task2_dataset.csv in the root folder
    csv_path = os.path.join(os.path.dirname(__file__), "..", "task2_dataset.csv")
    load_csv(csv_path)
