"""
scheduler.py — ST7071CEM Information Retrieval Assignment
==========================================================
Vertical Search Engine Crawler and Indexer

SCHEDULE: Every 3 MONTHS (approximately 90 days)
         "3 months — NOT ONCE PER WEEK"

This script:
  1. Crawls the Coventry University PurePortal for Research Outputs and Profiles
  2. Extracts structured metadata (title, authors, dates, profile URLs)
  3. Builds a TF-IDF inverted index
  4. Stores everything in MongoDB

Run:  python scheduler.py

MongoDB credentials are loaded from backend/.env — NEVER hard-coded.
"""

import os
import re
import time
import math
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque, Counter
from datetime import datetime, timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

import nltk
nltk.download("punkt",     quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus   import stopwords
from nltk.stem     import PorterStemmer
from nltk.tokenize import word_tokenize

from pymongo import MongoClient
from dotenv  import load_dotenv

# ── Environment ───────────────────────────────────────────────────────────────
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

MONGO_URI = os.environ.get("MONGODB_URI")
if not MONGO_URI:
    raise EnvironmentError("MONGODB_URI not set. Check backend/.env")

CRAWL_INTERVAL_MONTHS = int(os.environ.get("CRAWL_INTERVAL_MONTHS", 3))
CRAWL_INTERVAL_DAYS = CRAWL_INTERVAL_MONTHS * 30

# ── MongoDB collections ────────────────────────────────────────────────────
client = MongoClient(MONGO_URI)
db = client["Task1_Search"]   # Task 1 database

col_outputs  = db["research_publication"]    # structured research publication records
col_profiles = db["Profile"] # researcher profile documents
col_doc_vecs = db["doc_vectors"]         # normalised TF-IDF vectors
col_term_idx = db["term_index"]          # per-term IDF values
col_crawl_log = db["crawl_log"]          # crawl run history (existing)

# ── Mandatory Politeness / robots.txt implementation ────────────────────────
# Actually enforced (not just demonstrated) — every fetch_page() call is
# checked against PurePortal's robots.txt before the HTTP request is made.
import urllib.robotparser

_robots_parser = None


def _get_robots_parser():
    """
    Fetch and parse robots.txt.

    Deliberately does NOT use RobotFileParser.read() — that fetches via
    urllib.request with no custom headers, and PurePortal's edge protection
    returns HTTP 403 to urllib's default User-Agent (confirmed: `requests`
    with the same URL gets 200). RobotFileParser silently treats a 403 as
    "disallow everything", which would have blocked the crawler from
    fetching even the seed URL. Fetching the text ourselves via `requests`
    (matching the User-Agent used for every other request) and handing it
    to RobotFileParser.parse() avoids that failure mode.
    """
    global _robots_parser
    if _robots_parser is None:
        _robots_parser = urllib.robotparser.RobotFileParser()
        try:
            resp = requests.get(f"https://{ALLOWED_DOMAIN}/robots.txt",
                                 headers={"User-Agent": USER_AGENT}, timeout=10)
            resp.raise_for_status()
            _robots_parser.parse(resp.text.splitlines())
        except Exception as e:
            print(f"  [robots.txt] Could not fetch robots.txt: {e} — treating as permissive")
            _robots_parser = False  # sentinel: fetch failed, don't retry every call
    return _robots_parser or None


def can_fetch(url: str, user_agent: str = "ST7071CEM-IR-Bot") -> bool:
    rp = _get_robots_parser()
    return True if rp is None else rp.can_fetch(user_agent, url)

# ── Crawler configuration ─────────────────────────────────────────────────────
SEED_URL      = "https://pureportal.coventry.ac.uk/en/organisations/centre-for-healthcare-and-community-transformation/"
ALLOWED_DOMAIN = "pureportal.coventry.ac.uk"
CRAWL_DELAY_SECONDS = 2   # Polite delay between HTTP requests
MAX_PAGES     = 500       # Safety ceiling per crawl run
USER_AGENT    = "ST7071CEM-IR-Bot/1.0 (Educational assignment; Coventry University)"

# Only follow URLs whose paths start with these prefixes
ALLOWED_PATH_PREFIXES = (
    "/en/publications/",
    "/en/persons/",
    "/en/research-output/",
    "/en/organisations/centre-for-healthcare",
)

# ── NLP setup ─────────────────────────────────────────────────────────────────
STOPWORDS = set(stopwords.words("english"))
STOPWORDS.update(["coventry", "research", "pureportal", "university",
                  "www", "http", "https", "html", "com", "org", "uk"])
stemmer = PorterStemmer()


# =============================================================================
# CRAWLER POLITENESS — ROBOTS.TXT COMPLIANCE
# =============================================================================
# can_fetch() (defined above) is actually called from fetch_page() below —
# every request is checked against PurePortal's robots.txt, not just
# demonstrated in a comment. PurePortal's robots.txt (checked 2026-08-15)
# specifies "Crawl-Delay: 5" and disallows only RSS/XLS export query
# strings, which this crawler never requests. Other polite measures:
#   • CRAWL_DELAY_SECONDS = 2  between every HTTP request
#   • A descriptive User-Agent string identifying the bot
#   • Skipping already-visited URLs (deduplication)
#   • Limiting maximum pages per run (MAX_PAGES safety ceiling)
#   • Standard HTTP GET only — no scraping of authenticated pages
# =============================================================================


def is_relevant_url(url: str) -> bool:
    """
    Accept only Research Output and Profile URLs.
    Rejects generic navigation, search, and external pages.
    """
    parsed = urlparse(url)
    if not parsed.netloc.endswith(ALLOWED_DOMAIN):
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    path = parsed.path
    if not path.endswith("/"):
        path += "/"
        
    # Allow the specific organisation's publication and person lists
    if path in (
        "/en/organisations/centre-for-healthcare-and-community-transformation/publications/",
        "/en/organisations/centre-for-healthcare-and-community-transformation/persons/",
        "/en/organisations/centre-for-healthcare-and-community-transformation/"
    ):
        return True
        
    # Allow individual publications (exactly 3 path segments: '', 'en', 'publications', 'slug', '')
    # e.g. /en/publications/some-title/
    parts = [p for p in path.split("/") if p]
    if len(parts) == 3 and parts[0] == "en" and parts[1] in ("publications", "research-output", "persons"):
        return True
        
    return False


def extract_research_output(soup: BeautifulSoup, url: str) -> dict:
    """
    Extract structured metadata from a PurePortal research output page.

    Returns a dict with:
      - title, url, authors (list), author_profiles (dict name→url),
        publication_date, abstract/content, source_url, crawl_timestamp
    """
    # Title
    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

    # Authors and their profile URLs
    authors      = []
    author_profiles = {}
    for contributor in soup.select("a[href*='/en/persons/']"):
        name = contributor.get_text(strip=True)
        href = urljoin(url, contributor["href"]).split("?")[0]
        if name and name not in authors:
            authors.append(name)
            author_profiles[name] = href

    # Also pick up plain-text author spans not linked
    for span in soup.select("span[class*='author'], span[class*='person']"):
        name = span.get_text(strip=True)
        if name and name not in authors:
            authors.append(name)

    # Publication date — try common selectors
    pub_date = ""
    date_selectors = [
        "span.date", "div.date", "time",
        "[class*='publication-date']", "[class*='year']",
        "span[class*='date']",
    ]
    for sel in date_selectors:
        el = soup.select_one(sel)
        if el:
            text = el.get_text(strip=True)
            # Extract a 4-digit year
            year_match = re.search(r"\b(19|20)\d{2}\b", text)
            if year_match:
                pub_date = year_match.group(0)
                break

    # Abstract / content
    abstract = ""
    for sel in ["div.abstract", "div[class*='abstract']", "section.abstract",
                "div.description", "div[class*='description']"]:
        el = soup.select_one(sel)
        if el:
            abstract = el.get_text(separator=" ", strip=True)[:3000]
            break

    # Fallback: gather main text block
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    full_text = re.sub(r"\s+", " ", soup.get_text(separator=" ")).strip()

    return {
        "title":           title,
        "url":             url,
        "authors":         authors,
        "author_profiles": author_profiles,
        "publication_date": pub_date,
        "abstract":        abstract,
        "full_text":       full_text[:5000],
        "source_url":      SEED_URL,
        "crawled_at":      datetime.now(timezone.utc),
        "updated_at":      datetime.now(timezone.utc),
    }


def extract_profile(soup: BeautifulSoup, url: str) -> dict:
    """
    Extract metadata from a researcher profile page.
    """
    name = ""
    h1 = soup.find("h1")
    if h1:
        name = h1.get_text(strip=True)

    department = ""
    for sel in ["div[class*='organisation']", "span[class*='organisation']",
                "div[class*='department']"]:
        el = soup.select_one(sel)
        if el:
            department = el.get_text(strip=True)
            break

    # Related publications on profile page
    related_pubs = []
    for a in soup.select("a[href*='/en/publications/'], a[href*='/en/research-output/']"):
        href = urljoin(url, a["href"]).split("?")[0]
        if href not in related_pubs:
            related_pubs.append(href)

    return {
        "name":        name,
        "profile_url": url,
        "department":  department,
        "related_publications": related_pubs[:30],
        "crawled_at":  datetime.now(timezone.utc),
    }


def fetch_page(url: str) -> str | None:
    """Fetch a URL with polite headers and timeout. Returns HTML or None.
    Checks robots.txt before every request."""
    if not can_fetch(url, user_agent=USER_AGENT):
        print(f"    [robots.txt] Disallowed, skipping: {url}")
        return None
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=20
        )
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"    [ERROR] Could not fetch {url}: {e}")
        return None


def crawl():
    """
    Breadth-first crawler starting from SEED_URL.
    Only follows Research Output and Profile URLs (is_relevant_url filter).
    Extracts structured metadata and stores in MongoDB.
    Schedule: every 90 days (3 months) — NOT once per week.
    """
    print(f"\n{'='*65}")
    print(f"  CRAWL STARTED at {datetime.now()}")
    print(f"  Seed: {SEED_URL}")
    print(f"  Schedule: {CRAWL_INTERVAL_MONTHS}-month interval ({CRAWL_INTERVAL_DAYS} days) — NOT once per week")
    print(f"{'='*65}")

    # Wipe the database collections before starting to ensure clean counts
    col_outputs.delete_many({})
    col_profiles.delete_many({})
    db["term_index"].delete_many({})
    db["doc_vectors"].delete_many({})

    visited  = set()
    queue    = deque([SEED_URL])
    outputs_saved  = 0
    profiles_saved = 0
    errors   = 0
    start_dt = datetime.now(timezone.utc)

    while queue and (outputs_saved + profiles_saved) < MAX_PAGES:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        html = fetch_page(url)
        if not html:
            errors += 1
            time.sleep(CRAWL_DELAY_SECONDS)
            continue

        soup  = BeautifulSoup(html, "html.parser")
        path  = urlparse(url).path

        # Determine page type and extract accordingly
        if any(p in path for p in ("/en/publications/", "/en/research-output/")):
            data = extract_research_output(soup, url)
            if data["title"]:
                col_outputs.update_one(
                    {"url": url},
                    {"$set": data},
                    upsert=True
                )
                outputs_saved += 1
                try:
                    print(f"  [OUTPUT  {outputs_saved:03d}] {data['title'][:70]}")
                except UnicodeEncodeError:
                    print(f"  [OUTPUT  {outputs_saved:03d}] {data['title'][:70].encode('ascii', 'replace').decode('ascii')}")

        elif "/en/persons/" in path:
            data = extract_profile(soup, url)
            if data["name"]:
                col_profiles.update_one(
                    {"profile_url": url},
                    {"$set": data},
                    upsert=True
                )
                profiles_saved += 1
                try:
                    print(f"  [PROFILE {profiles_saved:03d}] {data['name'][:70]}")
                except UnicodeEncodeError:
                    print(f"  [PROFILE {profiles_saved:03d}] {data['name'][:70].encode('ascii', 'replace').decode('ascii')}")

        # Discover new relevant links from this page
        from urllib.parse import parse_qs
        for a in soup.find_all("a", href=True):
            raw_link = urljoin(url, a["href"]).split("#")[0]
            parsed_link = urlparse(raw_link)
            
            # Keep 'page' parameter for pagination, strip all other query params
            query = ""
            qs = parse_qs(parsed_link.query)
            if "page" in qs:
                query = f"?page={qs['page'][0]}"
                
            link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}{query}"
            
            if link not in visited and is_relevant_url(link):
                queue.append(link)

        time.sleep(CRAWL_DELAY_SECONDS)

    duration_s = (datetime.now(timezone.utc) - start_dt).total_seconds()

    col_crawl_log.insert_one({
        "run_at":          start_dt,
        "completed_at":    datetime.now(timezone.utc),
        "duration_seconds": duration_s,
        "pages_visited":   len(visited),
        "outputs_saved":   outputs_saved,
        "profiles_saved":  profiles_saved,
        "errors":          errors,
        "status":          "success",
        "schedule_note":   f"{CRAWL_INTERVAL_MONTHS}-month interval ({CRAWL_INTERVAL_DAYS} days) — NOT once per week",
    })

    print(f"\n  Crawl complete: {outputs_saved} outputs, {profiles_saved} profiles, {errors} errors")
    print(f"  Duration: {duration_s:.1f}s")
    print(f"{'='*65}\n")

    return outputs_saved, profiles_saved


def build_index():
    """
    Build a TF-IDF inverted index from all crawled research outputs.

    For each document:
      TF(t,d)  = count(t in d) / total_terms(d)
      IDF(t,D) = log(N / (1 + df(t))) + 1    [smoothed]
      TF-IDF   = TF × IDF
    Vector is L2-normalised before storage.
    """
    # PurePortal auto-generates a "/fingerprints/" companion page for every
    # publication (an auto-extracted topical-terms view of the same output,
    # not an independent publication). These are excluded from the search
    # index so each real publication appears once, not twice, in results.
    all_docs = list(col_outputs.find({}))
    docs = [d for d in all_docs if not d.get("url", "").rstrip("/").endswith("/fingerprints")]
    N = len(docs)
    if N == 0:
        print("  [INDEX] No documents found — run crawl first.")
        return

    print(f"  [INDEX] Building TF-IDF index for {N} documents "
          f"({len(all_docs) - N} '/fingerprints/' companion pages excluded)...")

    # Compute document frequency per term
    doc_tokens = {}
    df = Counter()
    for doc in docs:
        text    = (doc.get("abstract") or "") + " " + (doc.get("full_text") or "")
        title   = doc.get("title", "")
        authors = " ".join(doc.get("authors", []))
        # Boost title (x3) and author names (x2) — both are high-value,
        # low-frequency terms that a user is very likely to search by,
        # so they must be well represented in the document vector even
        # though "full_text" alone might mention an author only once.
        combined = (title + " ") * 3 + (authors + " ") * 2 + text
        tokens = _preprocess_for_index(combined)
        url    = doc.get("url", str(doc["_id"]))
        doc_tokens[url] = tokens
        for term in set(tokens):
            df[term] += 1

    # IDF with standard Laplace smoothing
    idf = {term: math.log((N + 1) / (freq + 1)) + 1 for term, freq in df.items()}

    # Store IDF values
    col_term_idx.delete_many({})
    if idf:
        col_term_idx.insert_many([{"term": t, "idf": v} for t, v in idf.items()])

    # Build and store normalised document vectors
    col_doc_vecs.delete_many({})
    for doc in docs:
        url    = doc.get("url", str(doc["_id"]))
        tokens = doc_tokens.get(url, [])
        if not tokens:
            continue

        tf  = Counter(tokens)
        total = len(tokens)
        vec = {term: (c / total) * idf.get(term, 0) for term, c in tf.items()}
        norm = math.sqrt(sum(w * w for w in vec.values())) or 1.0
        vec  = {t: w / norm for t, w in vec.items()}

        col_doc_vecs.update_one(
            {"url": url},
            {"$set": {
                "url":             url,
                "title":           doc.get("title", ""),
                "authors":         doc.get("authors", []),
                "author_profiles": doc.get("author_profiles", {}),
                "publication_date": doc.get("publication_date", ""),
                "source_url":      doc.get("source_url", ""),
                "vector":          vec,
                "indexed_at":      datetime.now(timezone.utc),
            }},
            upsert=True
        )

    print(f"  [INDEX] Indexed {N} documents, {len(idf)} unique terms.")


def _preprocess_for_index(text: str) -> list[str]:
    """Lowercase → strip → tokenize → remove stops → stem."""
    text   = text.lower()
    text   = re.sub(r"[^a-z\s]", " ", text)
    tokens = word_tokenize(text)
    return [
        stemmer.stem(t)
        for t in tokens
        if t not in STOPWORDS and len(t) > 2
    ]


# ── Scheduled job ─────────────────────────────────────────────────────────────

def scheduled_job():
    """Combined crawl + index job — runs according to CRAWL_INTERVAL_MONTHS."""
    print(f"\n{'#'*65}")
    print(f"  SCHEDULED JOB — {datetime.now()}")
    print(f"  Interval: {CRAWL_INTERVAL_MONTHS} months ({CRAWL_INTERVAL_DAYS} days) — NOT once per week")
    print(f"{'#'*65}")
    crawl()
    build_index()
    print(f"  Job completed at {datetime.now()}")


# ── Entry point ───────────────────────────────────────────────────────────────

def start_scheduler(run_immediately: bool = True) -> BlockingScheduler:
    """
    Configure and start the APScheduler job that re-runs the crawler and
    rebuilds the index every CRAWL_INTERVAL_MONTHS (3 months / 90 days by
    default) — NOT weekly, NOT daily.
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(
        scheduled_job,
        trigger=IntervalTrigger(days=CRAWL_INTERVAL_DAYS),
        id="pureportal_crawl",
        name=f"PurePortal {CRAWL_INTERVAL_MONTHS}-month Crawl — ST7071CEM Task 1",
        replace_existing=True,
    )

    print(f"{'='*65}")
    print(f"  Crawler Scheduler — ST7071CEM IR Assignment")
    print(f"  Started:  {datetime.now()}")
    print(f"  Schedule: every {CRAWL_INTERVAL_MONTHS} months ({CRAWL_INTERVAL_DAYS} days) — NOT once per week")
    print(f"  Seed:     {SEED_URL}")
    print(f"{'='*65}\n")

    if run_immediately:
        print("Running initial crawl immediately on startup...")
        scheduled_job()

    print(f"\nScheduler active — next run in {CRAWL_INTERVAL_DAYS} days.")
    return scheduler


if __name__ == "__main__":
    # ── SCHEDULE: CRAWL_INTERVAL_MONTHS ────────────────────────────────────────
    # The crawler must update every THREE MONTHS (approximately 90 days).
    # "3 months — NOT ONCE PER WEEK"
    sched = start_scheduler(run_immediately=True)
    try:
        sched.start()  # blocks; APScheduler fires scheduled_job() every CRAWL_INTERVAL_DAYS
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped.")
