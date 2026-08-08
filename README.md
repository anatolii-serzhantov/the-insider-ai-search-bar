# AI semantic search in the search bar theinsider.ru (prototype)

**GitHub Pages:** https://anatolii-serzhantov.github.io/the-insider-search-prototype/

**Objective:** This project aims to improve the search quality on the website by implementing AI-powered semantic search. 
Project focuses on solving limitations of pure vector search by combining neural network semantic embeddings with optimized rule-based heuristics and proportional ranking algorithms.

**Model used:** `Xenova/paraphrase-multilingual-mpnet-base-v2` (quantized). The model maps the user's query to a 768-dimensional dense vector space and calculates the cosine similarity against pre-computed article vectors.

**Data preparation:** The underlying dataset includes 1590 articles from https://theinsider.ru, that were parced, cleaned and pre-vectorized using Python script.

<div align="center"><img src="images/new_project_5_служба_фсб_выдача_гифка.gif" alt="5th_listing"></div>

## Applied search optimization:

### 1. Dynamic morphological expansion
To handle the complexity of the Russian language, the search engine automatically expands numerical and entity queries into morphological synonym groups (e.g., `"5"` expands to `["5", "5-я", "5-й", "пятая", "пятую", "пятой"]`) before evaluating exact match bonuses and extracting snippets.

### 2. Negative topic penalties
To prevent the neural network from returning highly semantically related but factually incorrect results, I implemented a penalty system. If a user explicitly searches for the "5th Service", but the article heavily discusses the "1st Service" and lacks the "5th", the algorithm applies a strict **-40% penalty**, immediately dropping the irrelevant cluster from the top results.

### 3. Anti-false-positive regex
Keyword bonuses are protected by advanced Regular Expressions using Negative Lookbehinds `(?<![\d.,])`. This ensures that when the algorithm searches for a specific number (like the "2nd Service"), it actively ignores decimals (e.g., `3888.2 sq meters`), preventing corrupted relevance scores and false highlighting.

### 4. Proportional context boosting
Instead of using hard cut-offs or blind score boosts (which create a "cliff effect" or falsely promote weak articles), the engine uses proportional boosting. 
For high-priority topics (e.g., queries about politicians), articles in the `/investigations` category receive a dynamic bonus. The bonus is calculated as a percentage of the article's *base semantic score*. A highly relevant article gets a massive boost, while a weak article gets a negligible one, keeping the Top 20 results pure.

<div align="center"><img src="images/new_project_навальный_выдача_гифка.gif" alt="navalny"></div>

### 5. Examples of improving search results
In https://theins.ru/inv/283609 there are 
<div align="center"><img src="images/theinsru_винодельная_реймана_статья.png" alt="reyman_article"></div>

Default theinsider.ru search doesn´t suggest
<div align="center"><img src="images/theinsru_винодельная_реймана_выдача.png" alt="reyman_listing"></div>

### 6. Article snippet extraction:
The engine splits articles into sentences, scores each sentence based on query/synonym density, and dynamically extracts the top 3 most relevant sentences. Matches are highlighted using safe Regex replacements.

## Plans for further improvement of the search engine

## Plans for implementation in the site's backend
