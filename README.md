# AI semantic search in the search bar prototype for theinsider.ru
**Model used:** paraphrase-multilingual-mpnet-base-v2
**GitHub Pages:** https://anatolii-serzhantov.github.io/the-insider-search-prototype/ 

Semantic search engine prototype built for a journalistic archive (inspired by *The Insider*). The underlying dataset was programmatically scraped, cleaned, and pre-vectorized into a JSON database, allowing advanced Natural Language Processing (NLP) to run entirely in the browser without requiring a dedicated backend GPU server.

This project focuses on solving the classic limitations of pure vector search by combining neural network semantic embeddings with highly optimized, rule-based heuristics and proportional ranking algorithms.

## Core AI Architecture
The search is powered by **Transformers.js**, running inference completely in the browser via WebAssembly.
* **Model:** `Xenova/paraphrase-multilingual-mpnet-base-v2` (Quantized).
* **Mechanism:** The model maps the user's query to a 768-dimensional dense vector space and calculates the **Cosine Similarity** against pre-computed article vectors.

## ⚙️ Advanced Search Engineering & Optimizations
While LLMs and embedding models are great at capturing the "vibe" or general topic of a text, they often fail at high-precision entity matching (e.g., confusing "1st Service" with "5th Service" due to high semantic overlap). To fix this, I engineered a custom hybrid ranking algorithm:

### 1. Soft Scaling (Proportional) Context Boosting
Instead of using hard cut-offs or blind score boosts (which create a "cliff effect" or falsely promote weak articles), the engine uses proportional boosting. 
For high-priority topics (e.g., queries about politicians), articles in the `/investigations` category receive a dynamic bonus. The bonus is calculated as a percentage of the article's *base semantic score*. A highly relevant article gets a massive boost, while a weak article gets a negligible one, keeping the Top 20 results pure.

### 2. Negative Topic Penalties
To prevent the neural network from returning highly semantically related but factually incorrect results, I implemented a penalty system. If a user explicitly searches for the "5th Service", but the article heavily discusses the "1st Service" and lacks the "5th", the algorithm applies a strict **-40% penalty**, immediately dropping the irrelevant cluster from the top results.

### 3. Anti-False-Positive Regex (Smart Boundaries)
Keyword bonuses are protected by advanced Regular Expressions using Negative Lookbehinds `(?<![\d.,])`. This ensures that when the algorithm searches for a specific number (like the "2nd Service"), it actively ignores decimals (e.g., `3888.2 sq meters`), preventing corrupted relevance scores and false highlighting.

### 4. Dynamic Morphological Expansion
To handle the complexity of the Russian language, the search engine automatically expands numerical and entity queries into morphological synonym groups (e.g., `"5"` expands to `["5", "5-я", "5-й", "пятая", "пятую", "пятой"]`) before evaluating exact match bonuses and extracting snippets.

### 5. Algorithmic Deduplication
To gracefully handle dirty backend data or duplicated URLs in the source datasets, the ranking algorithm utilizes JavaScript `Set` collections during the final sorting phase. It guarantees that the user sees exactly the **Top 20 unique** most relevant articles, silently dropping any backend duplicates.

## ✨ UI/UX Highlights
* **Zero-Latency Search:** After the initial model caching, query inference happens instantly on the client side.
* **Smart Snippet Extraction:** The engine splits articles into sentences, scores each sentence based on query/synonym density, and dynamically extracts the top 3 most relevant sentences. Matches are highlighted using safe Regex replacements.
* **Professional Layout:** A responsive Flexbox-based UI mimicking a high-end news portal, complete with auto-generated category badges, 16:9 image normalization, and real-time **AI Confidence** metrics.

## 🛠 Tech Stack
* **Machine Learning:** `@xenova/transformers` (Client-side NLP inference), `sentence-transformers` (for initial dataset vectorization).
* **Frontend:** Vanilla JavaScript (ES6 Modules), HTML5, CSS3 (Flexbox).
* **Data Engineering (Backend Prep):** Python, `pandas`, `BeautifulSoup` (for ETL pipeline and data merging).

---
### 🚀 The Hybrid Scoring Formula
```javascript
Base Score = Semantic Similarity (Cosine) 
           + Exact Phrase Bonus 
           + Synonym Match Bonus 
           + Target Entity Boost 
           - Negative Topic Penalty

Final AI Confidence = Base Score + (Max(0, Base Score) * Context_Bonus_Multiplier)
