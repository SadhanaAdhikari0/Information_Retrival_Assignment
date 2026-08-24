# ST7071CEM Information Retrieval Assignment - Video Demo Script

**Student Name:** Sadhana Adhikari  
**Project:** Vertical Search Engine (Task 1) & Document Clustering (Task 2)  
**Estimated Time:** ~10 minutes

---

## 1. Introduction & Architecture Overview (0:00 - 1:30)
**[Visuals: Screen recording showing the React Frontend homepage, slowly panning through the interface]**

**Speaker:** 
"Hello, my name is Sadhana Adhikari, and my Coventry ID is 17625409. Welcome to my comprehensive video demonstration for the Information Retrieval module ST7071CEM. 

In this video, I will be walking you through my vertical search engine and news clustering web application, which was built to solve two primary challenges: 
First, Task 1, which is a custom Vertical Search Engine designed to scrape, index, and search research profiles from Coventry University.
Second, Task 2, which involves building a Machine Learning Document Classifier capable of clustering unlabelled news articles into specific categories.   

Before diving into the functionalities, I want to briefly touch upon the architecture. I adopted a modern, decoupled tech stack to ensure scalability and high performance. The frontend is built using React.js and Vite, providing a fast, dynamic, and responsive user experience. The backend API is developed in Python using the Flask framework, which is excellent for integrating Machine Learning and Natural Language Processing pipelines. For data persistence, I utilized MongoDB Atlas—a cloud-based NoSQL database—because its document-based structure pairs perfectly with the nested nature of scraped web data and JSON responses.  

**[Visuals: Briefly show the terminal windows side-by-side where npm run dev and python app.py are actively running]**

As you can see here in my terminal, both the React frontend and the Python Flask backend are currently running locally on my machine, fully decoupled but communicating seamlessly."  

---

## 2. Task 1: Data Collection & Web Crawler (1:30 - 3:00)
**[Visuals: Show a side-by-side comparison of the original Coventry University PurePortal on one half of the screen, and your web application's search interface on the other half. Then open VS Code and show the `scheduler.py` file (which contains your crawling and RSS parsing logic), followed by the terminal window showing the crawler running.]**

**Speaker:**
"Let's begin with Task 1: The Vertical Search Engine. Here you can see a quick side-by-side comparison of the original Coventry University PurePortal on the left, and my custom application on the right. My goal was to extract this exact data and make it instantly searchable through my platform. 

Since a search engine is only as good as its data, the first step was building a reliable web crawler. 

I designed a custom scraper using Python's BeautifulSoup and Requests libraries to parse XML RSS feeds from Coventry University's PurePortal. One of the main challenges here was bypassing Cloudflare bot protections. By targeting the RSS endpoints rather than raw HTML, and by implementing proper header rotation and pagination logic, I successfully collected 100% of the target dataset, which includes research outputs and author profiles.

If we look at the MongoDB Atlas collection here, you can see the raw documents being stored. Each document contains essential metadata like the title, author, URL, and a snippet of the content. This clean data serves as the foundation for our indexing phase."

---

## 3. Task 1: The Vector Space Model & Search Execution (3:00 - 5:30)
**[Visuals: Switch back to the React Frontend. Type a search query like 'Healthcare' or 'Computer Science' into the search bar, but do not hit enter yet.]**

**Speaker:**
"Now, let's move to the frontend to see the search engine in action. When I type a query into this search bar, a series of complex mathematical operations occurs behind the scenes in the Flask backend.

**[Visuals: Hit enter. Show the results populating on the screen. Then briefly open VS Code and show the `app.py` file (specifically the `build_query_vector()` and `cosine_similarity()` functions) to prove the math, before returning to the frontend.]**

The engine does not use simple keyword matching. Instead, it utilizes the Vector Space Model. 
During the indexing phase, every scraped document is passed through an NLP pipeline—tokenized, lowercased, stop-words removed, and stemmed using the Porter Stemmer. 

I then implemented the Term Frequency-Inverse Document Frequency (TF-IDF) algorithm from scratch. This calculates a mathematical weight for every term in every document. Words that appear frequently in one document but rarely across the entire corpus receive a high weight, signaling that they are highly relevant to that specific document.

When the user submits a query, the query itself is transformed into a TF-IDF vector. The backend then calculates the Cosine Similarity—which is the cosine of the angle between the query vector and each document vector in our multi-dimensional space. A cosine value closer to 1 means the document is highly relevant. The results you see on the screen right now are dynamically sorted in descending order based on this exact mathematical similarity score."

---

## 4. Task 2: Natural Language Processing Pipeline (5:30 - 7:00)
**[Visuals: Transition to the Document Clustering (Task 2) UI on the frontend. Show VS Code with `app.py` focused on the NLP `preprocess()` function.]**

**Speaker:**
"Moving on to Task 2: Document Clustering. For this task, the goal is to automatically organize a large dataset of unlabelled news articles into distinct, logical categories. 

Before any Machine Learning can occur, the text must be cleaned. Here in the code, you can see my preprocessing pipeline. Raw news articles are incredibly messy. Using the Natural Language Toolkit (NLTK), I pass the text through several stages:
1. First, converting everything to lowercase and stripping out non-alphanumeric characters using regular expressions.
2. Second, tokenizing the text into individual words.
3. Third, filtering out common English stop-words that carry no semantic meaning, like 'the', 'is', or 'and'. I also added domain-specific stop-words to this list to improve accuracy.
4. Finally, applying stemming to reduce words to their root form—for example, reducing 'running' and 'runner' to 'run'.

This rigorous preprocessing drastically reduces the dimensionality of our data and eliminates noise, which is critical for the clustering algorithm's performance."

---

## 5. Task 2: Unsupervised K-Means Clustering (7:00 - 8:30)
**[Visuals: Show the Task 2 frontend interface where the user triggers or views the clustering results. Then open VS Code and show the `rss_collector.py` file (specifically the `train_kmeans()` function showing `TfidfVectorizer` and `KMeans`), before returning to the frontend graphs.]**

**Speaker:**
"Once the text is cleaned, it is converted into a numerical matrix using scikit-learn's `TfidfVectorizer`. 

For the actual clustering, I implemented the K-Means algorithm, which is an unsupervised Machine Learning model. Because the assignment specifies three categories—Health, Business, and Sports—I initialized the model with K equals 3. 

The algorithm randomly places three centroids in the vector space and iteratively assigns each news article to the nearest centroid, recalculating the centroid's position until the model converges. 

Looking at the frontend results, we can see how the model has grouped the articles. Despite having no prior labels or training data, the algorithm successfully identifies the latent semantic relationships between the documents. Articles discussing stocks and markets cluster together into the Business group, while articles about fitness and hospitals cluster into the Health group. The accuracy of these clusters demonstrates the effectiveness of the TF-IDF vectorization combined with K-Means."

---

## 6. Code Quality & Conclusion (8:30 - 10:00)
**[Visuals: Briefly scroll through `rss_collector.py` and `app.py` in VS Code, showing important code too (such as the K-Means clustering and TF-IDF logic), highlighting the modular functions and comments. Then return to the React Frontend homepage for the final sign-off.]**

**Speaker:**
"Throughout this project, I placed a strong emphasis on software engineering best practices. The backend Python code is highly modular, with distinct scripts for scraping, indexing, and serving the API. Error handling is implemented to gracefully manage network failures during scraping, and environmental variables are strictly used to protect database credentials. 

The React frontend was built with reusable components, ensuring the codebase remains maintainable and scalable if we were to add more features in the future.

To summarize, this application successfully integrates advanced web crawling, mathematical Information Retrieval models, and Machine Learning clustering into a single, cohesive, full-stack product. It meets all the rigorous requirements set forth in the ST7071CEM assignment.

Thank you very much for your time and for watching my demonstration."
