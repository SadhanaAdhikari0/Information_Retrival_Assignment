# FINAL MASTER IMPLEMENTATION PROMPT
## Coventry University — Information Retrieval Coursework
### Task 1: Vertical Search Engine
### Task 2: Document Clustering
### Complete Full-Stack Implementation + Evidence + Academic Documentation

---

# ROLE

Act simultaneously as:

- Senior Information Retrieval Engineer
- Python/Flask Backend Engineer
- React Frontend Engineer
- MongoDB Database Engineer
- Web Crawler Engineer
- Machine Learning Engineer
- Data Scientist
- UI/UX Engineer
- Software Testing Engineer
- Technical Writer
- APA 7 Academic Documentation Specialist
- University Coursework Quality Assessor

The objective is to produce a **complete, executable, tested, evidence-backed and professionally documented Information Retrieval coursework project**.

The final submission must contain:

1. Complete Task 1 source code
2. Complete Task 2 source code
3. Backend
4. Frontend
5. MongoDB integration
6. Web crawler
7. Three-month scheduler
8. Vector Space Model
9. TF-IDF
10. Cosine similarity
11. Top-k retrieval
12. Pagination
13. K-Means clustering
14. Dataset of at least 450 documents
15. User document classification
16. Prediction database storage
17. Visualisations
18. Testing
19. Screenshots
20. Conceptual diagrams
21. Architecture diagrams
22. Code screenshots
23. Required tables
24. Evaluation
25. APA 7 citations
26. Hyperlinked references
27. Complete `.docx`
28. README
29. Requirement traceability matrix
30. Final quality audit

Do not produce a superficial prototype.

---

# 1. FIRST STEP — INSPECT ALL PROVIDED DOCUMENTS

Before implementing anything, locate and inspect every coursework-related file available in the workspace.

Mandatory files to inspect if supplied:

```text
IR_Assignment.pdf
210337_Prabisha_Final_Sample.pdf
210337_Prabisha.pdf
Pasted markdown files
Coursework specification
Marking rubric
Any additional supporting files
```

Use PDF/text extraction where necessary.

Do not begin implementation until the requirements have been extracted.

Create an internal requirements matrix:

| Requirement ID | Source Document | Page/Section | Requirement | Implementation Needed | Evidence Needed |
|---|---|---|---|---|---|

Every requirement from the official coursework must be preserved.

---

# 2. SAMPLE DOCUMENT ANALYSIS

Analyse the supplied sample documentation carefully.

Identify:

- document structure
- section ordering
- methodology presentation
- diagrams
- tables
- screenshots
- code evidence
- testing
- evaluation
- references
- formatting
- academic writing style
- appendices
- evidence presentation.

Do NOT copy the sample.

Use it only as a quality and structural reference.

Create an internal gap analysis:

| Sample Requirement/Feature | Present in Sample? | Required by Coursework? | Included in Final? | Reason |
|---|---|---|---|---|

Any important coursework requirement missing from the initial implementation must be added.

---

# 3. IMPORTANT — CURRENT SEED PAGE

Task 1 must use this exact seed URL:

```text
https://pureportal.coventry.ac.uk/en/organisations/centre-for-healthcare-and-community-transformation/
```

The current Coventry Pure page contains dedicated:

- Research Output
- Profiles

sections and exposes pagination/view-all functionality for these resources. The crawler must therefore be designed specifically around this structure.

Do not replace the seed URL with another organisation.

---

# 4. CORE PROJECT STRUCTURE

Create:

```text
IR_COURSEWORK/
│
├── README.md
│
├── .gitignore
├── .env.example
│
├── task1_vertical_search/
│   │
│   ├── backend/
│   │   ├── app/
│   │   ├── config/
│   │   ├── crawler/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── ranking/
│   │   ├── scheduler/
│   │   ├── utils/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── run.py
│   │
│   ├── frontend/
│   │   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── styles/
│   │   └── ...
│   │
│   ├── scripts/
│   └── README.md
│
├── task2_document_clustering/
│   │
│   ├── backend/
│   │   ├── app/
│   │   ├── config/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── preprocessing/
│   │   ├── clustering/
│   │   ├── services/
│   │   ├── visualization/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── run.py
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
│   ├── diagrams/
│   ├── screenshots/
│   ├── code_screenshots/
│   ├── charts/
│   └── final_documentation.docx
│
└── tests/
```

The exact structure may be improved if technically justified.

---

# 5. TECHNOLOGY STACK

Use:

### Backend

- Python
- Flask
- REST API
- MongoDB
- BeautifulSoup/Scrapy/Requests or appropriate crawler libraries
- scikit-learn
- NumPy
- pandas
- APScheduler or an equivalent scheduler

### Frontend

Prefer:

- React
- TypeScript
- Vite
- Tailwind CSS or equivalent professional styling.

The technology stack must remain understandable and appropriate for an Information Retrieval coursework project.

---

# TASK 1
# VERTICAL SEARCH ENGINE

---

# 6. TASK 1 OBJECTIVE

Develop a vertical search engine specialised in the research outputs associated with:

```text
Centre for Healthcare and Community Transformation
Coventry University
```

The system must retrieve relevant research outputs and provide author/profile navigation.

The search engine must implement genuine Information Retrieval techniques rather than relying solely on database text matching.

---

# 7. CRAWLING SCOPE

The seed URL is:

```text
https://pureportal.coventry.ac.uk/en/organisations/centre-for-healthcare-and-community-transformation/
```

The crawler must focus ONLY on:

```text
Research Output
Profiles
```

Do NOT crawl unrelated:

- Projects
- Activities
- Prizes
- Student theses
- Press/media
- News
- Events
- unrelated university departments.

The crawler should follow:

```text
Seed organisation
       ↓
Research Output links
       ↓
Individual research output pages

Seed organisation
       ↓
Profile links
       ↓
Individual Coventry academic profiles
```

---

# 8. CRAWLER REQUIREMENTS

Implement:

- HTTP fetching
- timeout handling
- retries
- user-agent
- robots.txt consideration
- link extraction
- URL normalisation
- duplicate prevention
- content extraction
- pagination handling
- Research Output filtering
- Profile filtering
- logging
- crawl statistics
- error handling.

The crawler must not endlessly crawl the Coventry website.

---

# 9. RESEARCH OUTPUT DATA

Extract, where available:

```text
title
authors
author_profile_urls
publication_date
publication_type
journal/book/conference information
abstract/description
full searchable text
research_output_url
source_url
crawl_timestamp
```

The system must preserve the original research-output URL.

---

# 10. PROFILE DATA

For each relevant Coventry profile, store:

```text
name
profile_url
role
department/centre
research interests
profile description
related research outputs
```

The profile URL must be preserved.

Coventry profiles demonstrate that individual pages can identify roles such as Associate Professor or Assistant Professor and contain research-output information, which supports the required profile-link functionality.

---

# 11. THREE-MONTH CRAWL SCHEDULER — ABSOLUTE REQUIREMENT

The crawl schedule MUST be:

```text
EVERY 3 MONTHS
```

NOT:

```text
weekly
daily
monthly
every 7 days
```

This requirement must be visible in both the implementation and documentation.

Use a configurable value such as:

```text
CRAWL_INTERVAL_MONTHS=3
```

Implement an actual scheduler.

For example:

```text
APScheduler
```

or an equivalent production-appropriate scheduling mechanism.

The scheduler must trigger the crawler automatically every three months.

---

# 12. SCHEDULER CODE EVIDENCE

The documentation must contain a readable screenshot/code listing showing:

```text
three-month scheduling implementation
```

The evidence must make it obvious that the interval is three months.

Also show:

- scheduler startup
- scheduled job
- crawler function called by scheduler
- logging.

Do not merely write:

> The crawler runs every three months.

Show the actual implementation.

---

# 13. MONGODB

MongoDB must be the persistent database.

Suggested collections:

```text
research_outputs
profiles
crawl_logs
search_logs
```

Task 1 research-output schema:

| Field | Type | Description |
|---|---|---|
| `_id` | ObjectId | Unique MongoDB identifier |
| `title` | String | Research title |
| `authors` | Array | Author names |
| `author_profiles` | Array | Coventry profile URLs |
| `publication_date` | Date/String | Publication date |
| `publication_type` | String | Article/book/chapter/etc. |
| `description` | String | Description/abstract |
| `content` | String | Searchable text |
| `document_url` | String | Individual research-output URL |
| `source_url` | String | Crawl source |
| `crawl_timestamp` | Date | Crawl time |

Create appropriate indexes.

---

# 14. MONGODB CODE EVIDENCE

The documentation MUST include actual code showing:

```text
MongoDB connection
collection selection
document creation
insert/upsert
duplicate prevention
retrieval
```

The screenshot must be taken from the actual implementation.

---

# 15. VECTOR SPACE MODEL

The search engine MUST use the:

# Vector Space Model

Do not substitute the required model with:

- LLM ranking
- semantic search only
- embeddings only
- BM25 as the primary required ranking mechanism.

Implement:

```text
Documents
   ↓
Preprocessing
   ↓
TF-IDF
   ↓
Document vectors
```

and:

```text
User query
   ↓
Same preprocessing
   ↓
TF-IDF query vector
```

Then calculate:

```text
Cosine Similarity
```

between the query vector and each document vector.

---

# 16. TF-IDF

Explain and implement:

### Term Frequency

```text
TF(t,d)
```

### Inverse Document Frequency

```text
IDF(t) = log(N / df(t))
```

### TF-IDF

```text
TF-IDF(t,d) = TF(t,d) × IDF(t)
```

Use an appropriate scikit-learn implementation or equivalent transparent implementation.

The documentation must explain why TF-IDF is appropriate.

---

# 17. COSINE SIMILARITY

Implement:

```text
cosine_similarity(A,B)
=
(A · B) / (||A|| ||B||)
```

The calculated value must be used for ranking.

Do not create arbitrary similarity scores.

---

# 18. QUERY PROCESSING

The search interface must support queries such as:

```text
Artificial Intelligence
Mental Health
Digital Health
Machine Learning
```

and author names such as:

```text
Adeniyi Fagbamigbe
Gemma Pearce
Sally Abbott
```

The query processor must search the indexed research-output corpus.

---

# 19. AUTHOR SEARCH

When the query is an author's name:

- relevant publications should be returned
- matching authors should influence ranking
- author names must be searchable
- author names should remain clickable.

---

# 20. TOP-K = 10

The system MUST implement:

```text
K = 10
```

The first page displays:

```text
maximum 10 results
```

Results must be ordered:

```text
highest cosine similarity
          ↓
lowest cosine similarity
```

Each result must display the actual calculated similarity.

Example:

```text
Cosine Similarity: 0.8421
```

---

# 21. PAGINATION

If:

```text
total_results > 10
```

implement pagination.

Example:

```text
Page 1 → 1–10
Page 2 → 11–20
Page 3 → 21–30
```

Backend API must support pagination.

Use:

```text
page
limit
```

with:

```text
limit = 10
```

The frontend must include:

- Previous
- Next
- page numbers
- current page
- total results.

---

# 22. SEARCH RESULT REQUIREMENTS

Every result MUST contain:

### Title

Clickable.

Clicking the title must open the corresponding research-output page only.

### Authors

Display author names.

### Coventry profile links

If a Coventry profile URL exists, the corresponding author name must be clickable.

Clicking it must open that author's Coventry profile.

### Publication date

Display the actual publication date.

### Cosine similarity

Display the actual calculated score.

Example:

```text
────────────────────────────────────────
A digital yoga-based intervention...

Authors:
N. Bisal · R. Patel · N. Holliday...

Published:
12 June 2026

Cosine Similarity:
0.8124

[View Research Output]
────────────────────────────────────────
```

---

# 23. TASK 1 FRONTEND

Create a polished research-search interface.

Required:

- search bar
- search button
- search results
- result count
- title links
- author links
- publication dates
- cosine similarity
- pagination
- loading state
- empty state
- error state
- responsive layout.

The interface should be visually comparable to a modern academic search engine.

---

# TASK 1 API

Implement appropriate REST endpoints, for example:

```text
GET /api/search
GET /api/research-output/:id
GET /api/profile/:id
GET /api/crawler/status
POST /api/crawler/run
```

The exact routes may differ.

Document every endpoint.

---

# TASK 1 TESTING

Test:

```text
Crawler starts
Seed page works
Research Output filtering works
Profile filtering works
Individual output extraction works
Profile extraction works
MongoDB insertion works
Duplicate prevention works
Scheduler is configured for 3 months
Search works
Title query works
Author query works
Keyword query works
TF-IDF works
Cosine similarity works
Ranking works
Top 10 works
Pagination works
Research-output hyperlink works
Profile hyperlink works
Invalid query works
Empty result works
API errors handled
```

---

# TASK 1 DOCUMENTATION EVIDENCE

Include actual screenshots of:

1. Seed page
2. Crawler source code
3. Research Output extraction
4. Profile extraction
5. MongoDB connection code
6. MongoDB records
7. Scheduler code
8. Scheduler output/log
9. TF-IDF code
10. Cosine similarity code
11. Ranking code
12. API code
13. Search interface
14. Search result page
15. Pagination
16. Individual research-output page
17. Coventry profile page.

---

# TASK 2
# DOCUMENT CLUSTERING

---

# 24. TASK 2 OBJECTIVE

Develop a document-clustering system for exactly three primary categories:

```text
Economics
Entertainment
Politics
```

---

# 25. DATASET SIZE

Minimum:

```text
Economics       >= 150
Entertainment   >= 150
Politics        >= 150
```

Therefore:

```text
TOTAL >= 450
```

Prefer longer and information-rich documents.

Do not use artificially tiny sentences merely to satisfy the document count.

---

# 26. DATA COLLECTION

Either:

### Option A

Responsible web scraping from an appropriate news source.

OR:

### Option B

A legitimate existing dataset.

OR:

### Option C

A clearly documented self-created dataset if permitted by the coursework.

Do not falsely claim that data was scraped.

If scraping is used:

- respect robots.txt
- use reasonable delays
- identify source
- retain source URL
- record collection date
- avoid unnecessary server load.

---

# 27. DATASET VALIDATION

Before training, automatically verify:

```text
Economics >= 150
Entertainment >= 150
Politics >= 150
```

Generate a dataset report:

| Category | Required | Actual | Status |
|---|---:|---:|---|
| Economics | 150 | Actual | PASS/FAIL |
| Entertainment | 150 | Actual | PASS/FAIL |
| Politics | 150 | Actual | PASS/FAIL |
| Total | 450 | Actual | PASS/FAIL |

Do not continue to final documentation if minimum requirements are not satisfied.

---

# 28. DATASET SCHEMA

Use:

```text
document_id
title
content
category
source
source_url
collection_date
```

Store appropriate data in MongoDB or another justified storage layer while ensuring the required user predictions are stored in MongoDB.

---

# 29. TEXT PREPROCESSING

Implement and document:

```text
Raw document
      ↓
Cleaning
      ↓
Lowercase
      ↓
Tokenisation
      ↓
Punctuation removal
      ↓
Stop-word removal
      ↓
Optional stemming/lemmatisation
      ↓
TF-IDF
```

Explain every stage.

---

# 30. K-MEANS

Use:

```text
K = 3
```

Implement genuine K-Means.

Explain:

1. Initial centroids
2. Distance calculation
3. Assignment
4. Centroid update
5. Iteration
6. Convergence.

Do not merely call the algorithm without explaining its operation.

---

# 31. CLUSTER LABEL MAPPING

K-Means produces numerical cluster IDs.

For example:

```text
Cluster 0
Cluster 1
Cluster 2
```

These do not automatically mean:

```text
Economics
Entertainment
Politics
```

Therefore determine the mapping from the labelled dataset.

For example:

```text
Cluster 0 → Economics
Cluster 1 → Politics
Cluster 2 → Entertainment
```

The actual mapping must be calculated from the trained result.

Document the methodology.

---

# 32. USER CLASSIFICATION

The application must contain an input field allowing a user to enter:

- sentence
- statement
- paragraph
- document.

Example:

```text
The central bank increased interest rates to control inflation.
```

The system must output:

```text
Economics
```

The implementation must:

```text
User input
   ↓
Preprocessing
   ↓
Existing TF-IDF vectoriser
   ↓
Vector
   ↓
Distance to K-Means centroids
   ↓
Nearest cluster
   ↓
Cluster mapping
   ↓
Economics / Entertainment / Politics
```

Do not retrain the model every time the user submits a sentence.

---

# 33. SAVE PREDICTION

Every user classification must be saved to MongoDB.

Example:

```text
{
    input_text,
    predicted_category,
    cluster_id,
    distance,
    timestamp
}
```

The exact schema may be improved.

---

# 34. TASK 2 FRONTEND

Create:

- large document input
- classify button
- clear button
- predicted category
- cluster number
- distance/confidence where meaningful
- history
- timestamp
- loading state
- error handling.

The predicted category must be visually prominent.

---

# 35. CLUSTERING VISUALISATION

Generate an actual graph.

Because TF-IDF is high-dimensional, use:

```text
PCA
```

or:

```text
Truncated SVD
```

to reduce dimensions for visualisation.

Do not claim that dimensionality reduction is the actual clustering algorithm.

The actual clustering remains:

```text
K-Means
```

The visualisation must include:

- title
- x-axis
- y-axis
- legend
- cluster labels
- figure number
- explanation.

---

# 36. TASK 2 EVALUATION

Calculate actual metrics where appropriate:

- inertia
- silhouette score
- cluster distribution
- confusion matrix after label mapping
- accuracy
- precision
- recall
- F1-score

Only report metrics that are methodologically appropriate.

Never invent values.

---

# 37. TASK 2 DOCUMENTATION CODE EVIDENCE

Show actual code screenshots for:

1. Data collection
2. Dataset validation
3. Text preprocessing
4. TF-IDF
5. K-Means training
6. Cluster mapping
7. Prediction
8. MongoDB insertion
9. Visualisation.

---

# 38. TESTING TASK 2

Test:

```text
Dataset contains >=150/category
Dataset preprocessing
K=3
Model training
Cluster creation
Cluster mapping
Economics example
Entertainment example
Politics example
Empty input
Long input
Invalid input
Prediction storage
Visualisation
API response
Frontend response
```

---

# DOCUMENTATION
# FINAL ACADEMIC DOCX

---

# 39. FINAL FILE

Generate:

```text
documentation/final_documentation.docx
```

It must be a professional academic document.

---

# 40. DOCUMENTATION ORDER

The following must appear BEFORE the Introduction:

## Conceptual Diagram 1 — Task 1

```text
Coventry Seed URL
       ↓
Focused Crawler
       ↓
Research Output + Profile Filtering
       ↓
Data Extraction
       ↓
MongoDB
       ↓
Preprocessing
       ↓
TF-IDF
       ↓
Vector Space Model
       ↓
Query Processing
       ↓
Cosine Similarity
       ↓
Ranking
       ↓
Top 10
       ↓
Pagination
       ↓
Web Interface
```

## Conceptual Diagram 2 — Task 2

```text
News/Data Sources
       ↓
Dataset
       ↓
Economics / Entertainment / Politics
       ↓
Preprocessing
       ↓
TF-IDF
       ↓
K-Means K=3
       ↓
Cluster Mapping
       ↓
User Input
       ↓
Nearest Centroid
       ↓
Category
       ↓
MongoDB
```

These must be actual professional diagrams, not ASCII diagrams.

---

# 41. DOCUMENTATION STRUCTURE

Use an appropriate structure including:

## Cover Page

## Conceptual Diagram — Task 1

## Conceptual Diagram — Task 2

## Table of Contents

## List of Figures

## List of Tables

## 1. Introduction

## 2. Background / Literature Review

## 3. Requirements Analysis

## 4. System Architecture

## 5. Task 1 — Vertical Search Engine

### 5.1 Seed URL
### 5.2 Crawler
### 5.3 Link Filtering
### 5.4 Research Output Extraction
### 5.5 Profile Extraction
### 5.6 Database
### 5.7 Scheduler
### 5.8 Text Preprocessing
### 5.9 TF-IDF
### 5.10 Vector Space Model
### 5.11 Cosine Similarity
### 5.12 Query Processing
### 5.13 Ranking
### 5.14 Top-K
### 5.15 Pagination
### 5.16 Frontend
### 5.17 API
### 5.18 Implementation Evidence
### 5.19 Testing
### 5.20 Results

## 6. Task 2 — Document Clustering

### 6.1 Dataset
### 6.2 Data Collection
### 6.3 Dataset Validation
### 6.4 Preprocessing
### 6.5 TF-IDF
### 6.6 K-Means
### 6.7 Cluster Mapping
### 6.8 User Classification
### 6.9 MongoDB
### 6.10 Visualisation
### 6.11 Evaluation
### 6.12 Frontend
### 6.13 API
### 6.14 Implementation Evidence
### 6.15 Testing
### 6.16 Results

## 7. Discussion

## 8. Limitations

## 9. Ethical / Legal / Responsible Data Considerations

## 10. Conclusion

## References

## Appendices

Adjust the structure if the official coursework PDF specifies a different required structure.

---

# 42. ACADEMIC WRITING STYLE

The entire document must use formal academic third-person writing.

DO NOT write:

```text
I developed...
We created...
Our system...
You can search...
I used...
```

Use:

```text
The proposed system...
The implemented crawler...
The application...
The search interface...
The experimental results...
```

Avoid conversational language.

---

# 43. APA 7

Use APA 7 consistently.

Cite academic sources for:

- Information Retrieval
- Vector Space Model
- TF-IDF
- cosine similarity
- K-Means
- clustering
- dimensionality reduction
- web crawling
- machine learning
- MongoDB where appropriate.

Use legitimate scholarly/authoritative sources.

Do not fabricate references.

---

# 44. INLINE CITATIONS

Important academic statements must have inline citations.

Example:

> The Vector Space Model represents documents and queries as vectors in a multidimensional term space (Salton et al., 1975).

Every cited source must appear in the References section.

---

# 45. HYPERLINKED REFERENCES

References must contain working hyperlinks where appropriate.

Do not place random raw URLs throughout the document.

Use proper APA 7 reference formatting.

Verify links.

---

# 46. REQUIRED TABLES

Include appropriate tables such as:

### Table — Technology Stack

| Technology | Purpose |
|---|---|

### Table — Functional Requirements

| ID | Requirement | Implementation |
|---|---|---|

### Table — Task 1 Database Schema

| Field | Type | Purpose |
|---|---|---|

### Table — Task 2 Dataset Distribution

| Category | Required | Actual |
|---|---:|---:|

### Table — API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|

### Table — Testing

| Test ID | Test | Expected | Actual | Result |
|---|---|---|---|---|

### Table — Evaluation

| Metric | Result | Interpretation |
|---|---:|---|

Add every table required by the official coursework/sample.

---

# 47. SCREENSHOT REQUIREMENTS

All screenshots must come from the actual running implementation.

Do NOT create fake screenshots.

Do NOT use placeholders.

Required screenshots should include:

## Task 1

- seed page
- crawler execution
- extracted data
- MongoDB
- scheduler
- scheduler logs
- preprocessing
- TF-IDF
- cosine similarity
- search interface
- search result
- top 10
- pagination
- research output page
- author profile
- API response.

## Task 2

- dataset
- dataset statistics
- preprocessing
- model training
- K-Means
- clustering graph
- user input
- classification result
- MongoDB prediction
- API response.

---

# 48. CODE SCREENSHOT QUALITY

Code screenshots must:

- be readable
- show the filename
- show relevant code
- avoid tiny text
- avoid secrets
- contain figure numbers/captions.

Important code should also be included as properly formatted code listings where appropriate.

---

# 49. FIGURE CAPTIONS

Use:

```text
Figure 1
Conceptual architecture of the vertical search engine.

Figure 2
Conceptual architecture of the document clustering system.
```

and equivalent descriptions.

Do not use unexplained screenshots.

Every important figure should have an accompanying academic explanation.

---

# 50. REQUIREMENT TRACEABILITY MATRIX

Create a final table:

| Requirement | Implementation | Evidence | Documentation Section | Status |
|---|---|---|---|---|

This must include every major requirement.

For example:

```text
3-month crawler
→ scheduler.py
→ Figure X
→ Section 5.7
→ PASS
```

This is mandatory.

---

# 51. SAMPLE GAP ANALYSIS

Before finalising the DOCX, compare:

```text
Official Coursework
        +
Sample Documentation
        +
Implemented System
```

Create an internal checklist ensuring that nothing present in the official requirements has been omitted.

Do not blindly copy sample-specific content that is irrelevant to the current coursework.

---

# 52. APPENDICES

Include appropriate appendices for:

- important source code
- database schema
- API documentation
- extra screenshots
- testing evidence
- dataset statistics
- supplementary graphs
- requirement traceability
- configuration instructions.

---

# 53. README

Create a complete README.

Include:

```text
Project Overview
Requirements
Architecture
Installation
MongoDB Configuration
Environment Variables
Task 1 Setup
Crawler Setup
Scheduler Setup
Task 1 Search
Task 2 Dataset
Task 2 Training
Task 2 Classification
Testing
API
Project Structure
Troubleshooting
```

---

# 54. ENVIRONMENT VARIABLES

Create:

```text
.env.example
```

Never expose real credentials.

Example:

```text
MONGODB_URI=
DATABASE_NAME=
CRAWL_INTERVAL_MONTHS=3
BACKEND_URL=
FRONTEND_URL=
```

---

# 55. NO FABRICATION

Absolutely do not fabricate:

- screenshots
- results
- dataset counts
- crawler counts
- similarity values
- accuracy
- silhouette score
- execution time
- MongoDB records
- test results.

Every numerical result must come from actual execution.

---

# 56. EXECUTE BEFORE DOCUMENTING

The project must be executed before final documentation is written.

Perform:

```text
Install dependencies
        ↓
Configure environment
        ↓
Connect MongoDB
        ↓
Run Task 1 crawler
        ↓
Verify MongoDB
        ↓
Verify scheduler
        ↓
Build search index
        ↓
Run search queries
        ↓
Verify ranking
        ↓
Verify pagination
        ↓
Verify hyperlinks
        ↓
Collect Task 2 dataset
        ↓
Validate >=450 documents
        ↓
Train K-Means
        ↓
Generate graph
        ↓
Test predictions
        ↓
Store predictions
        ↓
Run complete tests
        ↓
Capture screenshots
        ↓
Generate DOCX
        ↓
Inspect DOCX
        ↓
Final audit
```

---

# 57. FINAL QUALITY AUDIT

Before declaring completion, inspect the final project as a strict university marker.

Verify:

## Task 1

- [ ] Correct Coventry seed URL
- [ ] Research Output only
- [ ] Profiles only
- [ ] MongoDB
- [ ] Vector Space Model
- [ ] TF-IDF
- [ ] Cosine similarity
- [ ] Search by title
- [ ] Search by author
- [ ] k=10
- [ ] Pagination
- [ ] Clickable research title
- [ ] Individual research-output navigation
- [ ] Clickable Coventry author profile
- [ ] Publication date
- [ ] Similarity score
- [ ] Automatic crawler
- [ ] Exactly three-month scheduling
- [ ] Crawler code evidence
- [ ] MongoDB code evidence
- [ ] Scheduler code evidence
- [ ] Frontend
- [ ] Backend
- [ ] Testing
- [ ] Results

## Task 2

- [ ] Economics ≥150
- [ ] Entertainment ≥150
- [ ] Politics ≥150
- [ ] Total ≥450
- [ ] Data collection evidence
- [ ] Preprocessing
- [ ] TF-IDF
- [ ] K-Means
- [ ] K=3
- [ ] Cluster mapping
- [ ] User classification
- [ ] Economics output
- [ ] Entertainment output
- [ ] Politics output
- [ ] MongoDB storage
- [ ] Clustering graph
- [ ] Training code
- [ ] Prediction code
- [ ] Testing
- [ ] Evaluation

## Documentation

- [ ] Conceptual diagram Task 1 before Introduction
- [ ] Conceptual diagram Task 2 before Introduction
- [ ] Table of Contents
- [ ] List of Figures
- [ ] List of Tables
- [ ] Introduction
- [ ] Literature/background
- [ ] Requirements
- [ ] Architecture
- [ ] Task 1 methodology
- [ ] Task 1 implementation
- [ ] Task 1 screenshots
- [ ] Task 1 code evidence
- [ ] Task 2 methodology
- [ ] Task 2 implementation
- [ ] Task 2 screenshots
- [ ] Task 2 code evidence
- [ ] Tables
- [ ] Graphs
- [ ] Testing
- [ ] Evaluation
- [ ] Discussion
- [ ] Limitations
- [ ] Ethical considerations
- [ ] Conclusion
- [ ] APA 7
- [ ] Inline citations
- [ ] Hyperlinked references
- [ ] Appendices
- [ ] Requirement traceability matrix
- [ ] No first-person language
- [ ] No placeholders
- [ ] No fabricated results
- [ ] Professional DOCX

---

# 58. FINAL DELIVERABLE STRUCTURE

The completed project must contain:

```text
IR_COURSEWORK/
│
├── task1_vertical_search/
│   ├── backend/
│   ├── frontend/
│   ├── crawler/
│   ├── scheduler/
│   └── tests/
│
├── task2_document_clustering/
│   ├── backend/
│   ├── frontend/
│   ├── dataset/
│   ├── clustering/
│   ├── visualization/
│   └── tests/
│
├── documentation/
│   ├── diagrams/
│   ├── screenshots/
│   ├── code_screenshots/
│   ├── charts/
│   └── final_documentation.docx
│
├── README.md
├── .env.example
└── .gitignore
```

---

# 59. FINAL INSTRUCTION

Do not stop at planning.

Do not provide pseudo-code as a substitute for implementation.

Do not provide fake screenshots.

Do not provide fake data.

Do not provide fabricated evaluation.

Do not claim that a requirement is complete without evidence.

The completed work must demonstrate the complete chain:

```text
COURSEWORK REQUIREMENT
        ↓
IMPLEMENTATION
        ↓
ACTUAL EXECUTION
        ↓
ACTUAL OUTPUT
        ↓
SCREENSHOT / CODE EVIDENCE
        ↓
DOCUMENTATION
        ↓
ACADEMIC CITATION
```

The final `.docx` must be submission-ready.

The final project must be executable.

The final documentation must be academically written, APA 7 compliant, professionally formatted and evidence-based.

The final audit must identify and fix every missing requirement before completion.

**Most importantly: do not assume that the previous prompt captured everything from the supplied coursework PDFs. Actually inspect the PDFs, compare their requirements against this specification, add anything missing, implement it, test it, document it, and only then produce the final submission.**