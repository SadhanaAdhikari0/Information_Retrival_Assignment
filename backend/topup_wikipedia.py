"""
Top up each Task 2 category with real Wikipedia article extracts (without
wiping the real RSS articles already collected), then retrain K-Means.
"""
from rss_collector import (
    col_news, fetch_wikipedia_articles, WIKIPEDIA_TOPICS,
    store_articles, train_kmeans, MIN_DOCS_PER_CATEGORY,
)

for category in ["Economics", "Entertainment", "Politics"]:
    current = col_news.count_documents({"category": category})
    needed = max(0, MIN_DOCS_PER_CATEGORY - current)
    print(f"{category}: currently {current}, need {needed} more")
    if needed > 0:
        extra = fetch_wikipedia_articles(category, WIKIPEDIA_TOPICS[category], needed)
        added = store_articles({category: extra})
        print(f"  -> stored {added} new Wikipedia documents for {category}")

print()
for category in ["Economics", "Entertainment", "Politics"]:
    print(category, col_news.count_documents({"category": category}))

print("\nRetraining K-Means on the combined real dataset...")
summary = train_kmeans()
print(summary)
