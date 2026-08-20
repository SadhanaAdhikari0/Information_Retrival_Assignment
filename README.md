# Coventry University Information Retrieval Assignment (ST7071CEM)
**Author:** Sadhana Adhikari
**Domain:** Centre for Healthcare and Community Transformation (Coventry University)

## Overview
This repository contains the full source code for the ST7071CEM Information Retrieval assignment. It is a full-stack web application combining a custom Search Engine (Task 1) and a Machine Learning Document Classifier (Task 2).

### Task 1: Vertical Search Engine
- **Custom Web Crawler:** Automatically paginates and parses XML RSS feeds from Coventry University's PurePortal to bypass Cloudflare bot protection, collecting 100% of the target research outputs (81) and profiles (117).
- **TF-IDF & Vector Space Model:** Implements mathematical Term Frequency-Inverse Document Frequency weighting from scratch to index documents.
- **Cosine Similarity:** Compares a user's search query vector against document vectors to rank results by exact mathematical relevance.

### Task 2: Document Clustering
- **K-Means Clustering:** Implements unsupervised K-Means Machine Learning (K=3) using `scikit-learn` to classify text into Health, Business, or Sports categories.
- **Preprocessing:** Includes rigorous NLP text preprocessing (tokenization, stop-word removal, and lowercasing) before vectorization using `TfidfVectorizer`.

---

## Tech Stack
- **Backend:** Python, Flask, PyMongo, Scikit-Learn, NLTK, BeautifulSoup4
- **Database:** MongoDB Atlas (Cloud NoSQL)
- **Frontend:** React.js, Vite, Vanilla CSS

---

## How to Run the Application

The application is fully decoupled. You must start the Python Backend and the React Frontend simultaneously.

### 1. Start the Backend (Python / Flask)

Open a terminal and navigate to the backend folder:
```bash
cd backend
```

Since a virtual environment is already provided, you can activate it and run the server directly:

For Windows (PowerShell/CMD):
```bash
.\venv\Scripts\activate
python app.py
```
*(Alternatively, you can just run `.\venv\Scripts\python.exe app.py`)*

*Note: The server will start on `http://127.0.0.1:5000`.*

### 2. Start the Frontend (React / Vite)

Open a **new** terminal window and navigate to the frontend folder:
```bash
cd frontend
```

Install the Node modules:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
*Note: The frontend will start locally on `http://localhost:3000`. Open this URL in your web browser to use the application.*


---

## How to use the Web Crawler
The web crawler is designed to be highly reliable and fast. To manually trigger the crawler and update your TF-IDF vectors, simply open a new terminal in the `backend` folder and run:
```bash
python scheduler.py
```
This will wipe the old data, scrape the university portal fresh, generate the term indexes, and populate the MongoDB Atlas cluster within 10 seconds.
