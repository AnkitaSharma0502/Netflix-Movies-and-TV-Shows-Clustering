# Netflix-Movies-and-TV-Shows-Clustering

## Problem Statement

Netflix has a large and continuously growing catalog of movies and TV shows from different countries, genres, and formats. As the catalog expands, it becomes difficult to manually organize content, identify patterns, and understand how different types of content relate to each other.

The challenge addressed in this project is that Netflix content does **not have predefined labels** that describe natural groupings such as content themes, formats, or regional patterns. Therefore, this problem is best approached using **unsupervised machine learning**, where the goal is to discover hidden structure in the data rather than predict a known outcome.

The objective of this project is to:

* Identify meaningful clusters of Netflix content based on textual information
* Understand differences between mainstream and niche content
* Generate insights that can support recommendation systems, content strategy, and business decision-making

---

## Dataset Overview

The dataset contains metadata for Netflix movies and TV shows till 2019, including:

* Title
* Type (Movie / TV Show)
* Description
* Genres
* Cast and Director
* Country
* Release year
* Date added to Netflix

A large portion of the dataset is **text-based**, making it suitable for Natural Language Processing (NLP)–driven analysis.

---

## Approach Used

### 1. Data Understanding and Cleaning

* Handled missing values at the title level before any transformations
* Differentiated between true missing values and structural NaNs created during unnesting
* Ensured a clean, one-title–one-row dataset for modeling

---

### 2. Exploratory Data Analysis (EDA)

EDA was performed to understand content distribution and trends:

* Movies vs TV shows distribution
* Growth of Netflix content over time
* Country-wise and genre-wise patterns
* Duration patterns for movies and TV shows

These insights confirmed that Netflix content is diverse and imbalanced, making clustering a suitable approach.

---

### 3. Hypothesis Testing

Statistical hypothesis tests were conducted to validate patterns observed during EDA:

* **Welch’s t-test** to compare when Movies and TV Shows are added to Netflix
* **Chi-square test** to analyze the relationship between content type and country

These tests helped establish that meaningful structure exists in the data before applying clustering models.

---

### 4. Feature Engineering and Text Preprocessing

To capture content semantics, a combined text feature was created using:

* Description
* Genres
* Cast
* Director

Text preprocessing steps included:

* Lowercasing
* Contraction expansion
* Punctuation removal
* Stopword removal
* Lemmatization (focused primarily on nouns)

This cleaned text was converted into numerical form using **TF-IDF vectorization**, which highlights words that are important to individual titles while downweighting common terms.

---

### 5. Dimensionality Reduction

TF-IDF creates a high-dimensional sparse feature space. To make clustering efficient and stable:

* **TruncatedSVD with 300 components** was applied
* TruncatedSVD was chosen because it works directly on sparse text data
* The number of components balances semantic richness and computational efficiency

---

### 6. Clustering Models

Multiple unsupervised clustering algorithms were explored:

* **KMeans Clustering** (Final Model)

  * Evaluated using the Silhouette Score
  * Best performance achieved at **K = 4**

* **Hierarchical Clustering**

  * Used as a validation method to understand high-level structure

* **DBSCAN**

  * Tested but rejected due to high-dimensional text data causing most points to be labeled as noise

---

### 7. Cluster Interpretation and Explainability

Clusters were interpreted using:

* Top TF-IDF terms per cluster
* Representative titles
* TF-IDF–weighted word clouds

The final KMeans model identified four meaningful clusters:

1. Mainstream international movies
2. International TV series and docuseries
3. Stand-up comedy specials (niche cluster)
4. Korean and East-Asian TV content (niche cluster)

Uneven cluster sizes reflect Netflix’s real-world catalog distribution.

---

## Business Impact

The clustering results provide practical value by:

* Supporting content-based recommendation systems
* Helping content strategy teams identify saturated and niche categories
* Enabling regional analysis of international content
* Assisting marketing teams in targeting specific audience segments

Overall, the project adds structure and clarity to a complex content catalog.

---

## Future Scope

Possible improvements include:

* Incorporating user interaction data such as watch history or ratings
* Using transformer-based text embeddings for deeper semantic understanding
* Performing time-based clustering to track content evolution
* Integrating clusters directly into recommendation pipelines

---

## Technologies Used

* **Programming Language:** Python
* **Libraries and Tools:**

  * Pandas, NumPy
  * Matplotlib, Seaborn
  * NLTK, SpaCy
  * Scikit-learn
  * WordCloud
* **Machine Learning Techniques:**

  * TF-IDF Vectorization
  * TruncatedSVD
  * KMeans Clustering
  * Hierarchical Clustering
  * DBSCAN
* **Statistical Methods:**

  * Welch’s t-test
  * Chi-square test

---

## Conclusion

This project demonstrates how unsupervised machine learning and NLP techniques can uncover meaningful patterns in large-scale text data. By combining data analysis, statistical validation, and interpretable clustering, the project delivers actionable insights that are relevant for real-world content platforms like Netflix.
