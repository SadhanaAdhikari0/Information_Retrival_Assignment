"""
generate_diagram.py — ST7071CEM System Architecture Diagram (Light Academic Theme)
====================================================================================
Generates a highly professional, print-friendly conceptual system diagram 
for the IR assignment report.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# Output path
os.makedirs("static", exist_ok=True)
OUTPUT_PATH = "static/conceptual_diagram.png"


def draw_box(ax, x, y, w, h, text, subtext=None,
             facecolor="#ffffff", edgecolor="#3b82f6", textcolor="#1e293b",
             fontsize=10, subfontsize=8, alpha=1.0, style="round,pad=0.2", zorder=3):
    """Draw a rounded rectangle with text for academic reports."""
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=style,
                         facecolor=facecolor,
                         edgecolor=edgecolor,
                         linewidth=1.8,
                         alpha=alpha,
                         zorder=zorder)
    ax.add_patch(box)
    
    # Shadow effect for professional depth
    shadow = FancyBboxPatch((x - w/2 + 0.08, y - h/2 - 0.08), w, h,
                            boxstyle=style,
                            facecolor="#000000",
                            edgecolor="none",
                            alpha=0.08,
                            zorder=zorder-1)
    ax.add_patch(shadow)

    if subtext:
        ax.text(x, y + h*0.12, text, ha="center", va="center",
                fontsize=fontsize, color=textcolor, fontweight="bold",
                wrap=True, zorder=zorder+1)
        ax.text(x, y - h*0.2, subtext, ha="center", va="center",
                fontsize=subfontsize, color="#475569",
                wrap=True, zorder=zorder+1)
    else:
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fontsize, color=textcolor, fontweight="bold",
                wrap=True, zorder=zorder+1)


def draw_arrow(ax, x1, y1, x2, y2, color="#64748b", lw=2):
    """Draw a clean arrow between two points."""
    ax.annotate("",
                xy=(x2, y2), xycoords="data",
                xytext=(x1, y1), textcoords="data",
                arrowprops=dict(
                    arrowstyle="-|>,head_width=0.2,head_length=0.3",
                    color=color,
                    lw=lw,
                    connectionstyle="arc3,rad=0.0",
                ),
                zorder=2)


def draw_section_label(ax, x, y, text, color="#0f172a"):
    ax.text(x, y, text, ha="center", va="center",
            fontsize=12, color=color, fontweight="bold",
            zorder=6)


fig, ax = plt.subplots(figsize=(20, 15))
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")
ax.set_xlim(0, 20)
ax.set_ylim(0, 15)
ax.axis("off")

# ─────────────────────────────────────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────────────────────────────────────
ax.text(10, 14.2, "ST7071CEM — System Architecture & Workflow Pipeline",
        ha="center", va="center", fontsize=18, color="#0f172a", fontweight="bold")
ax.text(10, 13.8, "Task 1: Vertical Search Engine   |   Task 2: News Document Clustering",
        ha="center", va="center", fontsize=12, color="#475569")

# Divider
ax.plot([1.0, 19.0], [13.4, 13.4], color="#cbd5e1", lw=2)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION BACKGROUNDS (Light academic zones)
# ─────────────────────────────────────────────────────────────────────────────
# Task 1 Zone (Light Blue)
task1_bg = FancyBboxPatch((0.5, 0.5), 8.5, 12.5,
                           boxstyle="round,pad=0.2",
                           facecolor="#f0f9ff",
                           edgecolor="#bae6fd",
                           linewidth=2,
                           alpha=0.5,
                           zorder=1)
ax.add_patch(task1_bg)

# Task 2 Zone (Light Green)
task2_bg = FancyBboxPatch((11.0, 0.5), 8.5, 12.5,
                           boxstyle="round,pad=0.2",
                           facecolor="#f0fdf4",
                           edgecolor="#bbf7d0",
                           linewidth=2,
                           alpha=0.5,
                           zorder=1)
ax.add_patch(task2_bg)

# Shared Infrastructure Zone (Light Purple/Gray)
shared_bg = FancyBboxPatch((7.0, 0.8), 6.0, 3.5,
                            boxstyle="round,pad=0.2",
                            facecolor="#f8fafc",
                            edgecolor="#e2e8f0",
                            linewidth=2,
                            alpha=0.9,
                            zorder=2)
ax.add_patch(shared_bg)

# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — VERTICAL SEARCH ENGINE (Left)
# ─────────────────────────────────────────────────────────────────────────────
X1 = 4.75
draw_section_label(ax, X1, 12.6, "TASK 1: Vertical Search Engine", "#0369a1")

# Blocks
boxes_t1 = [
    (11.8, "Coventry PurePortal Seed URL", "pureportal.coventry.ac.uk/en/organisations/...", "#ffffff", "#0284c7"),
    (10.7, "Requests + BeautifulSoup Crawler", "Extracts: Outputs · Profiles · Pagination (robots.txt-checked)", "#ffffff", "#0284c7"),
    (9.6,  "Data Extraction & Filtering", "Title · Authors · Date · URLs · Abstract", "#ffffff", "#0284c7"),
    (8.5,  "NLP Preprocessing Pipeline", "Lowercase → Tokenise → Stop-words → Stemming", "#ffffff", "#0284c7"),
    (7.4,  "TF-IDF Vectorisation", "TF(t,d) × IDF(t) · L2-Normalised Vectors", "#ffffff", "#0284c7"),
    (6.3,  "MongoDB — vertical_search_engine", "doc_vectors · term_index · crawl_log", "#f8fafc", "#475569"),
    (5.2,  "User Search Query", "Raw text → Preprocessed → Query Vector", "#fffbeb", "#d97706"),
    (4.1,  "Cosine Similarity Ranking", "cos(θ) = (Q·D) / (||Q|| × ||D||) · Top-K=10", "#ffffff", "#0284c7"),
    (3.0,  "Vertical Search Engine UI", "Clickable Titles · Profiles · Relevance Scores", "#f0fdfa", "#0d9488")
]

for y, title, sub, bg, edge in boxes_t1:
    draw_box(ax, X1, y, 4.4, 0.7, title, sub, facecolor=bg, edgecolor=edge)

# Scheduler mini-box
draw_box(ax, X1 + 3.2, 10.7, 1.8, 0.5, "APScheduler", "90-Day Interval", facecolor="#fef2f2", edgecolor="#ef4444", fontsize=8, subfontsize=7)
draw_arrow(ax, X1 + 2.3, 10.7, X1 + 2.2, 10.7, color="#ef4444", lw=1.5)

# Arrows T1
for i in range(len(boxes_t1)-1):
    draw_arrow(ax, X1, boxes_t1[i][0] - 0.35, X1, boxes_t1[i+1][0] + 0.35, color="#94a3b8")

# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — NEWS DOCUMENT CLUSTERING (Right)
# ─────────────────────────────────────────────────────────────────────────────
X2 = 15.25
draw_section_label(ax, X2, 12.6, "TASK 2: News Document Clustering", "#15803d")

# Blocks
boxes_t2 = [
    (11.8, "Live BBC RSS + Wikipedia", "Economics · Entertainment · Politics", "#ffffff", "#16a34a"),
    (10.7, "RSS Feed Collector (feedparser)", "Title · Content · URL · Date · Source", "#ffffff", "#16a34a"),
    (9.6,  "Data Cleaning & Deduplication", "HTML Stripping · Duplicate Detection", "#ffffff", "#16a34a"),
    (8.5,  "NLP Preprocessing Pipeline", "Lowercase → Punctuation → Tokenise → Stop-words", "#ffffff", "#16a34a"),
    (7.4,  "TF-IDF Vectorisation", "Feature Extraction · Sparse Matrix", "#ffffff", "#16a34a"),
    (6.3,  "K-Means Clustering (K=3)", "k-means++ init · Centroid Optimisation", "#ffffff", "#16a34a"),
]

for y, title, sub, bg, edge in boxes_t2:
    draw_box(ax, X2, y, 4.4, 0.7, title, sub, facecolor=bg, edgecolor=edge)

# Document count note
draw_box(ax, X2 + 3.2, 10.7, 1.8, 0.5, "Dataset Size", "198 real documents total", facecolor="#fefce8", edgecolor="#eab308", fontsize=8, subfontsize=7)
draw_arrow(ax, X2 + 2.3, 10.7, X2 + 2.2, 10.7, color="#eab308", lw=1.5)

# Split into 3 clusters
draw_box(ax, X2 - 1.8, 5.2, 1.8, 0.6, "Economics", "Cluster 0", facecolor="#ffffff", edgecolor="#16a34a")
draw_box(ax, X2,       5.2, 1.8, 0.6, "Entertainment", "Cluster 1", facecolor="#ffffff", edgecolor="#8b5cf6")
draw_box(ax, X2 + 1.8, 5.2, 1.8, 0.6, "Politics", "Cluster 2", facecolor="#ffffff", edgecolor="#ef4444")

draw_arrow(ax, X2, 5.95, X2 - 1.8, 5.5, color="#94a3b8")
draw_arrow(ax, X2, 5.95, X2, 5.5, color="#94a3b8")
draw_arrow(ax, X2, 5.95, X2 + 1.8, 5.5, color="#94a3b8")

# Join back to PCA
draw_box(ax, X2, 4.1, 4.4, 0.7, "PCA Dimensionality Reduction", "2D Scatter Plot Visualisation", "#ffffff", "#16a34a")
draw_arrow(ax, X2 - 1.8, 4.9, X2, 4.45, color="#94a3b8")
draw_arrow(ax, X2, 4.9, X2, 4.45, color="#94a3b8")
draw_arrow(ax, X2 + 1.8, 4.9, X2, 4.45, color="#94a3b8")

# User Classification
draw_box(ax, X2, 3.0, 4.4, 0.7, "User Text Classification", "Preprocess → Vectorise → Nearest Centroid", "#fffbeb", "#d97706")
draw_arrow(ax, X2, 3.75, X2, 3.35, color="#94a3b8")

# Arrows T2 top
for i in range(len(boxes_t2)-1):
    draw_arrow(ax, X2, boxes_t2[i][0] - 0.35, X2, boxes_t2[i+1][0] + 0.35, color="#94a3b8")

# ─────────────────────────────────────────────────────────────────────────────
# SHARED INFRASTRUCTURE (Bottom Center)
# ─────────────────────────────────────────────────────────────────────────────
draw_section_label(ax, 10, 4.0, "Shared Infrastructure", "#475569")

draw_box(ax, 10, 3.0, 4.0, 0.7, "MongoDB Atlas (Database)", "Shared Document Store", "#ffffff", "#64748b")
draw_box(ax, 10, 1.8, 4.0, 0.7, "Flask REST API (Backend)", "Serves Search & Clustering Endpoints", "#ffffff", "#64748b")
draw_box(ax, 10, 0.7, 4.0, 0.7, "React Frontend (UI)", "Unified Two-Tab Web Application", "#ffffff", "#64748b")

draw_arrow(ax, 10, 2.65, 10, 2.15, color="#94a3b8")
draw_arrow(ax, 10, 1.45, 10, 1.05, color="#94a3b8")

# Connect T1 & T2 to Shared DB
draw_arrow(ax, X1, 5.95, 8.0, 3.0, color="#64748b", lw=1.5) # DB to DB
draw_arrow(ax, X2, 2.65, 12.0, 3.0, color="#64748b", lw=1.5) # Classify to DB

# Connect UIs to Backend
draw_arrow(ax, X1, 2.65, 8.0, 1.8, color="#0d9488", lw=1.5)
draw_arrow(ax, X2, 3.0, 12.0, 1.8, color="#d97706", lw=1.5)

# ─────────────────────────────────────────────────────────────────────────────
# LEGEND
# ─────────────────────────────────────────────────────────────────────────────
legend_y = -0.5
# Handled safely below plot area, so let's skip legend and just rely on clear labels.

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight')
print(f"✅ Generated crisp academic diagram at: {OUTPUT_PATH}")
