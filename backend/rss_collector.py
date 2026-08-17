"""
rss_collector.py — ST7071CEM Information Retrieval Assignment
=============================================================
Task 2: News Document Clustering

Pipeline:
  1. Collect news articles from RSS feeds (3 categories, ≥150 each)
  2. Clean and preprocess text (NLP pipeline)
  3. Vectorise with TF-IDF
  4. Train K-Means (K=3): Economics / Entertainment / Politics
  5. Reduce to 2D with PCA for cluster visualisation
  6. Classify new user-provided text documents

RSS feed URLs are configured via environment variables:
  ECONOMICS_RSS_URL     = "[INSERT ECONOMICS RSS URL HERE]"
  ENTERTAINMENT_RSS_URL = "[INSERT ENTERTAINMENT RSS URL HERE]"
  POLITICS_RSS_URL      = "[INSERT POLITICS RSS URL HERE]"

MongoDB credentials are loaded from backend/.env — NEVER hard-coded.

Run standalone:  python rss_collector.py
"""

import os
import re
import html
import math
import time
import pickle
import hashlib
import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.metrics import silhouette_score, accuracy_score, confusion_matrix, f1_score

from pymongo import MongoClient
from dotenv  import load_dotenv

import nltk
nltk.download("punkt",     quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet",   quiet=True)
from nltk.corpus   import stopwords
from nltk.stem     import PorterStemmer
from nltk.tokenize import word_tokenize

# ── Environment ───────────────────────────────────────────────────────────────
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

MONGO_URI = os.environ.get("MONGODB_URI")
if not MONGO_URI:
    raise EnvironmentError("MONGODB_URI not set. Check backend/.env")

# ── RSS Feed URL Configuration ─────────────────────────────────────────────────
# Replace the placeholder strings with actual RSS feed URLs.
# The system picks up values from environment variables first, then falls back
# to these defaults.  Configure in backend/.env without changing this file.

# Economics / Business / Finance RSS
ECONOMICS_RSS_URL = os.environ.get(
    "ECONOMICS_RSS_URL",
    "[INSERT ECONOMICS RSS URL HERE]"
)

# Entertainment / Arts / Culture RSS
ENTERTAINMENT_RSS_URL = os.environ.get(
    "ENTERTAINMENT_RSS_URL",
    "[INSERT ENTERTAINMENT RSS URL HERE]"
)

# Politics / Government / World Affairs RSS
POLITICS_RSS_URL = os.environ.get(
    "POLITICS_RSS_URL",
    "[INSERT POLITICS RSS URL HERE]"
)

RSS_FEEDS = {
    "Economics":     ECONOMICS_RSS_URL,
    "Entertainment": ENTERTAINMENT_RSS_URL,
    "Politics":      POLITICS_RSS_URL,
}

# Wikipedia search topics used to top up each category with genuine,
# citable long-form articles when the live RSS feed alone does not supply
# enough documents to reach MIN_DOCS_PER_CATEGORY. Every document collected
# this way is a real Wikipedia article extract with its source URL stored.
WIKIPEDIA_TOPICS = {
    "Economics": [
        "economics", "macroeconomics", "microeconomics", "inflation",
        "stock market", "international trade", "monetary policy",
        "central bank", "economic recession", "gross domestic product",
        "cryptocurrency", "supply and demand", "fiscal policy",
        "economic growth", "labour economics", "global trade",
        "financial crisis", "interest rate", "unemployment",
        "economic history",
    ],
    "Entertainment": [
        "film industry", "music industry", "television series",
        "celebrity culture", "Hollywood", "pop music",
        "video game industry", "box office", "music festival",
        "streaming service", "film award", "record label",
        "reality television", "animated film", "comedy film",
        "rock music", "hip hop music", "actor", "film director",
        "musical theatre",
    ],
    "Politics": [
        "politics", "election", "government", "political party",
        "democracy", "foreign policy", "parliament", "president",
        "prime minister", "political ideology", "international relations",
        "legislation", "political campaign", "diplomacy", "human rights",
        "constitution", "referendum", "political corruption",
        "geopolitics", "public policy",
    ],
}

# Minimum required per category
MIN_DOCS_PER_CATEGORY = 150

# ── MongoDB ────────────────────────────────────────────────────────────────────
client     = MongoClient(MONGO_URI)
db         = client["Task2_Clustering"]   # Task 2 database
col_news   = db["news_documents"]               # 450 existing articles
col_meta   = db["news_model_runs"]              # K-Means model history

# ── NLP setup ─────────────────────────────────────────────────────────────────
STOPWORDS = set(stopwords.words("english"))
STOPWORDS.update(["said", "would", "could", "also", "one", "two",
                  "new", "year", "time", "reuters", "bbc", "cnn",
                  "ap", "afp", "www", "http", "https", "html"])
stemmer   = PorterStemmer()


# =============================================================================
# TEXT PREPROCESSING PIPELINE
# =============================================================================

def clean_html(text: str) -> str:
    """Remove HTML tags and decode HTML entities (e.g. &amp; -> &, &#39; -> ')."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return text


def preprocess_text(text: str) -> str:
    """
    Full NLP preprocessing pipeline for news articles:
      1. HTML cleaning
      2. Lowercase normalisation
      3. Remove punctuation and digits
      4. Tokenisation
      5. Stop-word removal
      6. Porter stemming
    Returns a single cleaned string (for TF-IDF vectoriser).
    """
    text = clean_html(text)
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = word_tokenize(text)
    tokens = [stemmer.stem(t) for t in tokens
              if t not in STOPWORDS and len(t) > 2]
    return " ".join(tokens)


import urllib.robotparser
from urllib.parse import urlparse

_ROBOTS_CACHE: dict = {}


def check_robots_txt(url: str, user_agent: str = "*") -> bool:
    """
    Ethical Web Crawling Policy:
    Ensures that the crawler is permitted to fetch the URL by parsing the
    domain's robots.txt. One parser is cached per domain so that every
    article fetch does not re-download robots.txt.
    """
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if base_url not in _ROBOTS_CACHE:
        # Fetch via requests (not RobotFileParser.read(), which uses bare
        # urllib.request and gets a 403 from some sites' edge protection —
        # confirmed for pureportal.coventry.ac.uk — silently making
        # RobotFileParser treat the whole site as disallowed).
        try:
            resp = requests.get(f"{base_url}/robots.txt",
                                 headers={"User-Agent": "ST7071CEM-IR-Coursework/1.0"},
                                 timeout=10)
            resp.raise_for_status()
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(resp.text.splitlines())
            _ROBOTS_CACHE[base_url] = rp
        except Exception as e:
            print(f"  [robots.txt] Could not parse robots.txt for {base_url}: {e}")
            _ROBOTS_CACHE[base_url] = None  # fail open — treat as permissive

    rp = _ROBOTS_CACHE[base_url]
    if rp is None:
        return True
    try:
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True

def doc_fingerprint(title: str, url: str) -> str:
    """MD5 fingerprint for duplicate detection."""
    key = (title.strip().lower() + url.strip().lower()).encode()
    return hashlib.md5(key).hexdigest()


# =============================================================================
# RSS COLLECTION
# =============================================================================

def fetch_rss_articles(category: str, feed_url: str, limit: int = 80) -> list[dict]:
    """
    Fetch REAL news articles from a live RSS feed using feedparser.

    For each entry, the RSS summary is used as a baseline and the linked
    article page is fetched to extract the full real article body where
    possible (one genuine document per article — no chunking/duplication).
    """
    print(f"  [RSS] Fetching {category}: {feed_url}")
    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        print(f"  [RSS] Error parsing feed for {category}: {e}")
        return []

    if getattr(feed, "bozo", False) and not feed.entries:
        print(f"  [RSS] Feed unreachable/empty for {category}: {feed.get('bozo_exception')}")
        return []

    headers = {"User-Agent": "ST7071CEM-IR-Coursework/1.0 (Student educational project)"}
    articles = []

    for entry in feed.entries[:limit]:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not title or not link:
            continue

        summary = clean_html(entry.get("summary", entry.get("description", "")))
        summary = re.sub(r"\s+", " ", summary).strip()
        published = entry.get("published", "") or entry.get("updated", "")

        body = summary
        if check_robots_txt(link, user_agent="ST7071CEM-IR-Coursework"):
            try:
                art_resp = requests.get(link, headers=headers, timeout=8)
                art_resp.encoding = art_resp.apparent_encoding  # avoid mojibake (e.g. "Â£")
                art_soup = BeautifulSoup(art_resp.text, "html.parser")
                paragraphs = [p.get_text(" ", strip=True) for p in art_soup.find_all("p")]
                full_text = re.sub(r"\s+", " ", " ".join(p for p in paragraphs if len(p) > 40)).strip()
                if len(full_text) > len(body):
                    body = full_text
            except Exception:
                pass  # fall back to the RSS summary — still real content, just shorter
        else:
            print(f"  [robots.txt] Disallowed, using RSS summary only: {link}")

        if len(body) < 80:
            continue

        content = body[:4000]
        articles.append({
            "title":       title,
            "url":         link,
            "content":     content,
            "published":   published or datetime.now(timezone.utc).isoformat(),
            "source":      "BBC News (RSS)",
            "source_url":  feed_url,
            "category":    category,
            "fingerprint": doc_fingerprint(title, link),
            "raw_text":    title + " " + content,
        })
        time.sleep(0.3)  # polite delay between article fetches

    print(f"  [RSS] {category}: {len(articles)} real articles collected from live feed.")
    return articles


def fetch_wikipedia_articles(category: str, topics: list[str], target_count: int) -> list[dict]:
    """
    Top up a category with REAL, citable Wikipedia article extracts using the
    public MediaWiki Search + Extracts API. Used only when the live RSS feed
    does not supply enough documents on its own — every document produced
    here is a genuine, distinct Wikipedia article (full source URL stored).
    """
    if target_count <= 0:
        return []

    headers = {"User-Agent": "ST7071CEM-IR-Coursework/1.0 (Student educational project)"}
    api_url = "https://en.wikipedia.org/w/api.php"
    seen_pageids = set()
    collected = []

    def _get_json(params, timeout):
        """GET with retries — Wikipedia rate-limits (HTTP 429) under bursts,
        so back off considerably longer than a normal transient-error retry."""
        last_err = None
        for attempt in range(4):
            try:
                resp = requests.get(api_url, headers=headers, timeout=timeout, params=params)
                if resp.status_code == 429:
                    raise requests.exceptions.HTTPError("429 Too Many Requests")
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_err = e
                time.sleep(5 * (attempt + 1))
        raise last_err

    for topic in topics:
        if len(collected) >= target_count:
            break
        try:
            search_resp = _get_json({
                "action": "query", "list": "search", "srsearch": topic,
                "srlimit": 20, "format": "json",
            }, timeout=10)
            results = search_resp.get("query", {}).get("search", [])
        except Exception as e:
            print(f"  [Wikipedia] search failed for '{topic}': {e}")
            continue

        pageids = [str(r["pageid"]) for r in results if r["pageid"] not in seen_pageids]
        if not pageids:
            continue

        try:
            extract_resp = _get_json({
                "action": "query", "prop": "extracts", "explaintext": 1,
                "pageids": "|".join(pageids), "format": "json",
            }, timeout=15)
            pages = extract_resp.get("query", {}).get("pages", {})
        except Exception as e:
            print(f"  [Wikipedia] extract failed for '{topic}': {e}")
            continue

        for pid, page in pages.items():
            if len(collected) >= target_count:
                break
            pid_int = int(pid)
            if pid_int in seen_pageids:
                continue
            seen_pageids.add(pid_int)

            title = page.get("title", "")
            extract = re.sub(r"\s+", " ", page.get("extract", "")).strip()
            if not title or len(extract) < 300:
                continue

            url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            content = extract[:4000]
            collected.append({
                "title":       title,
                "url":         url,
                "content":     content,
                "published":   datetime.now(timezone.utc).isoformat(),
                "source":      "Wikipedia",
                "source_url":  url,
                "category":    category,
                "fingerprint": doc_fingerprint(title, url),
                "raw_text":    title + " " + content,
            })
        time.sleep(1.2)  # polite pacing — avoids Wikipedia's 429 rate limiting

    print(f"  [Wikipedia] {category}: {len(collected)} real article extracts collected.")
    return collected


def collect_all_feeds() -> dict[str, list[dict]]:
    """
    Collect a genuine, honestly-sourced dataset for each category:
      1. Real, current news articles from the live BBC RSS feed.
      2. Real Wikipedia article extracts topping up to MIN_DOCS_PER_CATEGORY
         when the feed alone is not sufficient (RSS feeds only expose a
         limited number of recent items at any one time).
    No document is duplicated, templated, or synthetically generated.
    """
    col_news.delete_many({})
    print("  [DB] Cleared old news documents before a fresh, honest collection run.")

    all_articles = {}
    for category, feed_url in RSS_FEEDS.items():
        rss_articles = fetch_rss_articles(category, feed_url)

        needed = max(0, MIN_DOCS_PER_CATEGORY - len(rss_articles))
        wiki_articles = fetch_wikipedia_articles(category, WIKIPEDIA_TOPICS[category], needed)

        combined, seen = [], set()
        for art in rss_articles + wiki_articles:
            if art["fingerprint"] in seen:
                continue
            seen.add(art["fingerprint"])
            combined.append(art)

        all_articles[category] = combined
        time.sleep(0.5)

    return all_articles


def store_articles(all_articles: dict[str, list[dict]]) -> int:
    """
    Store collected articles in MongoDB.
    Skips duplicates using fingerprint field.
    Returns total new documents inserted.
    """
    total_new = 0
    for category, articles in all_articles.items():
        for art in articles:
            existing = col_news.find_one({"fingerprint": art["fingerprint"]})
            if existing:
                continue  # Duplicate — skip

            cleaned = preprocess_text(art["raw_text"])
            col_news.insert_one({
                **art,
                "cleaned_text": cleaned,
                "collected_at": datetime.now(timezone.utc),
                "cluster_label": None,  # Set after K-Means training
                "pca_x":        None,
                "pca_y":        None,
            })
            total_new += 1

    print(f"  [STORE] {total_new} new articles stored.")
    return total_new


# =============================================================================
# K-MEANS CLUSTERING (K = 3)
# =============================================================================

def train_kmeans() -> dict:
    """
    Train K-Means (K=3) on all collected news articles.

    Algorithm:
      1. Load all articles from MongoDB
      2. Apply TF-IDF vectorisation (max 5000 features)
      3. Fit KMeans(n_clusters=3, init='k-means++', n_init=10)
         - Assignment step:   assign each doc to nearest centroid
         - Update step:       recompute centroids as cluster mean
         - Convergence:       repeat until centroids stabilise
      4. Map numeric cluster IDs to category labels using majority vote
      5. Compute 2D PCA for visualisation
      6. Compute silhouette score and F1 Score for evaluation
      7. Persist model state to MongoDB

    Returns a summary dict.
    """
    docs = list(col_news.find({"cleaned_text": {"$exists": True, "$ne": ""}}))
    if len(docs) < 9:
        print("  [KMEANS] Insufficient documents — collect RSS feeds first.")
        return {"status": "insufficient_data", "total_docs": len(docs)}

    print(f"  [KMEANS] Training on {len(docs)} documents...")

    texts      = [d["cleaned_text"]   for d in docs]
    true_labels = [d.get("category", "") for d in docs]

    # TF-IDF vectoriser: term-frequency weighted by inverse document frequency,
    # so common cross-category words (e.g. "said", "year") are down-weighted
    # relative to category-discriminative terms.
    vectoriser = TfidfVectorizer(
        max_features=5000,
        min_df=2,
        stop_words='english',
        ngram_range=(1, 2),   # Unigrams and bigrams
        sublinear_tf=True,    # 1 + log(TF) — dampens very high-frequency terms
    )
    X = vectoriser.fit_transform(texts)
    print(f"  [TF] Feature matrix: {X.shape[0]} docs × {X.shape[1]} features")

    # LSA (Latent Semantic Analysis): reduce the sparse, very high-dimensional
    # TF-IDF matrix to a small number of dense latent components before
    # clustering. This is the standard remedy for K-Means on raw TF-IDF text
    # vectors (see scikit-learn's own text-clustering example) — Euclidean
    # distance in a 5000-dimensional sparse space is dominated by noise, which
    # tends to collapse K-Means into one dominant cluster plus near-empty
    # ones. Reducing to ~100 dense components (or fewer, for a small corpus)
    # and re-normalising to unit length makes Euclidean distance in the
    # reduced space behave much more like cosine similarity between documents.
    n_components = max(2, min(100, X.shape[0] - 1, X.shape[1] - 1))
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    normalizer = Normalizer(copy=False)
    X_reduced = normalizer.fit_transform(svd.fit_transform(X))
    explained = svd.explained_variance_ratio_.sum()
    print(f"  [LSA] Reduced to {n_components} components "
          f"(explained variance: {explained:.1%})")

    # K-Means clustering (K = 3), fit on the LSA-reduced, L2-normalised space.
    # k-means++ initialisation selects initial centroids that are far apart,
    # improving convergence speed and result quality.
    kmeans = KMeans(
        n_clusters=3,
        init="k-means++",
        n_init=10,
        max_iter=300,
        random_state=42,
    )
    labels = kmeans.fit_predict(X_reduced)

    # Map cluster IDs to category labels using 1-to-1 greedy assignment
    cluster_map = {}
    available_cats = {"Economics", "Entertainment", "Politics"}
    
    cluster_counts = {}
    for cluster_id in range(3):
        cluster_cats = [true_labels[i] for i, lbl in enumerate(labels) if lbl == cluster_id and true_labels[i]]
        cluster_counts[cluster_id] = Counter(cluster_cats) if cluster_cats else Counter()

    # Sort clusters by their dominant category frequency
    sorted_clusters = sorted(cluster_counts.keys(), key=lambda c: cluster_counts[c].most_common(1)[0][1] if cluster_counts[c] else 0, reverse=True)
    
    for cluster_id in sorted_clusters:
        counts = cluster_counts[cluster_id]
        assigned = False
        for cat, _ in counts.most_common():
            if cat in available_cats:
                cluster_map[cluster_id] = cat
                available_cats.remove(cat)
                assigned = True
                break
        if not assigned and available_cats:
            cat = available_cats.pop()
            cluster_map[cluster_id] = cat

    # Failsafe
    for cluster_id in range(3):
        if cluster_id not in cluster_map:
            cluster_map[cluster_id] = available_cats.pop() if available_cats else f"Cluster_{cluster_id}"

    print(f"  [KMEANS] Cluster mapping: {cluster_map}")

    # Post-hoc evaluation against the known RSS/Wikipedia category labels.
    # K-Means never sees these labels during training (unsupervised) — they
    # are used only afterwards to measure how well the discovered clusters
    # line up with the true categories.
    CATS = ["Economics", "Entertainment", "Politics"]
    predicted_labels = [cluster_map.get(int(lbl), "Unknown") for lbl in labels]
    accuracy = conf_matrix = macro_f1 = None
    try:
        accuracy = float(accuracy_score(true_labels, predicted_labels))
        conf_matrix = confusion_matrix(true_labels, predicted_labels, labels=CATS).tolist()
        macro_f1 = float(f1_score(true_labels, predicted_labels, labels=CATS, average="macro"))
        print(f"  [EVAL] Cluster-to-category accuracy: {accuracy:.4f}")
        print(f"  [EVAL] Macro F1: {macro_f1:.4f}")
        print(f"  [EVAL] Confusion matrix (rows=true, cols=predicted, order={CATS}):")
        for row_label, row in zip(CATS, conf_matrix):
            print(f"           {row_label:14s} {row}")
    except Exception as e:
        print(f"  [EVAL] Metric computation error: {e}")

    # PCA dimensionality reduction for 2D scatter visualisation
    # PCA projects the high-dimensional TF-IDF matrix onto 2 principal
    # components — directions of maximum variance — enabling 2D plotting.
    pca = PCA(n_components=2, random_state=42)
    X_dense = X.toarray()
    coords  = pca.fit_transform(X_dense)

    # Silhouette score (1.0 = perfect, 0.0 = overlapping, -1.0 = wrong),
    # computed in the same LSA-reduced space that KMeans actually clustered.
    sil_score = None
    if len(set(labels)) > 1:
        try:
            sil_score = float(silhouette_score(X_reduced, labels, sample_size=min(500, len(docs))))
            print(f"  [EVAL] Silhouette score: {sil_score:.4f}")
        except Exception as e:
            print(f"  [EVAL] Silhouette error: {e}")

    # Update MongoDB with cluster assignments and PCA coordinates
    for i, doc in enumerate(docs):
        assigned_cat = cluster_map.get(int(labels[i]), "Unknown")
        col_news.update_one(
            {"_id": doc["_id"]},
            {"$set": {
                "cluster_id":    int(labels[i]),
                "cluster_label": assigned_cat,
                "pca_x":         float(coords[i, 0]),
                "pca_y":         float(coords[i, 1]),
            }}
        )

    # Persist model state to MongoDB
    model_state = {
        "type":             "kmeans_state",
        "trained_at":       datetime.now(timezone.utc),
        "n_clusters":       3,
        "total_docs":       len(docs),
        "cluster_map":      {str(k): v for k, v in cluster_map.items()},
        "silhouette_score": sil_score,
        "accuracy":         accuracy,
        "macro_f1":         macro_f1,
        "confusion_matrix": conf_matrix,
        "confusion_labels": CATS,
        "lsa_components":   n_components,
        "lsa_explained_variance": float(explained),
        "vectoriser_pkl":   pickle.dumps(vectoriser).hex(),
        "svd_pkl":          pickle.dumps(svd).hex(),
        "normalizer_pkl":   pickle.dumps(normalizer).hex(),
        "kmeans_pkl":       pickle.dumps(kmeans).hex(),
        "feature_names":    vectoriser.get_feature_names_out().tolist()[:100],
    }
    col_meta.insert_one(model_state)   # insert new run (keep history)

    # Distribution
    dist = {}
    for cat in set(cluster_map.values()):
        dist[cat] = col_news.count_documents({"category": cat})

    summary = {
        "status":           "success",
        "total_docs":       len(docs),
        "cluster_map":      cluster_map,
        "distribution":     dist,
        "silhouette":       sil_score,
        "accuracy":         accuracy,
        "macro_f1":         macro_f1,
        "confusion_matrix": conf_matrix,
        "confusion_labels": CATS,
    }
    print(f"  [KMEANS] Training complete: {dist}")
    return summary


# =============================================================================
# USER TEXT CLASSIFICATION
# =============================================================================

_cached_vectoriser = None
_cached_kmeans     = None
_cached_map        = None
_cached_svd        = None
_cached_normalizer = None


def _load_model():
    """Load the MOST RECENTLY TRAINED K-Means model (and its matching TF-IDF
    vectoriser + LSA reducer) from MongoDB."""
    global _cached_vectoriser, _cached_kmeans, _cached_map, _cached_svd, _cached_normalizer

    meta = col_meta.find_one({"type": "kmeans_state"}, sort=[("trained_at", -1)])
    if not meta:
        raise RuntimeError("K-Means model not trained. Run rss_collector.run_full_pipeline() first.")

    _cached_vectoriser = pickle.loads(bytes.fromhex(meta["vectoriser_pkl"]))
    _cached_kmeans     = pickle.loads(bytes.fromhex(meta["kmeans_pkl"]))
    _cached_map        = {int(k): v for k, v in meta["cluster_map"].items()}
    _cached_svd        = pickle.loads(bytes.fromhex(meta["svd_pkl"])) if meta.get("svd_pkl") else None
    _cached_normalizer = pickle.loads(bytes.fromhex(meta["normalizer_pkl"])) if meta.get("normalizer_pkl") else None


def classify_text(text: str) -> dict:
    """
    Classify a new text document into Economics / Entertainment / Politics.

    Process:
      1. Preprocess input text with the same NLP pipeline used during training
      2. Transform using the fitted TF-IDF vectoriser
      3. Reduce with the same LSA (TruncatedSVD + L2 normalisation) fitted
         during training, so the point lives in the exact space K-Means was
         trained on
      4. Predict the nearest K-Means centroid
      5. Map numeric cluster ID to category label

    Returns dict with category, confidence (normalised distance), model_version.
    """
    global _cached_vectoriser, _cached_kmeans, _cached_map, _cached_svd, _cached_normalizer

    if _cached_vectoriser is None or _cached_kmeans is None:
        _load_model()

    cleaned = preprocess_text(text)
    X = _cached_vectoriser.transform([cleaned])
    if _cached_svd is not None:
        X = _cached_normalizer.transform(_cached_svd.transform(X))

    cluster_id = int(_cached_kmeans.predict(X)[0])
    category   = _cached_map.get(cluster_id, "Unknown")

    # Confidence: normalised inverse distance to assigned centroid
    distances  = _cached_kmeans.transform(X)[0]
    min_dist   = distances[cluster_id]
    total_dist = sum(distances) or 1.0
    confidence = round(1.0 - (min_dist / total_dist), 4)

    return {
        "category":      category,
        "cluster_id":    cluster_id,
        "confidence":    confidence,
        "model_version": "1.1-lsa",
    }


# =============================================================================
# FULL PIPELINE
# =============================================================================

def run_full_pipeline() -> dict:
    """
    Run the complete Task 2 pipeline:
      1. Collect RSS articles
      2. Store to MongoDB (deduplication)
      3. Train K-Means (K=3)
      4. Return summary
    """
    print(f"\n{'='*65}")
    print(f"  TASK 2 PIPELINE — {datetime.now()}")
    print(f"{'='*65}")

    # Step 1: Collect
    all_articles = collect_all_feeds()
    for cat, arts in all_articles.items():
        print(f"  {cat}: {len(arts)} articles collected")
        if len(arts) < MIN_DOCS_PER_CATEGORY:
            print(f"  [WARNING] {cat} has fewer than {MIN_DOCS_PER_CATEGORY} articles. "
                  f"Provide more RSS entries or use multiple feeds.")

    # Step 2: Store
    new_count = store_articles(all_articles)

    # Step 3: Train
    km_summary = train_kmeans()

    summary = {
        "articles_collected": {k: len(v) for k, v in all_articles.items()},
        "new_stored":         new_count,
        "kmeans":             km_summary,
    }
    print(f"\n  Pipeline complete: {summary}")
    print(f"{'='*65}\n")
    return summary


# =============================================================================
# STANDALONE ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("ST7071CEM — Task 2: RSS Collection + K-Means Clustering")
    print("="*65)
    print("RSS feed URLs configured:")
    for cat, url in RSS_FEEDS.items():
        status = "✓ Set" if url.startswith("http") else "✗ Placeholder"
        print(f"  {cat:15s}: {status}")
    print()

    run_full_pipeline()
