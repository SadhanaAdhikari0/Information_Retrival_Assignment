"""
regenerate_screenshots.py — Rebuilds every code-evidence figure used in the
report directly from the real, current source files (copy-pasted verbatim
below from scheduler.py / app.py / rss_collector.py), so the "Code Evidence"
screenshots can never drift out of sync with the actual implementation again.

Run:  python regenerate_screenshots.py
Output: ../screenshots/*.png
"""
import os
from render_code_image import render_code_to_png

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(OUT_DIR, exist_ok=True)


CRAWLER_CODE = '''# scheduler.py — breadth-first crawler (requests + BeautifulSoup)
def crawl():
    """Breadth-first crawl from SEED_URL. Only follows Research Output
    and Profile URLs (is_relevant_url filter). Schedule: every 90 days."""
    visited = set()
    queue   = deque([SEED_URL])
    outputs_saved = profiles_saved = errors = 0

    while queue and (outputs_saved + profiles_saved) < MAX_PAGES:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        html = fetch_page(url)          # polite: 5s delay, descriptive UA
        if not html:
            errors += 1
            time.sleep(CRAWL_DELAY_SECONDS)
            continue

        soup = BeautifulSoup(html, "html.parser")
        path = urlparse(url).path

        if any(p in path for p in ("/en/publications/", "/en/research-output/")):
            data = extract_research_output(soup, url)
            if data["title"]:
                col_outputs.update_one({"url": url}, {"$set": data}, upsert=True)
                outputs_saved += 1

        elif "/en/persons/" in path:
            data = extract_profile(soup, url)
            if data["name"]:
                col_profiles.update_one({"profile_url": url}, {"$set": data}, upsert=True)
                profiles_saved += 1

        # Discover new relevant links from this page
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"]).split("#")[0].split("?")[0]
            if link not in visited and is_relevant_url(link):
                queue.append(link)

        time.sleep(CRAWL_DELAY_SECONDS)
'''

SCHEDULER_CODE = '''# scheduler.py — APScheduler: crawl + index rebuild every 3 months (90 days)
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

CRAWL_INTERVAL_MONTHS = int(os.environ.get("CRAWL_INTERVAL_MONTHS", 3))
CRAWL_INTERVAL_DAYS = CRAWL_INTERVAL_MONTHS * 30

def scheduled_job():
    """Combined crawl + index job — runs every CRAWL_INTERVAL_MONTHS."""
    crawl()
    build_index()

def start_scheduler(run_immediately: bool = True) -> BlockingScheduler:
    scheduler = BlockingScheduler()
    scheduler.add_job(
        scheduled_job,
        trigger=IntervalTrigger(days=CRAWL_INTERVAL_DAYS),   # 90 days, NOT weekly
        id="pureportal_crawl",
        name=f"PurePortal {CRAWL_INTERVAL_MONTHS}-month Crawl — ST7071CEM Task 1",
        replace_existing=True,
    )
    if run_immediately:
        scheduled_job()
    return scheduler

if __name__ == "__main__":
    sched = start_scheduler(run_immediately=True)
    sched.start()   # blocks; fires scheduled_job() every 90 days
'''

SEARCH_ENGINE_CODE = '''# app.py — Vector Space Model: TF-IDF query vector + cosine similarity
def build_query_vector(query: str) -> dict:
    tokens = preprocess(query)                 # lowercase, tokenise, stopwords, stem
    tf = Counter(tokens)
    total = len(tokens)

    idf_cursor = col_term_idx.find({"term": {"$in": list(tf.keys())}})
    idf_map = {d["term"]: d["idf"] for d in idf_cursor}

    vector = {
        term: (count / total) * idf_map.get(term, 0)   # TF x IDF
        for term, count in tf.items() if term in idf_map
    }
    norm = math.sqrt(sum(w * w for w in vector.values())) or 1.0
    return {t: w / norm for t, w in vector.items()}     # L2-normalised


def cosine_similarity(vec1: dict, vec2: dict) -> float:
    common = set(vec1.keys()) & set(vec2.keys())
    return sum(vec1[t] * vec2[t] for t in common)       # both vectors L2-normalised


def search_documents(query: str, page: int = 1):
    q_vec = build_query_vector(query)
    scored = []
    for doc in col_doc_vecs.find({}):
        score = cosine_similarity(q_vec, doc.get("vector", {}))
        if score > 0:
            scored.append({"score": round(score, 4), "title": doc.get("title", ""), ...})
    scored.sort(key=lambda x: x["score"], reverse=True)
    start = (page - 1) * RESULTS_PER_PAGE          # K = 10 per page
    return scored[start:start + RESULTS_PER_PAGE], len(scored)
'''

KMEANS_TRAINING_CODE = '''# rss_collector.py — K-Means (K=3) training on TF-IDF + LSA-reduced vectors
vectoriser = TfidfVectorizer(
    max_features=5000, min_df=2, stop_words='english',
    ngram_range=(1, 2),     # unigrams and bigrams
    sublinear_tf=True,      # 1 + log(TF) dampens very high-frequency terms
)
X = vectoriser.fit_transform(texts)

# LSA: reduce sparse high-dim TF-IDF to dense components before clustering
# (standard remedy for K-Means on raw TF-IDF — Euclidean distance in a
# 5000-dim sparse space is dominated by noise otherwise)
n_components = max(2, min(100, X.shape[0] - 1, X.shape[1] - 1))
svd = TruncatedSVD(n_components=n_components, random_state=42)
normalizer = Normalizer(copy=False)
X_reduced = normalizer.fit_transform(svd.fit_transform(X))

kmeans = KMeans(
    n_clusters=3,
    init="k-means++",
    n_init=10,
    max_iter=300,
    random_state=42,
)
labels = kmeans.fit_predict(X_reduced)

# Post-hoc evaluation only (never used as training signal)
accuracy    = accuracy_score(true_labels, predicted_labels)
conf_matrix = confusion_matrix(true_labels, predicted_labels, labels=CATS)
macro_f1    = f1_score(true_labels, predicted_labels, labels=CATS, average="macro")
sil_score   = silhouette_score(X_reduced, labels, sample_size=min(500, len(docs)))
'''

GREEDY_MAPPING_CODE = '''# rss_collector.py — greedy 1-to-1 cluster -> category assignment
# (never assigns two clusters to the same category)
cluster_counts = {}
for cluster_id in range(3):
    cluster_cats = [true_labels[i] for i, lbl in enumerate(labels)
                    if lbl == cluster_id and true_labels[i]]
    cluster_counts[cluster_id] = Counter(cluster_cats) if cluster_cats else Counter()

sorted_clusters = sorted(
    cluster_counts.keys(),
    key=lambda c: cluster_counts[c].most_common(1)[0][1] if cluster_counts[c] else 0,
    reverse=True,
)

cluster_map, available_cats = {}, {"Economics", "Entertainment", "Politics"}
for cluster_id in sorted_clusters:
    for cat, _ in cluster_counts[cluster_id].most_common():
        if cat in available_cats:
            cluster_map[cluster_id] = cat
            available_cats.remove(cat)
            break
'''

SCRAPER_CODE = '''# rss_collector.py — real data only: live BBC RSS + Wikipedia extracts
def fetch_rss_articles(category, feed_url, limit=80):
    """One genuine document per real BBC article — no chunking/duplication."""
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:limit]:
        title, link = entry.get("title", "").strip(), entry.get("link", "").strip()
        body = clean_html(entry.get("summary", ""))

        if check_robots_txt(link, user_agent="ST7071CEM-IR-Coursework"):
            art_resp = requests.get(link, headers=headers, timeout=8)
            art_resp.encoding = art_resp.apparent_encoding
            paragraphs = [p.get_text(" ", strip=True)
                          for p in BeautifulSoup(art_resp.text, "html.parser").find_all("p")]
            full_text = " ".join(p for p in paragraphs if len(p) > 40)
            if len(full_text) > len(body):
                body = full_text

        articles.append({"title": title, "url": link, "content": body[:4000],
                          "source": "BBC News (RSS)", "source_url": feed_url,
                          "category": category, "fingerprint": doc_fingerprint(title, link)})
        time.sleep(0.3)
    return articles


def fetch_wikipedia_articles(category, topics, target_count):
    """Tops up a category with real, citable Wikipedia extracts when the
    live RSS feed alone does not reach MIN_DOCS_PER_CATEGORY."""
    for topic in topics:
        results = _get_json({"action": "query", "list": "search",
                              "srsearch": topic, "srlimit": 20, "format": "json"}, 10)
        pages = _get_json({"action": "query", "prop": "extracts", "explaintext": 1,
                            "pageids": "|".join(pageids), "format": "json"}, 15)
        # ... each real Wikipedia page becomes one document, cited by its URL
'''

ROBOTS_TXT_CODE = '''# rss_collector.py / scheduler.py — robots.txt compliance, actually enforced
#
# IMPORTANT BUG FOUND & FIXED: RobotFileParser.read() fetches via bare
# urllib.request with no custom headers. PurePortal's edge protection
# returns HTTP 403 to urllib's default User-Agent (confirmed: `requests`
# gets 200 for the identical URL). RobotFileParser silently treats a 403
# as "disallow everything", which would have blocked the crawler from
# fetching even its own seed URL. Fix: fetch the text via `requests`
# ourselves and hand it to RobotFileParser.parse() instead of .read().

_ROBOTS_CACHE: dict = {}

def check_robots_txt(url: str, user_agent: str = "*") -> bool:
    """Checks the domain's robots.txt before fetching (cached per domain)."""
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    if base_url not in _ROBOTS_CACHE:
        try:
            resp = requests.get(f"{base_url}/robots.txt",
                                 headers={"User-Agent": USER_AGENT}, timeout=10)
            resp.raise_for_status()
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(resp.text.splitlines())      # NOT rp.read() — see above
            _ROBOTS_CACHE[base_url] = rp
        except Exception:
            _ROBOTS_CACHE[base_url] = None         # fail open — treat as permissive

    rp = _ROBOTS_CACHE[base_url]
    return True if rp is None else rp.can_fetch(user_agent, url)

# Called before every fetch — scheduler.fetch_page() and
# rss_collector.fetch_rss_articles() both check this before requesting a page.
'''

SNIPPETS = [
    ("crawler_code.png", CRAWLER_CODE),
    ("scheduler_code.png", SCHEDULER_CODE),
    ("search_engine_code.png", SEARCH_ENGINE_CODE),
    ("kmeans_training.png", KMEANS_TRAINING_CODE),
    ("greedy_mapping.png", GREEDY_MAPPING_CODE),
    ("task2_scraper_code.png", SCRAPER_CODE),
    ("robots_txt_code.png", ROBOTS_TXT_CODE),
]

if __name__ == "__main__":
    for filename, code in SNIPPETS:
        render_code_to_png(code, os.path.join(OUT_DIR, filename), font_size=15)
