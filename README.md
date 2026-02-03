#  Netflix Movies & TV Shows Recommendation System

A **content-based recommendation system** built using **unsupervised machine learning and NLP** techniques to suggest similar Netflix movies and TV shows based on semantic similarity. The project includes end-to-end steps from data preprocessing and clustering to model deployment via APIs and an interactive web interface.

Link: https://netflix-movies-and-tv-shows-clustering-y2i3skyf3y2bxj6ntgxcrh.streamlit.app/
---

## 📌 Problem Statement

Netflix hosts a large and diverse catalog of movies and TV shows without explicit labels defining content similarity. As the catalog grows, discovering meaningful relationships between titles becomes challenging.  
This project addresses the problem using **unsupervised learning** to uncover latent structure in content metadata and generate personalized recommendations.

---

## 📊 Dataset Overview

The dataset contains metadata for Netflix titles up to 2019, including:

- Title  
- Type (Movie / TV Show)  
- Description  
- Genres  
- Cast & Director  
- Country  
- Release Year  
- Date Added  

The dataset is primarily **text-heavy**, making it suitable for NLP-based modeling.

---

## 🔍 Approach

### 1. Data Cleaning & Preparation
- Handled missing and inconsistent values
- Ensured one-title–one-row consistency
- Combined textual attributes into a unified feature set

### 2. Exploratory Data Analysis
- Content distribution by type, country, and genre
- Temporal trends in content addition
- Duration analysis for movies and TV shows

### 3. Statistical Validation
- Welch’s t-test to compare Movies vs TV Shows addition patterns
- Chi-square test to examine content type and country relationships

### 4. Feature Engineering & NLP
- Text preprocessing: lowercasing, punctuation removal, stopword removal, lemmatization
- Vectorization using **TF-IDF**
- Dimensionality reduction with **Truncated SVD** for efficient similarity computation

### 5. Unsupervised Learning
- **KMeans clustering (K = 4)** to identify latent content groups
- Cluster interpretation using top TF-IDF terms and representative titles

### 6. Recommendation Logic
- **Cosine similarity** on reduced embeddings
- Top-N similar titles generated for a given input
- Fuzzy title matching for improved search robustness

---

## ⚙️ System Architecture

The system follows a modular, service-oriented architecture separating model inference, external data enrichment, and presentation logic.

### Architecture Flow

User Input  
→ FastAPI Inference Service  
→ Recommendation Engine (TF-IDF + SVD + Cosine Similarity)  
→ TMDB API (Metadata Enrichment)  
→ Streamlit Frontend  

### Component Description

- **FastAPI Service**  
  Handles incoming requests, performs fuzzy title matching, executes similarity-based inference, and returns ranked recommendations.

- **Recommendation Engine**  
  Uses precomputed TF-IDF embeddings reduced via Truncated SVD, applying cosine similarity to retrieve top-N semantically similar titles.

- **External Metadata Layer (TMDB API)**  
  Enriches recommendations with posters, ratings, runtime, overview, and cast information.

- **Streamlit Frontend**  
  Provides an interactive user interface for search, filtering, sorting, and real-time visualization of recommendations.


---

## 🛠️ Tech Stack

**Programming Language:**  
- Python  

**Libraries & Tools:**  
- Pandas, NumPy  
- Scikit-learn  
- NLTK / SpaCy  
- FastAPI  
- Streamlit  
- Requests  

**Machine Learning Techniques:**  
- TF-IDF Vectorization  
- Truncated SVD  
- KMeans Clustering  
- Cosine Similarity  

---

## 📈 Business Impact

- Enables **content-based recommendation** without user interaction data  
- Identifies mainstream and niche content categories  
- Supports content strategy and catalog analysis  
- Provides a deployable ML inference pipeline

---

## 🔮 Future Enhancements

- Incorporate user interaction signals (ratings, watch history)
- Replace TF-IDF with transformer-based embeddings
- Add caching and scalability optimizations
- Improve recommendation diversity and ranking strategies

---

## ✅ Conclusion

This project demonstrates the application of **unsupervised machine learning and NLP** to solve real-world recommendation problems. By combining data analysis, interpretable modeling, and deployment-ready architecture, the system delivers meaningful insights and practical recommendations for large-scale content platforms.

