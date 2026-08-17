# MASTER IMPLEMENTATION PROMPT  
## Coventry University — Information Retrieval Coursework  
### Task 1: Vertical Search Engine + Task 2: Document Clustering

Act as a **senior Information Retrieval engineer, full-stack software engineer, data scientist, academic researcher, technical documentation specialist, and university coursework assessor**.

The objective is to implement the complete coursework described below to a **professional, production-quality and academically rigorous standard**, while strictly following every requirement in the official coursework specification and the provided sample documentation.

The implementation must be complete, executable, demonstrable, well documented, and suitable for university submission.

---

# 1. CRITICAL INSTRUCTION — REVIEW ALL PROVIDED MATERIAL FIRST

Before writing any implementation, documentation, or code:

Thoroughly inspect and analyse **every provided coursework/sample file**, including:

1. `IR_Assignment.pdf`
2. `210337_Prabisha_Final_Sample.pdf`
3. `210337_Prabisha.pdf`
4. `210337_Prabisha markdown file`
5. Any additional coursework files, marking criteria, screenshots, instructions, datasets, or supporting documents supplied with this task.

Extract and create an internal requirements checklist from all files.

### Requirement preservation rule

Every requirement appearing in:

- official coursework specification
- coursework PDF
- sample PDF
- sample Markdown
- marking rubric
- implementation requirements
- documentation requirements
- screenshots/examples
- assessment criteria

must be considered.

**Do not omit a requirement simply because it is not repeated in this prompt.**

Where the sample documentation contains useful sections, tables, diagrams, testing approaches, implementation explanations, screenshots, or academic presentation patterns, incorporate the equivalent or improved version.

The sample must be treated as a **structural and quality reference**, not copied verbatim.

Do not plagiarise the sample.

---

# 2. ACADEMIC INTEGRITY

The final work must be original.

Do not copy:

- paragraphs
- explanations
- code
- diagrams
- screenshots
- conclusions
- tables
- wording

from the sample document.

The sample should only be used to understand:

- expected structure
- level of detail
- presentation
- documentation quality
- evidence requirements
- assessment expectations.

All external academic/technical claims must be supported by appropriate scholarly or authoritative references.

Use **APA 7th edition** referencing consistently.

---

# 3. REQUIRED FINAL PROJECT STRUCTURE

Create a complete project containing both tasks.

Use a clean separation between frontend and backend.

Recommended high-level structure:

```text
IR-Coursework/
│
├── README.md
│
├── task1_vertical_search_engine/
│   │
│   ├── backend/
│   │   ├── app/
│   │   ├── crawler/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── ranking/
│   │   ├── database/
│   │   ├── scheduler/
│   │   ├── config/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── ...
│   │
│   ├── frontend/
│   │   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   └── ...
│   │
│   ├── crawler/
│   ├── scripts/
│   └── README.md
│
├── task2_document_clustering/
│   │
│   ├── backend/
│   │   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── preprocessing/
│   │   ├── clustering/
│   │   ├── database/
│   │   ├── tests/
│   │   └── ...
│   │
│   ├── frontend/
│   │   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── dataset/
│   ├── notebooks/
│   ├── scripts/
│   └── README.md
│
├── documentation/
│   ├── figures/
│   ├── screenshots/
│   ├── code-listings/
│   ├── datasets/
│   └── final_documentation.docx
│
└── ...
```

The exact structure may be improved where technically justified, but **both Task 1 and Task 2 must contain clearly identifiable backend and frontend components**.

---

# 4. TECHNOLOGY REQUIREMENTS

Select a technically appropriate technology stack that supports the coursework requirements.

The implementation should preferably use:

### Backend

- Python
- Flask or an equally appropriate Python web framework
- REST API architecture
- MongoDB
- appropriate Python information-retrieval/data-science libraries

### Frontend

Use a modern, professional web interface.

A suitable implementation may use:

- React
- TypeScript/JavaScript
- CSS/Tailwind or another appropriate styling system

However, do not introduce unnecessary technologies simply for appearance.

The final system must be:

- executable
- maintainable
- modular
- documented
- responsive
- easy to demonstrate.

---

# 5. TASK 1 — VERTICAL SEARCH ENGINE

## 5.1 Seed URL

The crawler must start from:

```text
https://pureportal.coventry.ac.uk/en/organisations/centre-for-healthcare-and-community-transformation/
```

The vertical search engine must focus exclusively on relevant content belonging to the specified Coventry University Centre.

---

# 6. CRAWLING REQUIREMENTS

Implement a proper crawler.

The crawler must:

1. Start from the supplied seed URL.
2. Retrieve the page.
3. Identify relevant links.
4. Follow **Research Output** links.
5. Follow relevant **Profiles** links.
6. Extract the required metadata/content.
7. Store the crawled information in MongoDB.
8. Avoid irrelevant sections/pages.
9. Avoid duplicate records.
10. Maintain crawl metadata.
11. Respect robots.txt and reasonable HTTP behaviour.
12. Handle HTTP failures gracefully.
13. Handle malformed pages gracefully.
14. Log crawling activity.

### IMPORTANT CRAWLING SCOPE

The crawler must focus **only on**:

```text
Research Output
Profiles
```

Do not unnecessarily crawl unrelated:

- news
- events
- teaching
- vacancies
- administrative pages
- unrelated university content
- unrelated departments.

The implementation must clearly demonstrate how the crawler identifies and follows the required link types.

---

# 7. THREE-MONTH CRAWL SCHEDULE — CRITICAL

The coursework requirement is:

> Crawl delay time: **3 months**

This means the automatic crawler must run **once every three months**.

It must NOT be implemented as:

- once per day
- once per week
- once per month
- every 7 days.

Do not interpret this requirement as a weekly crawl delay.

Implement a proper scheduler equivalent to:

```text
Every 3 months
```

For example, use an appropriate scheduling mechanism such as:

- APScheduler
- cron-compatible scheduling
- a persistent scheduled job
- another reliable scheduling mechanism.

The scheduler must be configurable.

Include configuration such as:

```text
CRAWL_INTERVAL_MONTHS=3
```

The documentation must explicitly explain that the automatic crawl occurs every three months.

---

# 8. CRAWLER IMPLEMENTATION EVIDENCE

The documentation MUST include actual code screenshots showing:

### A. Crawler implementation

Show the code responsible for:

- starting from the seed URL
- fetching pages
- extracting links
- identifying Research Output links
- identifying Profile links
- extracting data
- preventing duplicates
- handling errors.

### B. Automatic crawling

Show the exact code that triggers crawling automatically.

### C. Three-month scheduler

Show the exact scheduling implementation demonstrating the three-month interval.

### D. Database storage

Show the exact code responsible for saving crawled records into MongoDB.

Do not merely describe these features.

**Actual source-code evidence must be included.**

---

# 9. TASK 1 DATABASE DESIGN

Use MongoDB.

Design an appropriate collection for research outputs.

The database should store useful fields such as:

```text
_id
title
authors
author_profiles
publication_date
document_url
profile_urls
document_type
description/abstract
content
source_url
category
crawl_timestamp
last_updated
searchable_text
```

The exact schema can be improved where necessary.

Create appropriate indexes where beneficial.

For example:

- title
- authors
- publication date
- searchable content
- URL
- unique identifiers.

Explain the database design academically.

Include a database schema/table describing:

| Field | Data Type | Description | Purpose |
|---|---|---|---|

---

# 10. VECTOR SPACE MODEL

The search engine MUST use the **Vector Space Model** for ranking.

Do not replace the required ranking model with:

- neural embeddings only
- LLM ranking
- Elasticsearch ranking
- BM25 as the primary required ranking method.

The implementation must explicitly demonstrate Vector Space Modeling.

Use an appropriate TF-IDF representation.

The process should include:

```text
Documents
      ↓
Text preprocessing
      ↓
Tokenisation
      ↓
Stop-word removal
      ↓
Normalisation/stemming or lemmatisation
      ↓
TF-IDF
      ↓
Document vectors
      ↓
Query vector
      ↓
Cosine similarity
      ↓
Ranking
      ↓
Top-k results
```

Explain the mathematical basis of:

### TF-IDF

Include appropriate equations.

### Cosine Similarity

Include:

```text
cosine similarity =
(A · B) / (||A|| ||B||)
```

Explain what the value means.

---

# 11. SEARCH FUNCTIONALITY

The search system must support queries including:

- research book names
- research output titles
- author names
- professor names
- relevant keywords.

Example:

```text
Query:
Machine Learning

Query:
John Smith

Query:
Artificial Intelligence
```

The search engine should search the indexed research outputs and return the most relevant documents.

---

# 12. TOP-K REQUIREMENT

The required value is:

```text
k = 10
```

Therefore:

- display up to 10 most relevant documents per result page.
- rank documents using cosine similarity.
- display the cosine similarity score.
- sort results from highest similarity to lowest similarity.

Example:

```text
1. Research Title A
   Authors: ...
   Published: ...
   Cosine Similarity: 0.8421

2. Research Title B
   Authors: ...
   Published: ...
   Cosine Similarity: 0.7914
```

Do not fabricate similarity scores.

Scores must be calculated by the actual ranking algorithm.

---

# 13. PAGINATION

If more than 10 documents match a query:

```text
Page 1 → Results 1–10
Page 2 → Results 11–20
Page 3 → Results 21–30
...
```

The system must support pagination.

Pagination must not simply hide results on the frontend.

The backend API should correctly support pagination parameters such as:

```text
page
limit
```

with:

```text
limit = 10
```

The frontend should provide:

- Previous
- Next
- page numbers where appropriate
- total results
- current page.

---

# 14. TASK 1 SEARCH RESULT REQUIREMENTS

Every result must contain:

### Title

The title must be clickable.

Clicking it must navigate directly to the corresponding research output/document page.

### Author names

Display all relevant author names.

If an author is a Coventry University professor/academic profile:

- the name must be clickable
- clicking the name must navigate to the author's Coventry University profile.

### Publication date

Display the publication date.

### Cosine similarity

Display the actual cosine similarity value.

Example:

```text
Cosine Similarity: 0.8234
```

The interface should clearly communicate that this is the ranking score.

---

# 15. TASK 1 FRONTEND

Create a professional search-engine interface.

The interface should include:

- Coventry-focused branding
- search bar
- search button
- search suggestions if appropriate
- result count
- ranked result cards
- title links
- author links
- publication date
- cosine similarity
- pagination
- loading state
- empty-result state
- error state
- responsive design.

The UI should be modern but academically appropriate.

Avoid unnecessary visual complexity.

---

# 16. TASK 1 REQUIRED OUTPUTS

The final working application must demonstrate:

1. Seed page crawling.
2. Research Output extraction.
3. Profile extraction.
4. MongoDB storage.
5. Automatic three-month scheduler.
6. TF-IDF processing.
7. Vector Space Model.
8. Query processing.
9. Cosine similarity.
10. Ranking.
11. Top-10 retrieval.
12. Pagination.
13. Clickable research output titles.
14. Clickable Coventry academic profiles.
15. Publication dates.
16. Similarity scores.

---

# 17. TASK 2 — DOCUMENT CLUSTERING

Implement a complete document clustering system using **K-Means clustering**.

The required categories are:

```text
Economics
Entertainment
Politics
```

---

# 18. TASK 2 DATASET REQUIREMENT

There must be at least:

```text
150 Economics documents
150 Entertainment documents
150 Politics documents
```

Therefore, the minimum dataset size is:

```text
450 documents
```

Prefer longer and information-rich documents rather than extremely short articles.

The dataset may be collected through legitimate web scraping from a suitable news source or constructed using an appropriate dataset.

If web scraping is used:

- clearly identify the source.
- implement responsible scraping.
- respect robots.txt and site policies.
- avoid excessive request rates.
- retain source URLs where appropriate.
- store collection metadata.

Do not invent that data was scraped if it was not actually scraped.

---

# 19. TASK 2 DATASET STRUCTURE

Each document should contain fields such as:

```text
document_id
title
content
category
source
source_url
date
```

Example:

```text
{
    "document_id": "...",
    "title": "...",
    "content": "...",
    "category": "Economics",
    "source": "...",
    "source_url": "...",
    "date": "..."
}
```

Store the dataset appropriately.

---

# 20. TASK 2 TEXT PREPROCESSING

Implement appropriate preprocessing.

The pipeline should include, where justified:

```text
Raw document
      ↓
Lowercasing
      ↓
Cleaning
      ↓
Tokenisation
      ↓
Stop-word removal
      ↓
Punctuation removal
      ↓
Optional stemming/lemmatisation
      ↓
TF-IDF representation
      ↓
K-Means clustering
```

Explain every preprocessing stage.

Do not remove useful information blindly.

---

# 21. K-MEANS CLUSTERING

Use:

```text
K = 3
```

because there are three required categories.

The algorithm must cluster the documents into three groups.

Explain:

- centroid initialisation
- distance calculation
- assignment step
- centroid update
- iterative optimisation
- convergence.

The implementation must use actual K-Means.

---

# 22. CLUSTER-TO-CATEGORY LABELING

K-Means cluster numbers such as:

```text
Cluster 0
Cluster 1
Cluster 2
```

do not inherently mean:

```text
Economics
Entertainment
Politics
```

Therefore, implement a scientifically valid cluster-label mapping.

Use the known category labels in the dataset to determine the dominant category associated with each cluster.

For example:

```text
Cluster 0 → Economics
Cluster 1 → Entertainment
Cluster 2 → Politics
```

The actual mapping must be calculated from the resulting clustering rather than hard-coded without evidence.

Explain this methodology in the documentation.

---

# 23. USER DOCUMENT CLASSIFICATION

The application must allow a user to enter:

- a sentence
- a statement
- a paragraph
- a document.

The system must predict one of:

```text
Economics
Entertainment
Politics
```

The input must be:

1. preprocessed
2. transformed into the same TF-IDF feature space
3. compared with the trained K-Means centroids
4. assigned to the nearest cluster
5. mapped to the corresponding category.

---

# 24. SAVE USER PREDICTION TO DATABASE

Every classification request must be stored in MongoDB.

Store information such as:

```text
_id
input_text
predicted_category
cluster_id
timestamp
confidence/distance if implemented
```

The documentation must show the actual database insertion code.

---

# 25. TASK 2 FRONTEND

Create a professional interface containing:

- document/sentence input area
- classify button
- predicted category
- cluster information
- relevant score/distance if implemented
- classification history
- clear/reset functionality
- loading state
- error handling.

The result should be visually obvious.

Example:

```text
Input:
The central bank has changed interest rates...

Prediction:
ECONOMICS

Cluster:
Cluster 1
```

---

# 26. TASK 2 VISUALISATION

The documentation MUST contain clustering visualisations.

Produce a meaningful two-dimensional visualisation of the clustered documents.

Because TF-IDF normally produces high-dimensional vectors, use an appropriate dimensionality reduction technique such as:

- PCA
- Truncated SVD

for visualisation.

Do not claim that the original high-dimensional data itself is two-dimensional.

The visualisation must clearly distinguish the three clusters.

Include:

- axis labels
- figure title
- legend
- appropriate caption
- explanation.

If category ground truth is also visualised, clearly distinguish:

```text
K-Means cluster assignment
```

from:

```text
original category label
```

---

# 27. TASK 2 REQUIRED CODE EVIDENCE

The documentation must show actual screenshots/listings of:

### Dataset acquisition

Show the code responsible for:

- scraping or dataset construction
- collecting Economics documents
- collecting Entertainment documents
- collecting Politics documents
- validating document counts.

### Preprocessing

Show the code responsible for:

- cleaning
- tokenisation
- stop-word handling
- TF-IDF.

### Model training

Show the exact K-Means training code.

### Cluster labelling

Show how cluster IDs are mapped to:

- Economics
- Entertainment
- Politics.

### Prediction

Show the code responsible for classifying a new user document.

### Database

Show the code responsible for saving the prediction.

### Visualisation

Show the code generating the clustering graph.

---

# 28. TESTING

Create comprehensive testing for both tasks.

Include:

## Task 1

Test:

- seed URL accessibility
- crawler extraction
- Research Output filtering
- Profile extraction
- duplicate handling
- MongoDB insertion
- scheduler configuration
- search with title
- search with author
- search with keyword
- cosine similarity
- ranking order
- top-10 limitation
- pagination
- broken links
- empty search
- invalid request
- research output link
- profile link.

## Task 2

Test:

- dataset count
- category balance
- preprocessing
- K-Means training
- cluster count
- cluster labelling
- Economics prediction
- Entertainment prediction
- Politics prediction
- empty input
- very long input
- MongoDB storage
- visualisation generation.

Create professional testing tables containing:

| Test ID | Requirement | Test Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|

Only mark a test as passed after actually executing it.

---

# 29. PERFORMANCE / EVALUATION

Where appropriate, calculate and report meaningful evaluation metrics.

For Task 1, report information such as:

- number of documents crawled
- number of profiles found
- number of research outputs indexed
- query processing time where measured
- number of results returned.

For Task 2, report appropriate clustering evaluation such as:

- silhouette score
- inertia
- cluster distribution
- confusion matrix after mapping cluster labels
- accuracy/precision/recall/F1 where the labelled dataset permits meaningful evaluation.

Do not manufacture evaluation values.

All reported values must come from actual execution.

---

# 30. SECURITY AND ROBUSTNESS

Implement reasonable security and reliability practices.

Include:

- input validation
- error handling
- safe database access
- environment variables for credentials
- `.env` support
- no hard-coded passwords
- no exposed database credentials
- API validation
- appropriate logging
- duplicate prevention
- timeout handling.

Do not expose secrets in screenshots or documentation.

---

# 31. DOCUMENTATION — DOCX REQUIREMENT

Create a complete final documentation document:

```text
final_documentation.docx
```

The document must be professionally formatted and suitable for academic submission.

Use **APA 7th edition**.

Use an appropriate academic font and formatting consistent with the coursework/sample requirements, including **Times New Roman** where required by the coursework.

Maintain consistent:

- heading hierarchy
- figure numbering
- table numbering
- captions
- page numbering
- spacing
- margins
- references
- citations.

---

# 32. VERY IMPORTANT DOCUMENT ORDER

Before the Introduction, include the required conceptual diagrams.

The documentation should follow a logical academic structure similar to:

## Cover Page

Include appropriate:

- university information
- module information
- coursework title
- student information
- submission information.

Do not invent personal details that were not provided.

---

## Conceptual Diagram 1 — Task 1

Place the Task 1 conceptual architecture **before the Introduction**.

The diagram should clearly show:

```text
Coventry Seed URL
       ↓
Web Crawler
       ↓
Research Output / Profile Filtering
       ↓
Data Extraction
       ↓
MongoDB
       ↓
Text Preprocessing
       ↓
TF-IDF
       ↓
Vector Space Model
       ↓
Cosine Similarity
       ↓
Ranking
       ↓
Top-10 + Pagination
       ↓
Search Interface
```

Make it modern, visually attractive, clear, and easy to understand.

---

## Conceptual Diagram 2 — Task 2

Also place the Task 2 conceptual architecture **before the Introduction**.

Show:

```text
News/Data Sources
       ↓
Dataset Collection
       ↓
450+ Documents
       ↓
Economics / Entertainment / Politics
       ↓
Text Preprocessing
       ↓
TF-IDF
       ↓
K-Means (K=3)
       ↓
Cluster Identification
       ↓
Cluster-to-Category Mapping
       ↓
User Input
       ↓
Nearest Cluster
       ↓
Category Prediction
       ↓
MongoDB
```

The diagrams must be actual generated figures, not merely text boxes.

---

# 33. RECOMMENDED DOCUMENTATION STRUCTURE

After the conceptual diagrams, structure the documentation logically.

Include, where supported by the official coursework/sample requirements:

### 1. Introduction

Explain:

- Information Retrieval
- Vertical search
- document clustering
- objectives
- scope
- relevance of the implementation.

Do not write in first person.

Avoid:

```text
I developed...
We implemented...
You can...
```

Use academic third-person language such as:

```text
The system implements...
The proposed architecture...
The application provides...
The crawler retrieves...
```

---

### 2. System Requirements

Document:

- functional requirements
- non-functional requirements
- hardware/software requirements
- database requirements
- development environment.

---

### 3. Overall System Architecture

Provide:

- architecture diagram
- component descriptions
- frontend/backend communication
- database communication.

---

### 4. Task 1 — Vertical Search Engine

Include:

#### 4.1 Seed URL

Show and explain the provided Coventry University URL.

#### 4.2 Crawler Architecture

Explain crawler design.

#### 4.3 Link Filtering

Explain why only Research Output and Profile links are followed.

#### 4.4 Web Scraping/Data Extraction

Explain extraction.

#### 4.5 MongoDB Data Model

Include database schema/table.

#### 4.6 Three-Month Scheduler

Explain the automatic three-month schedule.

#### 4.7 Text Preprocessing

Explain preprocessing.

#### 4.8 Vector Space Model

Explain VSM.

#### 4.9 TF-IDF

Provide mathematical explanation.

#### 4.10 Cosine Similarity

Provide formula and explanation.

#### 4.11 Ranking

Explain ranking mechanism.

#### 4.12 Top-K Retrieval

Explain:

```text
k = 10
```

#### 4.13 Pagination

Explain pagination.

#### 4.14 Frontend Interface

Include screenshots.

#### 4.15 Search Results

Include real screenshots showing:

- title
- author
- date
- cosine similarity
- clickable links.

#### 4.16 Code Evidence

Include actual screenshots/listings of critical code.

---

# 34. TASK 2 DOCUMENTATION

Include:

### 5. Task 2 — Document Clustering

#### 5.1 Dataset

Explain:

- sources
- categories
- document counts
- collection method.

#### 5.2 Dataset Statistics

Provide a table:

| Category | Required | Actual | Status |
|---|---:|---:|---|

Minimum:

```text
Economics ≥ 150
Entertainment ≥ 150
Politics ≥ 150
Total ≥ 450
```

#### 5.3 Data Preprocessing

Explain every preprocessing stage.

#### 5.4 TF-IDF Representation

Explain vector representation.

#### 5.5 K-Means

Explain K-Means mathematically and conceptually.

#### 5.6 Cluster Mapping

Explain how numerical clusters become meaningful category labels.

#### 5.7 User Prediction

Explain the prediction pipeline.

#### 5.8 MongoDB Storage

Explain prediction storage.

#### 5.9 Visualisation

Include the actual clustering graph.

#### 5.10 Evaluation

Include actual evaluation metrics.

#### 5.11 Frontend

Include screenshots.

#### 5.12 Code Evidence

Include important code screenshots/listings.

---

# 35. SCREENSHOT REQUIREMENTS

The documentation MUST contain **real screenshots from the implemented system**.

Do not use placeholder screenshots.

Do not use fake UI screenshots.

Do not write:

```text
[Insert screenshot here]
```

and leave it empty.

Capture screenshots after running the actual application.

Include screenshots of:

### Task 1

- homepage
- search interface
- search query
- results
- top 10 results
- pagination
- research output page
- clickable profile
- MongoDB records
- crawler execution
- scheduler
- relevant code
- API response where useful.

### Task 2

- dataset
- training process
- K-Means output
- clustering graph
- user input
- prediction
- database record
- frontend interface
- relevant code
- evaluation output.

Every screenshot should have:

```text
Figure X. Descriptive title.
```

and an academic explanation below/around it where appropriate.

---

# 36. CODE SCREENSHOTS / CODE LISTINGS

Critical code must be included in the documentation.

Do not include every single source file unnecessarily.

Prioritise code demonstrating the assessment requirements.

### Task 1 critical code

Include:

1. crawler
2. link filtering
3. data extraction
4. MongoDB storage
5. scheduler
6. preprocessing
7. TF-IDF
8. cosine similarity
9. ranking
10. top-k
11. pagination
12. API/search endpoint.

### Task 2 critical code

Include:

1. dataset acquisition
2. preprocessing
3. TF-IDF
4. K-Means
5. cluster labelling
6. prediction
7. MongoDB storage
8. visualisation
9. API endpoint.

Code listings should be readable and professionally formatted.

---

# 37. TABLES REQUIRED IN DOCUMENTATION

Include appropriate tables such as:

### Requirements table

| ID | Requirement | Implementation | Evidence |
|---|---|---|---|

### Database schema

| Field | Type | Description |
|---|---|---|

### Dataset distribution

| Category | Number of Documents |
|---|---:|

### Testing

| Test ID | Test | Expected | Actual | Status |
|---|---|---|---|---|

### Technology stack

| Technology | Purpose |
|---|---|

### Functional requirements

| Requirement | Description | Implementation |
|---|---|---|

Add other tables required by the official coursework and sample document.

---

# 38. FIGURE REQUIREMENTS

All important diagrams, graphs and screenshots must be numbered.

For example:

```text
Figure 1. Conceptual architecture of the vertical search engine.
Figure 2. Conceptual architecture of the document clustering system.
Figure 3. Vertical search engine system architecture.
Figure 4. Task 1 search interface.
Figure 5. Task 1 ranked search results.
Figure 6. K-Means clustering visualisation.
...
```

The figure numbering must be consistent throughout the document.

---

# 39. APA 7 CITATIONS

Use proper APA 7 in-text citations.

For example:

```text
Vector Space Models represent documents and queries as vectors in a multidimensional term space (Salton et al., 1975).
```

Do not add unsupported citations.

Use authoritative sources for:

- Information Retrieval
- Vector Space Model
- TF-IDF
- cosine similarity
- K-Means
- clustering
- dimensionality reduction
- web crawling
- MongoDB where appropriate
- relevant machine-learning methods.

---

# 40. REFERENCES SECTION

Create a complete:

# References

section using APA 7.

Every external source cited in the document must appear in References.

Every important reference should contain a working hyperlink where appropriate.

Do not place raw URLs throughout the body.

Use proper APA 7 reference formatting.

Verify that hyperlinks work.

Do not create fake references.

---

# 41. INLINE CITATION REQUIREMENT

Academic claims must contain inline citations.

Avoid a documentation style where sources only appear at the end without being cited in the body.

Example:

```text
K-Means partitions observations into a predefined number of clusters by iteratively assigning observations to centroids and updating centroid positions (MacQueen, 1967).
```

Then provide the complete APA 7 reference with hyperlink in the References section.

---

# 42. NO FIRST-PERSON LANGUAGE

The entire documentation must avoid:

```text
I
We
You
Our
My
```

unless unavoidable inside a quoted external source.

Use academic third-person language.

For example:

❌

```text
We created a crawler.
```

Correct:

```text
A focused web crawler was implemented to retrieve relevant research outputs and academic profiles.
```

❌

```text
You can search for a professor.
```

Correct:

```text
The search interface supports queries containing academic author names.
```

---

# 43. RESULTS MUST BE REAL

This is critical.

Do not fabricate:

- number of crawled pages
- number of research outputs
- number of profiles
- similarity scores
- dataset counts
- clustering scores
- silhouette score
- accuracy
- screenshots
- testing results
- execution times.

All results must come from actual execution.

If an external website changes during implementation, document the actual observed result and explain the situation accurately.

---

# 44. DATA VALIDATION

Before completing the project, automatically verify:

### Task 1

```text
Crawler runs successfully
Research outputs extracted
Profiles extracted
MongoDB populated
Scheduler configured for 3 months
Search works
TF-IDF works
Cosine similarity works
Top 10 works
Pagination works
Links work
```

### Task 2

```text
Economics >= 150
Entertainment >= 150
Politics >= 150
Total >= 450
K-Means K=3
Clusters generated
Clusters mapped
User classification works
MongoDB stores predictions
Visualisation generated
```

If a requirement fails, fix the implementation before producing the final documentation.

---

# 45. README

Create a comprehensive README containing:

- project overview
- Task 1 overview
- Task 2 overview
- architecture
- prerequisites
- installation
- environment variables
- MongoDB configuration
- crawler execution
- scheduler configuration
- frontend execution
- backend execution
- dataset preparation
- model training
- testing
- screenshots
- API endpoints
- project structure
- troubleshooting.

Include commands that actually work.

---

# 46. ENVIRONMENT CONFIGURATION

Create an appropriate `.env.example`.

Never expose real credentials.

Example:

```text
MONGODB_URI=
DATABASE_NAME=
CRAWL_INTERVAL_MONTHS=3
API_BASE_URL=
```

The actual `.env` must not be committed.

---

# 47. API DOCUMENTATION

Document important API endpoints.

For example:

### Task 1

```text
GET /api/search?q=
GET /api/search?q=&page=&limit=
GET /api/research-output/<id>
GET /api/profile/<id>
POST /api/crawler/run
GET /api/crawler/status
```

### Task 2

```text
POST /api/classify
GET /api/classification-history
GET /api/clustering/statistics
```

The exact endpoints may differ based on implementation.

Document:

- HTTP method
- endpoint
- parameters
- request
- response
- purpose.

---

# 48. USER INTERFACE QUALITY

The frontend should look like a genuine modern academic research system rather than a basic student prototype.

Use:

- clean typography
- responsive layout
- accessible controls
- consistent spacing
- clear result hierarchy
- professional cards
- clear navigation
- appropriate icons
- meaningful empty states
- loading indicators
- error messages.

Do not sacrifice functionality for visual design.

---

# 49. ACCESSIBILITY

Where reasonably possible:

- semantic HTML
- labels for inputs
- keyboard accessibility
- readable contrast
- descriptive link text
- responsive design.

---

# 50. CODE QUALITY

Use:

- modular architecture
- functions/classes with clear responsibilities
- meaningful names
- comments only where useful
- error handling
- type hints where appropriate
- configuration separation
- reusable services
- clean API design.

Avoid:

- massive single files
- duplicated code
- hard-coded values
- unnecessary complexity
- unused dependencies.

---

# 51. FINAL QUALITY AUDIT

Before producing the final result, perform a strict assessment-style audit.

Create an internal checklist containing **every requirement from the coursework and every relevant requirement from the sample PDFs**.

For each requirement determine:

```text
Requirement
Implementation
Evidence
Documentation Location
Status
```

No requirement may remain unverified.

Pay particular attention to:

### Task 1

- Correct seed URL
- Research Output only
- Profiles only
- MongoDB
- Vector Space Model
- TF-IDF
- cosine similarity
- k = 10
- pagination
- title hyperlink
- professor/profile hyperlink
- publication date
- similarity score
- automatic crawling
- exactly three-month scheduling
- crawler code
- database code
- scheduler code
- frontend
- backend.

### Task 2

- Economics
- Entertainment
- Politics
- ≥150 documents/category
- ≥450 total
- K-Means
- K=3
- preprocessing
- TF-IDF
- cluster mapping
- user classification
- MongoDB
- clustering graph
- scraping/dataset code
- training code
- prediction code
- frontend
- backend.

### Documentation

- conceptual diagrams before Introduction
- architecture
- methodology
- implementation
- code evidence
- screenshots
- outputs
- tables
- graphs
- testing
- evaluation
- APA 7
- inline citations
- hyperlinks
- references
- academic third-person language
- no fabricated results
- professional DOCX.

---

# 52. FINAL DELIVERABLES

The final submission directory must contain:

```text
1. Complete source code
2. Backend
3. Frontend
4. Task 1 crawler
5. Task 1 scheduler
6. Task 1 MongoDB integration
7. Task 1 VSM ranking
8. Task 1 search interface
9. Task 2 dataset
10. Task 2 preprocessing
11. Task 2 K-Means model
12. Task 2 prediction system
13. Task 2 MongoDB integration
14. Task 2 visualisation
15. Tests
16. README
17. Configuration examples
18. Screenshots
19. Diagrams
20. Final APA 7 DOCX documentation
```

---

# 53. DOCUMENTATION OUTPUT

The final documentation must be generated as:

```text
final_documentation.docx
```

It must be a polished academic document rather than a plain text export.

Ensure:

- headings are properly styled
- automatic table of contents is included
- figures are numbered
- tables are numbered
- captions are consistent
- page numbers are included
- code is readable
- screenshots are high resolution
- references are APA 7
- hyperlinks work
- no broken placeholders remain.

---

# 54. FINAL EXECUTION REQUIREMENT

Do not stop after writing code.

Actually:

1. install dependencies
2. configure the project
3. start MongoDB or connect to the configured MongoDB instance
4. execute the crawler
5. verify stored records
6. verify scheduler configuration
7. build the Task 1 search index
8. execute search queries
9. verify ranking
10. verify pagination
11. verify links
12. collect Task 2 dataset
13. verify ≥150 documents per category
14. train K-Means
15. generate visualisation
16. test classification
17. verify MongoDB predictions
18. run tests
19. capture screenshots
20. generate diagrams
21. generate the final DOCX
22. inspect the final DOCX
23. perform the requirement audit.

---

# 55. IMPORTANT — DO NOT CLAIM COMPLETION WITHOUT EVIDENCE

A feature is considered complete only when:

```text
Code exists
+
Code executes
+
Output is verified
+
Screenshot/evidence is available where required
+
Documentation explains it
```

Do not mark incomplete functionality as complete.

Do not create simulated screenshots when the actual system can be executed.

Do not invent dataset records or evaluation metrics.

---

# 56. FINAL ASSESSMENT-ORIENTED REVIEW

At the very end, perform one final review as if acting as a **Coventry University Information Retrieval coursework marker**.

Ask:

- Is every stated requirement implemented?
- Is every requirement demonstrated?
- Is every major implementation supported by evidence?
- Is the Vector Space Model genuinely used?
- Is cosine similarity genuinely used?
- Is k=10 genuinely implemented?
- Is pagination genuinely implemented?
- Is crawling restricted to Research Output and Profiles?
- Is automatic crawling genuinely scheduled every three months?
- Is MongoDB genuinely used?
- Are there at least 150 documents in each Task 2 category?
- Is K-Means genuinely used?
- Is K=3 used?
- Can an arbitrary user statement be classified?
- Is the classification saved to MongoDB?
- Is the clustering visualised?
- Are code screenshots included?
- Are real system screenshots included?
- Are the conceptual diagrams before the Introduction?
- Are required tables included?
- Are APA 7 citations correct?
- Are references hyperlinked?
- Is the language academic and third-person?
- Are there any missing sections?
- Are there any placeholders?
- Are any results fabricated?
- Does the final DOCX look professionally submitted?

Fix every identified issue before considering the coursework complete.

---

# FINAL INSTRUCTION

**Do not provide a superficial prototype. Build the complete, executable, evidence-backed coursework system and professional documentation.**

The implementation, screenshots, diagrams, outputs, database records, testing results, evaluation metrics, and documentation must all correspond to the actual executed system.

The official coursework files and sample PDFs take precedence wherever they contain additional requirements not explicitly repeated above.

The final result must be sufficiently comprehensive that an academic assessor can trace each major coursework requirement from:

```text
Requirement
     ↓
Implementation
     ↓
Actual Output
     ↓
Screenshot / Code Evidence
     ↓
Documentation
     ↓
Reference / Academic Justification
```

No requirement should be omitted.