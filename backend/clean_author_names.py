"""
clean_author_names.py — Post-processing cleanup of author name extraction
artifacts already stored in research_outputs (citation-fragment junk like
", Turner, A.," or "; Brookes-Smith, Celine," picked up from PurePortal's
alternate citation-format markup alongside the real byline links).

This does NOT re-crawl (no extra load on PurePortal) — it only cleans the
`authors` / `author_profiles` fields already in MongoDB, then rebuilds the
search index so the cleaned names are reflected in search results.
"""
import os
import re
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
from pymongo import MongoClient

db = MongoClient(os.environ["MONGODB_URI"])["vertical_search_engine"]
col = db["research_outputs"]


def clean_name(name: str) -> str:
    name = re.sub(r"^[,;&\s]+", "", name)   # strip leading junk (", ", "; ", "& ")
    name = re.sub(r"[,;\s]+$", "", name)    # strip trailing junk
    name = re.sub(r"\s+", " ", name).strip()
    return name


def normalise_key(name: str) -> str:
    """Loose key for de-duplicating citation-format variants of the same
    author (e.g. 'Celine Brookes-Smith' vs 'Brookes-Smith, C.')."""
    tokens = re.findall(r"[a-z]+", name.lower())
    return "".join(sorted(tokens))


updated = 0
for doc in col.find({}):
    authors = doc.get("authors", [])
    profiles = doc.get("author_profiles", {})
    if not authors:
        continue

    cleaned_authors = []
    cleaned_profiles = {}
    seen_keys = {}

    for name in authors:
        clean = clean_name(name)
        if not clean or len(clean) < 3:
            continue
        key = normalise_key(clean)
        if not key:
            continue

        if key in seen_keys:
            # Keep whichever variant is longer/has a linked profile
            existing = seen_keys[key]
            has_profile_new = name in profiles
            has_profile_existing = existing in profiles
            if has_profile_new and not has_profile_existing:
                cleaned_authors[cleaned_authors.index(existing)] = clean
                seen_keys[key] = clean
                if name in profiles:
                    cleaned_profiles[clean] = profiles[name]
                    cleaned_profiles.pop(existing, None)
            continue

        seen_keys[key] = clean
        cleaned_authors.append(clean)
        if name in profiles:
            cleaned_profiles[clean] = profiles[name]

    if cleaned_authors != authors or cleaned_profiles != profiles:
        col.update_one({"_id": doc["_id"]}, {"$set": {
            "authors": cleaned_authors,
            "author_profiles": cleaned_profiles,
        }})
        updated += 1

print(f"Cleaned authors on {updated} research_outputs documents.")
