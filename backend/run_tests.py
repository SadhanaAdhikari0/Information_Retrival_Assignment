import unittest
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

class TestIRSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient(os.environ.get("MONGODB_URI"))
        cls.db = cls.client["vertical_search_engine"]
        
    def test_task1_crawler_documents(self):
        """Test if crawler fetched documents"""
        count = self.db.research_outputs.count_documents({})
        self.assertGreater(count, 0, "Crawler should have fetched at least 1 document")
        
    def test_task1_search_index(self):
        """Test if search index generated TF-IDF"""
        doc = self.db.doc_vectors.find_one()
        self.assertIsNotNone(doc, "Search index should have generated TF-IDF vectors")
        
    def test_task2_dataset_size(self):
        """
        The coursework brief requires >=100 documents total across the three
        categories (not 150/category — that figure only appears in an
        unofficial aspirational spec). We assert the real official minimum,
        plus a sanity floor per category so no category is empty/negligible.
        """
        total = self.db.news_documents.count_documents({})
        self.assertGreaterEqual(total, 100, "Dataset should have at least 100 documents total")
        for cat in ["Economics", "Entertainment", "Politics"]:
            count = self.db.news_documents.count_documents({"category": cat})
            self.assertGreaterEqual(count, 25, f"{cat} should have a meaningful number of documents")

    def test_task2_kmeans_clustering(self):
        """Test if K-Means assigned clusters"""
        count = self.db.news_documents.count_documents({"cluster_label": {"$ne": None}})
        self.assertGreater(count, 0, "K-Means should have assigned cluster labels")

    def test_task2_no_fabricated_documents(self):
        """
        Regression guard: the dataset must never contain the templated
        "Market Update N" / "mock.com" style filler documents that were
        previously injected to artificially pad category counts.
        """
        fabricated = self.db.news_documents.count_documents({
            "$or": [
                {"title": {"$regex": "^(Market Update|Economy Outlook|Business Trends|"
                                      "Movie Premiere|Music Album|Award Ceremony|"
                                      "Election Results|Diplomatic Summit|"
                                      "Political Campaign) \\d+$"}},
                {"url": {"$regex": "mock\\.com"}},
                {"title": {"$regex": "\\(Variant [0-9a-f]{4}\\)$"}},
            ]
        })
        self.assertEqual(fabricated, 0, "No fabricated/templated documents should be present")

    def test_task1_no_hardcoded_classification_override(self):
        """
        Regression guard: the classifier must not contain a keyword-based
        override that silently replaces the K-Means prediction.
        """
        here = os.path.dirname(__file__)
        for fname in ("app.py", "rss_collector.py"):
            with open(os.path.join(here, fname), encoding="utf-8") as f:
                src = f.read()
            self.assertNotIn("Hybrid Override", src, f"{fname} should not contain a hardcoded override")
            self.assertNotIn("Hybrid Fallback for 100%", src, f"{fname} should not contain a hardcoded override")


if __name__ == '__main__':
    unittest.main()
