"""
app.py — ST7071CEM Information Retrieval Assignment
====================================================
Flask API server for:
  Task 1 — Vertical Search Engine (VSM + Cosine Similarity)
  Task 2 — News Document Clustering (K-Means, K=3)

Environment variables are loaded from .env (never hard-coded).
Database: vertical_search_engine (existing MongoDB with crawled data)
"""

import os
import re
import math
import pickle
import threading
from collections import Counter
from datetime import datetime, timezone

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient

import nltk
nltk.download("punkt",      quiet=True)
nltk.download("punkt_tab",  quiet=True)
nltk.download("stopwords",  quiet=True)
nltk.download("wordnet",    quiet=True)
from nltk.corpus   import stopwords
from nltk.stem     import PorterStemmer
from nltk.tokenize import word_tokenize

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ── Flask setup ───────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static")
CORS(app)

# ── MongoDB setup (credentials from environment, NEVER hard-coded) ────────────
MONGO_URI = os.environ.get("MONGODB_URI")
if not MONGO_URI:
    raise EnvironmentError(
        "MONGODB_URI is not set. Create backend/.env and set MONGODB_URI."
    )

client = MongoClient(MONGO_URI)
db_task1 = client["Task1_Search"]
db_task2 = client["Task2_Clustering"]

# Task 1 — existing collections
col_doc_vecs  = db_task1["doc_vectors"]         # TF-IDF document vectors (31 docs)
col_term_idx  = db_task1["term_index"]          # IDF values per term (2184 terms)
col_crawl_log = db_task1["crawl_log"]           # crawl history
col_raw_pages = db_task1["research_publication"]           # original crawled pages

# Task 2 — existing collections
col_news      = db_task2["news_documents"]      # 450 news articles (existing)
col_news_cls  = db_task2["news_classifications"] # user classification history
col_model_runs = db_task2["news_model_runs"]    # K-Means model run history

# ── NLP pipeline ──────────────────────────────────────────────────────────────
STOPWORDS = set(stopwords.words("english"))
STOPWORDS.update(["coventry", "research", "pureportal", "university",
                  "www", "http", "https", "html", "com", "org", "uk"])
stemmer = PorterStemmer()

RESULTS_PER_PAGE = 10  # K = 10 as required by assignment


def preprocess(text: str) -> list:
    """
    NLP preprocessing pipeline:
      1. Lowercase normalisation
      2. Remove non-alphanumeric characters
      3. Tokenisation (NLTK)
      4. Stop-word removal
      5. Porter stemming
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = word_tokenize(text)
    return [
        stemmer.stem(t)
        for t in tokens
        if t not in STOPWORDS and len(t) > 2
    ]


# ── Task 1: Vector Space Model ─────────────────────────────────────────────────

def build_query_vector(query: str) -> dict:
    """
    Build a normalised TF-IDF query vector from the user's search query.

    Formula:
        TF(t,q)  = count(t in q) / total_terms(q)
        TF-IDF   = TF(t,q) × IDF(t)          [IDF from pre-built index]
        vector   = L2-normalised TF-IDF weights

    Returns {term: normalised_weight} dict.
    """
    tokens = preprocess(query)
    if not tokens:
        return {}

    tf = Counter(tokens)
    total = len(tokens)

    idf_cursor = col_term_idx.find({"term": {"$in": list(tf.keys())}})
    idf_map = {d["term"]: d["idf"] for d in idf_cursor}

    vector = {
        term: (count / total) * idf_map.get(term, 0)
        for term, count in tf.items()
        if term in idf_map
    }

    norm = math.sqrt(sum(w * w for w in vector.values())) or 1.0
    return {t: w / norm for t, w in vector.items()}


def cosine_similarity(vec1: dict, vec2: dict) -> float:
    """
    Cosine similarity between two L2-normalised TF-IDF vectors.

    Formula:
        cos(θ) = (Q · D) / (|Q| × |D|)

    Since both vectors are L2-normalised: |Q| = |D| = 1
    Therefore: cos(θ) = dot product of shared terms only.
    """
    common = set(vec1.keys()) & set(vec2.keys())
    return sum(vec1[t] * vec2[t] for t in common)


def search_documents(query: str, page: int = 1):
    """
    Full VSM search pipeline with pagination.
    Returns (page_results, total_matching).
    """
    q_vec = build_query_vector(query)
    if not q_vec:
        return [], 0

    scored = []
    for doc in col_doc_vecs.find({}):
        score = cosine_similarity(q_vec, doc.get("vector", {}))
        if score > 0:
            # Fetch rich metadata from raw_pages if available
            raw = col_raw_pages.find_one({"url": doc.get("url", "")}) or {}
            scored.append({
                "score":            round(score, 4),
                "url":              doc.get("url", ""),
                "title":            doc.get("title", "") or raw.get("title", "Untitled"),
                "authors":          doc.get("authors", []),
                "author_profiles":  doc.get("author_profiles", {}),
                "publication_date": doc.get("publication_date", ""),
                "source_url":       doc.get("source_url", ""),
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    total = len(scored)
    start = (page - 1) * RESULTS_PER_PAGE
    return scored[start: start + RESULTS_PER_PAGE], total


# ── Task 1 API Routes ──────────────────────────────────────────────────────────

@app.route("/api/search", methods=["GET"])
def api_search():
    """
    GET /api/search?q=<query>&page=<page>
    Returns ranked results with pagination metadata.
    """
    query = request.args.get("q", "").strip()
    page  = max(1, int(request.args.get("page", 1)))

    if not query:
        return jsonify({"results": [], "total": 0, "pages": 0, "page": 1})

    results, total = search_documents(query, page)
    total_pages = math.ceil(total / RESULTS_PER_PAGE) if total else 0

    return jsonify({
        "results":  results,
        "total":    total,
        "page":     page,
        "pages":    total_pages,
        "per_page": RESULTS_PER_PAGE,
        "query":    query,
    })


@app.route("/api/suggestions", methods=["GET"])
def api_suggestions():
    """GET /api/suggestions?q=<partial>  — Autocomplete from term index."""
    q = request.args.get("q", "").strip().lower()
    if not q or len(q) < 2:
        return jsonify({"suggestions": []})

    regex = f"^{re.escape(q)}"
    docs  = col_term_idx.find(
        {"term": {"$regex": regex, "$options": "i"}},
        {"_id": 0, "term": 1}
    ).limit(6)
    return jsonify({"suggestions": [d["term"] for d in docs]})


@app.route("/api/crawl-status", methods=["GET"])
def api_crawl_status():
    """GET /api/crawl-status — Last crawl info and index stats."""
    last_log = col_crawl_log.find_one({}, sort=[("run_at", -1)])
    if last_log:
        last_log["_id"] = str(last_log["_id"])
        if isinstance(last_log.get("run_at"), datetime):
            last_log["run_at"] = last_log["run_at"].isoformat()

    return jsonify({
        "last_crawl": last_log,
        "documents":  col_doc_vecs.count_documents({}),
        "terms":      col_term_idx.count_documents({}),
        "raw_pages":  col_raw_pages.count_documents({}),
        "profiles":   db_task1["Profile"].count_documents({}),
    })


_crawl_lock = threading.Lock()
_crawl_running = False


@app.route("/api/crawler/run", methods=["POST"])
def api_crawler_run():
    """
    POST /api/crawler/run — Development/admin endpoint that manually
    triggers an immediate crawl + index rebuild without waiting for the
    3-month scheduled interval (see scheduler.py for the production
    schedule). Runs in a background thread; poll /api/crawl-status for
    progress and results once it completes.
    """
    global _crawl_running

    admin_key = os.environ.get("CRAWLER_ADMIN_KEY")
    if admin_key and request.headers.get("X-Admin-Key") != admin_key:
        return jsonify({"error": "Unauthorized"}), 401

    with _crawl_lock:
        if _crawl_running:
            return jsonify({"status": "already_running"}), 409
        _crawl_running = True

    def _run():
        global _crawl_running
        try:
            from scheduler import crawl, build_index
            crawl()
            build_index()
        finally:
            _crawl_running = False

    threading.Thread(target=_run, daemon=True).start()
    return jsonify({"status": "started",
                     "message": "Crawl + index rebuild started in the background."}), 202


# ── Task 2: News Clustering API ────────────────────────────────────────────────

# Keyword-based fallback classifier (works without K-Means training)
# Used when no trained model is available, or as a supplement.
KEYWORD_CLASSIFIER = {
    "Economics": [
        "economy", "economic", "market", "stock", "gdp", "finance", "financial",
        "trade", "inflation", "budget", "investment", "bank", "banking", "currency",
        "revenue", "profit", "loss", "recession", "growth", "fiscal", "monetary",
        "interest", "rate", "debt", "tax", "tariff", "export", "import", "wage",
        "employment", "unemployment", "bond", "hedge", "fund", "equity", "commodity",
        "oil", "price", "retail", "consumer", "spending", "treasury", "federal",
        "reserve", "corporate", "startup", "venture", "capital", "billion", "million",
        "quarter", "earnings", "dividend", "nasdaq", "dow", "ftse", "crypto",
        "bitcoin", "blockchain", "insurance", "mortgage", "loan", "credit"
    ],
    "Entertainment": [
        "movie", "film", "cinema", "actor", "actress", "director", "hollywood",
        "music", "song", "album", "concert", "singer", "band", "pop", "rock",
        "celebrity", "award", "oscar", "grammy", "bafta", "emmy", "golden",
        "television", "series", "show", "episode", "streaming", "netflix",
        "disney", "hbo", "amazon", "prime", "spotify", "youtube", "viral",
        "trending", "famous", "star", "red carpet", "premiere", "trailer",
        "sequel", "box office", "chart", "record", "tour", "festival",
        "comedy", "drama", "thriller", "animation", "documentary", "reality",
        "fashion", "model", "influencer", "instagram", "tiktok", "social media",
        "game", "gaming", "esports", "sports", "footballer", "athlete", "team"
    ],
    "Politics": [
        "government", "political", "president", "prime minister", "parliament",
        "congress", "senate", "election", "vote", "voting", "democracy",
        "republican", "democrat", "conservative", "liberal", "party", "policy",
        "law", "legislation", "bill", "amendment", "constitution", "minister",
        "secretary", "cabinet", "diplomat", "diplomacy", "foreign", "national",
        "security", "military", "defence", "defense", "war", "conflict",
        "treaty", "sanctions", "nato", "united nations", "un", "eu",
        "european union", "brexit", "immigration", "refugee", "border",
        "protest", "rally", "campaign", "candidate", "coalition", "referendum",
        "corruption", "scandal", "investigation", "justice", "court", "judge",
        "rights", "freedom", "civil", "authority", "federal", "state", "local"
    ]
}


def keyword_classify(text: str) -> dict:
    """
    Keyword-based fallback classifier.
    Scores each category by counting matching keywords in the text.
    Returns the category with the highest score.
    """
    text_lower = text.lower()
    scores = {}
    for category, keywords in KEYWORD_CLASSIFIER.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[category] = score

    total = sum(scores.values())
    
    if total == 0:
        return {
            "category":      "Unknown",
            "confidence":    0.0,
            "method":        "keyword_fallback",
            "model_version": "keyword-1.0",
            "scores":        scores,
        }
        
    best_cat   = max(scores, key=scores.get)
    confidence = round(scores[best_cat] / total, 4)

    return {
        "category":      best_cat,
        "confidence":    confidence,
        "method":        "keyword_fallback",
        "model_version": "keyword-1.0",
        "scores":        scores,
    }


def kmeans_classify(text: str) -> dict:
    """
    K-Means classifier using stored model from news_model_runs.
    Falls back to keyword classifier if no model is trained.
    """
    # Try to load from existing model runs collection
    model_doc = col_model_runs.find_one({}, sort=[("trained_at", -1)])
    if not model_doc:
        return None

    try:
        vectoriser = pickle.loads(bytes.fromhex(model_doc["vectoriser_pkl"]))
        kmeans     = pickle.loads(bytes.fromhex(model_doc["kmeans_pkl"]))
        cluster_map = {int(k): v for k, v in model_doc.get("cluster_map", {}).items()}
        svd        = pickle.loads(bytes.fromhex(model_doc["svd_pkl"])) if model_doc.get("svd_pkl") else None
        normalizer = pickle.loads(bytes.fromhex(model_doc["normalizer_pkl"])) if model_doc.get("normalizer_pkl") else None

        # Preprocess
        text_lower = text.lower()
        text_clean = re.sub(r"[^a-z\s]", " ", text_lower)
        tokens = word_tokenize(text_clean)
        tokens = [stemmer.stem(t) for t in tokens
                  if t not in STOPWORDS and len(t) > 2]
        cleaned = " ".join(tokens)

        X = vectoriser.transform([cleaned])
        if X.nnz == 0:
            return None

        if svd is not None:
            # Same LSA reduction (TruncatedSVD + L2 normalise) fitted during
            # training — the model was trained on this reduced space, not raw TF-IDF.
            X = normalizer.transform(svd.transform(X))
        cluster_id = int(kmeans.predict(X)[0])
        category   = cluster_map.get(cluster_id, "Unknown")

        distances  = kmeans.transform(X)[0]
        min_dist   = distances[cluster_id]
        total_dist = sum(distances) or 1.0
        confidence = round(1.0 - (min_dist / total_dist), 4)

        return {
            "category":      category,
            "cluster_id":    cluster_id,
            "confidence":    confidence,
            "method":        "kmeans",
            "model_version": "1.1-lsa",
        }
    except Exception as e:
        print(f"  [CLASSIFY] K-Means failed: {e}")
        return None


@app.route("/api/news/stats", methods=["GET"])
def api_news_stats():
    """GET /api/news/stats — Cluster distribution and model info."""
    categories = ["Economics", "Entertainment", "Politics"]
    counts = {cat: col_news.count_documents({"category": cat}) for cat in categories}

    model_doc  = col_model_runs.find_one({}, sort=[("trained_at", -1)])
    model_info = {}
    if model_doc:
        ta = model_doc.get("trained_at", "")
        if isinstance(ta, datetime):
            ta = ta.isoformat()
        model_info = {
            "trained_at":  ta,
            "n_clusters":  3,
            "total_docs":  model_doc.get("total_docs", 0),
            "silhouette":  model_doc.get("silhouette_score"),
            "method":      "K-Means (K=3, k-means++)",
        }

    return jsonify({
        "distribution": counts,
        "total":        sum(counts.values()),
        "model":        model_info,
    })


@app.route("/api/news/clusters", methods=["GET"])
def api_news_clusters():
    """GET /api/news/clusters — PCA 2D points for scatter chart."""
    docs = list(col_news.find(
        {"pca_x": {"$exists": True}},
        {"_id": 0, "pca_x": 1, "pca_y": 1, "category": 1, "title": 1}
    ).limit(400))
    return jsonify({"points": docs})


@app.route("/api/news/articles", methods=["GET"])
def api_news_articles():
    """GET /api/news/articles?category=Economics&page=1"""
    category = request.args.get("category", "").strip()
    page     = max(1, int(request.args.get("page", 1)))
    per_page = 10

    query = {"category": category} if category else {}
    total = col_news.count_documents(query)
    docs  = list(col_news.find(
        query,
        {"_id": 0, "title": 1, "url": 1, "category": 1, "source": 1, "published": 1}
    ).skip((page - 1) * per_page).limit(per_page))

    return jsonify({
        "articles": docs,
        "total":    total,
        "page":     page,
        "pages":    math.ceil(total / per_page) if total else 0,
    })


@app.route("/api/news/classify", methods=["POST"])
def api_news_classify():
    """
    POST /api/news/classify  {"text": "..."}

    Classifies user text as Economics / Entertainment / Politics.
    Uses K-Means model if trained, falls back to keyword classifier.
    Saves result to MongoDB.
    """
    body = request.get_json(silent=True) or {}
    text = (body.get("text") or "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Try K-Means first, fall back to keyword classifier
    result = kmeans_classify(text)
    if result is None:
        result = keyword_classify(text)

    # Persist classification result
    col_news_cls.insert_one({
        "input_text":    text[:1000],
        "category":      result["category"],
        "confidence":    result.get("confidence"),
        "method":        result.get("method", "unknown"),
        "model_version": result.get("model_version", "1.0"),
        "classified_at": datetime.now(timezone.utc),
    })

    return jsonify({
        "category":   result["category"],
        "confidence": result.get("confidence"),
        "method":     result.get("method"),
        "text":       text[:200],
    })


@app.route("/api/news/collect", methods=["POST"])
def api_news_collect():
    """POST /api/news/collect — Trigger RSS collection + K-Means training."""
    try:
        from rss_collector import run_full_pipeline
        summary = run_full_pipeline()
        return jsonify({"status": "success", "summary": summary})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ── Static serving ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port  = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f"  DB1: Task1_Search @ {MONGO_URI[:40]}...")
    print(f"  DB2: Task2_Clustering @ {MONGO_URI[:40]}...")
    app.run(debug=debug, port=port)
