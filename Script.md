# ST7071CEM Information Retrieval – Final Video Presentation Script

**Student Name:** Sadhana Adhikari
**Batch:** MSc Batch 8
**Module:** Information Retrieval (ST7071CEM)
**Target Duration:** 12–15 Minutes

---

## Important Instructions for Recording
- Make sure to have your Flask backend running (`python app.py`) and your React frontend running (`npm run dev`) before you start recording.
- Keep your MongoDB Atlas cluster open in a browser tab.
- Keep your IDE (VS Code) open with `scheduler.py`, `app.py`, and `rss_collector.py` ready to show.
- Speak naturally and confidently. The text below is a guide—feel free to adjust the wording slightly to sound more like your natural speaking voice, but ensure you hit all the technical points.

---

## 1. Introduction & Overview (Estimated Time: 1:30)
**[Visuals: Start by sharing your screen showing the home page of your React web application.]**

**Speaker:**
"Hello Sir/Mam, I am Sadhana Adhikari from MSc Batch 8. My assignment module is Information Retrieval. 

Today, I am going to demonstrate my full-stack web application, which was developed to solve two distinct Information Retrieval challenges as outlined in the assignment brief. 

The assignment is divided into two primary tasks:
Task 1 required building a custom Vertical Search Engine. I focused my domain on the Centre for Healthcare and Community Transformation at Coventry University. The goal was to build a system capable of crawling research publications and researcher profiles, indexing them mathematically, and returning highly relevant results for user queries.

Task 2 involved building a Machine Learning Document Classifier. The objective here was to collect unlabelled news articles and use Unsupervised Machine Learning—specifically K-Means clustering—to automatically group them into three distinct categories: Economics, Entertainment, and Politics.

My system architecture is completely decoupled. The frontend is built using React.js and Vite, providing a fast and dynamic user interface. The backend is powered by Python and Flask, which handles all the heavy lifting for Information Retrieval, Natural Language Processing, and Machine Learning. For persistent storage, I am using MongoDB Atlas, a cloud-based NoSQL database, which allows me to store flexible JSON-like documents for both tasks.

Let's begin by diving into Task 1: The Vertical Search Engine."

---

## 2. Task 1: Data Collection & Web Crawling (Estimated Time: 1:30)
**[Visuals: Open your IDE and show the `scheduler.py` file, specifically scrolling to the `crawl()` function and `fetch_page()` function.]**

**Speaker:**
"The foundation of any search engine is data collection. For this, I developed a highly reliable web crawler in Python. 

Initially, scraping the Coventry University PurePortal directly via HTML was challenging because of Cloudflare bot protection. To solve this, I designed my crawler to target the XML RSS feed endpoints instead. As you can see here in my `scheduler.py` file, the crawler loops through paginated RSS feeds. 

I implemented strict ethical crawling policies. Before any request is made, my system parses the domain's `robots.txt` file and respects the 'Crawl-Delay' directives. I also ensure the crawler sends a descriptive User-Agent identifying it as an educational bot. 

**[Visuals: Switch to MongoDB Atlas and show the `Task1_Search` database, specifically the `research_publication` and `Profile` collections.]**

Through this automated process, I successfully scraped 100% of the target dataset, yielding 81 research outputs and 117 author profiles. In MongoDB Atlas, you can see the structured metadata we extract: the title, the authors, publication dates, and most importantly, the abstract and full text. This rich, structured data forms the basis of our search index."

---

## 3. Task 1: Preprocessing & Indexing (Estimated Time: 2:00)
**[Visuals: Switch back to the IDE. Show the `_preprocess_for_index()` and `build_index()` functions in `scheduler.py`.]**

**Speaker:**
"Raw text cannot be searched efficiently, so the next critical step is text preprocessing. In my pipeline, I use the Natural Language Toolkit (NLTK) to clean the data. First, I convert all text to lowercase and remove non-alphanumeric characters. Then, I apply tokenization to break sentences into individual words. Next, I remove standard English stop-words as well as custom domain-specific stop words like 'coventry' or 'university' which add no informational value. Finally, I apply the Porter Stemming algorithm to reduce words to their root form—for example, converting 'computing' and 'computed' into 'comput'.

Once the text is normalized, I build an Inverted Index using the Term Frequency-Inverse Document Frequency (TF-IDF) weighting scheme. I implemented this mathematically from scratch rather than relying on external search libraries. 

For each term in a document, I calculate the Term Frequency (TF), which is the count of the term divided by the total terms in that document. Then, I calculate the Inverse Document Frequency (IDF) using Laplace smoothing to prevent division-by-zero errors. In my `build_index` function, you will notice I specifically applied a weight boosting technique: I multiply the title terms by 3 and author names by 2. This ensures that if a user searches for a specific author or paper title, those documents receive a significantly higher relevance score.

Finally, the TF-IDF vector for each document is L2-normalized so that longer documents don't gain an unfair advantage, and the vectors are stored in our MongoDB `doc_vectors` collection."

---

## 4. Task 1: Search, Retrieval & Ranking (Estimated Time: 1:30)
**[Visuals: Open the React frontend in your browser. Type a query like 'Healthcare' or 'Rehabilitation' into the search bar and press search. Show the results.]**

**Speaker:**
"Now, let's look at how query processing and ranking works in practice. When a user enters a query on the frontend, the text goes through the exact same NLP preprocessing pipeline—tokenization, stop-word removal, and stemming. 

**[Visuals: Switch to `app.py` in the IDE and highlight the `build_query_vector()` and `cosine_similarity()` functions.]**

The backend generates an L2-normalized TF-IDF query vector. To rank the documents, I implemented the Vector Space Model (VSM) using Cosine Similarity. Because both the query vector and the document vectors are L2-normalized, calculating the cosine of the angle between them is highly efficient—it simplifies to the dot product of their shared terms. 

Documents with a cosine similarity score greater than zero are returned, ranked in descending order of relevance. As you can see on the frontend, the most mathematically relevant documents appear at the top, complete with their metadata and a clean user interface that handles pagination."

---

## 5. Task 2: Document Clustering Data Collection (Estimated Time: 1:30)
**[Visuals: Switch to `rss_collector.py` in the IDE.]**

**Speaker:**
"Moving on to Task 2, the objective was to implement unsupervised machine learning to classify news articles into Economics, Entertainment, and Politics.

First, I needed a dataset. I built an automated RSS collector in `rss_collector.py` that connects to live BBC News feeds. It fetches the latest news, cleans the HTML, and extracts the core content. Because live RSS feeds only show recent articles, I also integrated the Wikipedia Extracts API to dynamically top up the dataset with genuine, citable articles until I reached a balanced dataset of at least 150 documents per category, totaling over 450 documents.

I implemented fingerprinting using MD5 hashing to ensure that absolutely no duplicate articles are stored in the database."

---

## 6. Task 2: K-Means Implementation & Evaluation (Estimated Time: 2:00)
**[Visuals: In `rss_collector.py`, scroll to the `train_kmeans()` function.]**

**Speaker:**
"For the clustering algorithm, I used the `scikit-learn` library. The text is passed through a `TfidfVectorizer` which extracts unigrams and bigrams, creating a sparse matrix of up to 5000 features. 

Because K-Means calculates Euclidean distance, it performs poorly in highly sparse, high-dimensional spaces—a phenomenon known as the curse of dimensionality. To solve this, I applied Latent Semantic Analysis (LSA). I used `TruncatedSVD` to perform Principal Component Analysis (PCA), reducing the 5000 dimensions down to a dense matrix of around 100 components, and then L2-normalized the matrix.

I then trained the K-Means algorithm with K=3, using the `k-means++` initialization method for faster and more accurate convergence. Since K-Means is unsupervised, it clusters the data blindly. After training, my script uses a majority-vote logic to map the predicted clusters back to our human-readable labels: Economics, Entertainment, and Politics.

**[Visuals: Go to the frontend and navigate to the Task 2 clustering visualizer / classify page.]**

For evaluation, the backend calculates the Silhouette Score to measure cluster cohesion and separation, as well as Macro F1 and Accuracy scores. The model states, including the pickled vectorizer and K-Means objects, are stored in MongoDB. I also compute 3D PCA coordinates for every document so we can visualize the cluster distributions on the frontend."

---

## 7. Task 2: Live Classification Demonstration (Estimated Time: 1:00)
**[Visuals: On the React frontend, go to the text classification tool. Paste a paragraph about a recent political event or a movie, and click classify.]**

**Speaker:**
"Let me demonstrate the classification API. When I paste a piece of text here, it is sent to the Flask backend. 

The backend loads the most recently trained K-Means model from MongoDB. The text is preprocessed, transformed by the saved TF-IDF vectorizer, reduced using the exact same SVD components, and then K-Means predicts the nearest centroid. 

As you can see, the application correctly predicts the category and returns a confidence score based on the normalized inverse distance to the centroid. As a failsafe, I also implemented a keyword-based classifier that acts as a fallback if the machine learning model is unavailable or confidence is exceptionally low."

---

## 8. Limitations & Future Improvements (Estimated Time: 1:00)
**[Visuals: Return to the home screen or keep the visualizer on screen.]**

**Speaker:**
"While the system meets the assignment requirements robustly, there are limitations. 
First, standard TF-IDF does not capture semantic context or word meanings like modern dense embeddings (such as Word2Vec or BERT) do. Synonyms might be missed in Task 1. 
Second, K-Means assumes spherical clusters, which isn't always true for complex text data. 

In the future, I would improve the system by implementing BM25 ranking instead of standard TF-IDF for better term saturation limits. I would also introduce lemmatization instead of simple Porter Stemming to preserve actual dictionary words, and utilize transformer models for the clustering task to capture deep semantic relationships."

---

## 9. Conclusion (Estimated Time: 0:30)
**Speaker:**
"In conclusion, I have successfully developed a fully decoupled Information Retrieval system. I implemented mathematical TF-IDF and Cosine Similarity from scratch for a robust vertical search engine, and successfully engineered an automated data pipeline to train an unsupervised K-Means classifier for document clustering. 

Thank you for your time and for reviewing my assignment."

---
---

# Viva / Examiner Preparation Questions
*Use these to prepare for questions your examiner might ask you based on your specific implementation.*

### 1. What is the difference between crawling HTML and crawling RSS, and why did you choose RSS?
**Answer:** Crawling HTML requires parsing complex, changing DOM structures and often triggers bot protections like Cloudflare. I chose to target XML RSS feeds in my `scheduler.py` because RSS is highly structured, designed for machine consumption, and allowed me to reliably extract metadata without being blocked.

### 2. How did you respect ethical crawling policies?
**Answer:** In my `check_robots_txt` and `can_fetch` functions, I implemented a parser that dynamically reads the target domain's `robots.txt` file before making requests. I also used polite crawl delays (e.g., `time.sleep()`) and a descriptive User-Agent header so the server knows who is crawling them.

### 3. Explain how you implemented the Vector Space Model.
**Answer:** In `scheduler.py`, I built a TF-IDF index. I calculate Term Frequency for each word in a document, then multiply it by the Inverse Document Frequency (using Laplace smoothing). I then L2-normalize this vector. For searching, I do the same to the user's query, and calculate the Cosine Similarity (the dot product of the two normalized vectors) in `app.py` to rank the results.

### 4. Why did you boost the Title and Author names during indexing?
**Answer:** A word appearing in a title is significantly more indicative of the document's subject than a word buried in the abstract. In my `build_index` function, I appended the title multiplied by 3, and author names multiplied by 2 to the text corpus before vectorization. This mathematically increases their Term Frequency, ensuring they rank higher for relevant searches.

### 5. Why did you use L2 Normalization on your TF-IDF vectors?
**Answer:** L2 Normalization ensures that the length of every document vector is exactly 1. This completely removes the bias of document length—a very long document with many words won't outrank a short, highly relevant document just because it has higher raw term counts. It also simplifies Cosine Similarity to a simple dot product.

### 6. What NLP techniques did you use in preprocessing?
**Answer:** I used NLTK. I lowercased all text, stripped non-alphanumeric characters, tokenized the strings, removed standard and custom stop-words (like 'university' or 'coventry'), and finally applied Porter Stemming to reduce words to their root forms (e.g., 'computing' to 'comput').

### 7. What is Porter Stemming and what is its limitation?
**Answer:** It's a heuristic algorithm that chops off the ends of words to find their root (stem). The limitation is that it often produces non-dictionary words (like "univers" instead of "university") and can suffer from over-stemming or under-stemming. Lemmatization would be a more advanced alternative as it uses vocabulary analysis to return proper base words.

### 8. Explain how K-Means Clustering works in your Task 2.
**Answer:** K-Means is an unsupervised algorithm. It initializes 3 random centroids (using k-means++ for better placement). It calculates the Euclidean distance between every document vector and the centroids, assigns each document to the closest centroid, and then moves the centroid to the mean of the assigned documents. It repeats this until the centroids stop moving (convergence).

### 9. Why did you use PCA / TruncatedSVD before K-Means?
**Answer:** TF-IDF creates a highly sparse matrix of 5,000 dimensions. Euclidean distance (which K-Means uses) behaves poorly in high dimensions due to the "curse of dimensionality"—distances between points become almost uniform. By using Latent Semantic Analysis (TruncatedSVD), I reduced the data to a dense matrix of ~100 components, making the Euclidean distance meaningful and improving cluster quality.

### 10. How did you evaluate the performance of your Unsupervised K-Means model?
**Answer:** Because it is unsupervised, the model doesn't know the labels during training. After convergence, I mapped the clusters to my known categories using majority voting. I then calculated the Silhouette Score (to measure cluster separation), and post-hoc metrics like Accuracy, Macro F1, and a Confusion Matrix to evaluate against the true labels from my dataset.

### 11. How did you ensure you had enough data for Task 2?
**Answer:** My `rss_collector.py` pulls live articles from BBC feeds. Because live feeds only have recent articles, I implemented a fallback that queries the Wikipedia Extracts API to dynamically pull genuine, distinct articles related to Economics, Entertainment, and Politics until I hit a minimum of 150 documents per category.

### 12. How did you prevent duplicate articles in your database?
**Answer:** I implemented an MD5 fingerprinting function (`doc_fingerprint`) that hashes the combination of the article's title and URL. Before inserting an article into MongoDB, I check if that fingerprint already exists.

### 13. What happens if your K-Means model fails or isn't trained yet when a user tries to classify text?
**Answer:** In `app.py`, I implemented a fallback Keyword Classifier. It holds a dictionary of highly relevant terms for each category. If the ML model is missing, or if the user types a very short query that exactly matches a category keyword (like "politics"), the system calculates a score based on keyword counts and returns a classification safely.

### 14. What are the limitations of the TF-IDF and Cosine Similarity approach?
**Answer:** It relies entirely on exact lexical matching. If a document uses the word "physician" and the user searches for "doctor", TF-IDF will not find a match because it does not understand semantic meaning or synonyms. It also suffers from term saturation (TF scales logarithmically but doesn't cap like BM25).

### 15. Why use MongoDB instead of a relational database like MySQL?
**Answer:** Information Retrieval deals with unstructured or semi-structured data. My documents have varying fields—some have authors, some have profile links, and the TF-IDF vectors are dynamic dictionaries. A NoSQL document store like MongoDB allows me to store this hierarchical JSON-like data naturally without rigid schemas.

### 16. What is Laplace Smoothing and where did you use it?
**Answer:** I used it in my IDF calculation: `log((N + 1) / (freq + 1)) + 1`. It adds 1 to the numerator and denominator to prevent division by zero in cases where a term's frequency might be zero, and prevents the IDF of a term that appears in every document from becoming exactly zero.

### 17. Can you explain the architecture of your application?
**Answer:** It's a decoupled client-server architecture. The backend is a stateless Flask API that handles data scraping, indexing, and machine learning. The frontend is a React Single Page Application (SPA) that communicates with the backend via RESTful APIs. Both connect to MongoDB Atlas for persistence.

### 18. How do you handle pagination in your search results?
**Answer:** In `app.py`, my `search_documents` function returns all documents with a score > 0. I sort them by score, and then use array slicing `[start : start + RESULTS_PER_PAGE]` to return only the subset for the requested page. The API also returns `total` and `pages` metadata so the React frontend can render pagination buttons.

### 19. How did you implement autocomplete/suggestions?
**Answer:** I created a `/api/suggestions` endpoint. It takes the user's partial query and performs a MongoDB regular expression search (`$regex`) against the `title` field of the indexed documents, returning up to 6 matching titles.

### 20. If you had more time, how would you improve the document clustering?
**Answer:** Instead of K-Means with TF-IDF, I would use pre-trained contextual embeddings like sentence-transformers (BERT). Text embeddings capture deep semantic meaning. I would then cluster those dense vectors using an algorithm like HDBSCAN, which handles noise and non-spherical clusters much better than K-Means.
