"""
visualize_clusters.py — ST7071CEM Information Retrieval Assignment
====================================================================
Task 2: Generates the K-Means cluster visualisation figure.

Reads the PCA(2D) coordinates that train_kmeans() (see rss_collector.py)
already computed and stored per-document (pca_x, pca_y, cluster_label) and
plots a real scatter chart — one point per genuine collected document,
coloured by its K-Means-assigned cluster label.

Run:  python visualize_clusters.py
Output: visualization/kmeans_clusters.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["vertical_search_engine"]
col_news = db["news_documents"]
col_meta = db["news_model_runs"]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "visualization")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "kmeans_clusters.png")

CATEGORY_COLORS = {
    "Economics":     "#2563eb",   # blue
    "Entertainment": "#db2777",   # pink
    "Politics":      "#059669",   # green
    "Unknown":       "#9ca3af",   # grey — fallback only
}


def main():
    docs = list(col_news.find(
        {"pca_x": {"$exists": True, "$ne": None}},
        {"_id": 0, "pca_x": 1, "pca_y": 1, "cluster_label": 1, "category": 1}
    ))
    if not docs:
        print("No PCA coordinates found — run rss_collector.train_kmeans() first.")
        return

    model_doc = col_meta.find_one({}, sort=[("trained_at", -1)])
    sil = model_doc.get("silhouette_score") if model_doc else None
    acc = model_doc.get("accuracy") if model_doc else None

    fig, ax = plt.subplots(figsize=(9, 7), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#fafafa")

    for cat, color in CATEGORY_COLORS.items():
        if cat == "Unknown":
            continue
        pts = [d for d in docs if (d.get("cluster_label") or "Unknown") == cat]
        if not pts:
            continue
        xs = [d["pca_x"] for d in pts]
        ys = [d["pca_y"] for d in pts]
        ax.scatter(xs, ys, s=28, alpha=0.75, c=color, label=f"{cat} (n={len(pts)})",
                   edgecolors="white", linewidths=0.4)

    title = "K-Means Clustering (K=3) — PCA 2D Projection of Real News/Reference Documents"
    subtitle_parts = []
    if sil is not None:
        subtitle_parts.append(f"silhouette={sil:.3f}")
    if acc is not None:
        subtitle_parts.append(f"cluster-to-category accuracy={acc:.1%}")
    subtitle = "  |  ".join(subtitle_parts)

    ax.set_title(title, fontsize=13, fontweight="bold", pad=14)
    if subtitle:
        ax.text(0.5, 1.02, subtitle, transform=ax.transAxes, ha="center",
                fontsize=9.5, color="#555555")
    ax.set_xlabel("Principal Component 1", fontsize=10)
    ax.set_ylabel("Principal Component 2", fontsize=10)
    ax.legend(loc="best", fontsize=9, frameon=True)
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, facecolor="white")
    print(f"Saved: {OUTPUT_PATH}  ({len(docs)} points plotted)")


if __name__ == "__main__":
    main()
