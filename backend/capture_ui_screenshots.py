"""
capture_ui_screenshots.py — Captures real, current UI screenshots from the
live app (served by app.py at http://127.0.0.1:5000) using headless Edge.

Run:  python capture_ui_screenshots.py   (with `python app.py` already running)
Output: ../screenshots/ui_*.png
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1440,1400")
options.add_argument("--force-device-scale-factor=1")
options.add_argument("--hide-scrollbars")

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 15)

try:
    # 1. Home / search landing page
    driver.get(BASE_URL)
    wait.until(EC.presence_of_element_located((By.ID, "main-search-input")))
    time.sleep(1.5)  # let fade-in animations settle
    driver.save_screenshot(os.path.join(OUT_DIR, "ui_home_search_page.png"))
    print("Captured: ui_home_search_page.png")

    # 2. Search results for "mental health"
    # Note: the loading skeleton cards share the "result-card" CSS class, so
    # wait for "results-count" instead — it only renders once real results
    # (not skeletons) are shown.
    box = driver.find_element(By.ID, "main-search-input")
    box.clear()
    box.send_keys("mental health")
    driver.find_element(By.ID, "search-btn").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "results-count")))
    time.sleep(1.0)
    driver.save_screenshot(os.path.join(OUT_DIR, "ui_search_mental_health.png"))
    print("Captured: ui_search_mental_health.png")

    # 2b. Search for an author name (author/profile links visible)
    box = driver.find_element(By.ID, "main-search-input")
    box.clear()
    box.send_keys("Deborah Lycett")
    driver.find_element(By.ID, "search-btn").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "results-count")))
    time.sleep(1.0)
    driver.save_screenshot(os.path.join(OUT_DIR, "ui_search_author.png"))
    print("Captured: ui_search_author.png")

    # 3. News tab — overview
    driver.find_element(By.ID, "tab-news").click()
    wait.until(EC.presence_of_element_located((By.ID, "news-tab-overview")))
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(OUT_DIR, "ui_news_overview.png"))
    print("Captured: ui_news_overview.png")

    # 4. News tab — clusters (PCA scatter)
    driver.find_element(By.ID, "news-tab-clusters").click()
    time.sleep(1.8)
    driver.save_screenshot(os.path.join(OUT_DIR, "ui_news_clusters.png"))
    print("Captured: ui_news_clusters.png")

    # 5. News tab — classify
    driver.find_element(By.ID, "news-tab-classify").click()
    wait.until(EC.presence_of_element_located((By.ID, "classify-textarea")))
    time.sleep(0.8)
    driver.save_screenshot(os.path.join(OUT_DIR, "ui_classify_panel.png"))
    print("Captured: ui_classify_panel.png")

    ta = driver.find_element(By.ID, "classify-textarea")
    ta.clear()
    ta.send_keys("The central bank raised interest rates again to control rising inflation.")
    driver.find_element(By.ID, "classify-btn").click()
    result_el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "classify-result")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result_el)
    time.sleep(1.0)
    driver.save_screenshot(os.path.join(OUT_DIR, "ui_classify_result.png"))
    print("Captured: ui_classify_result.png")

finally:
    driver.quit()

print("Done.")
