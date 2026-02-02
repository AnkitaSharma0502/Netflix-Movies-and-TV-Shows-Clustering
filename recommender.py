import pickle
import pandas as pd
import difflib
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Load artifacts (ONE pickle)
# -------------------------------
with open("netflix_recommender_artifacts.pkl", "rb") as f:
    artifacts = pickle.load(f)

df_ml = artifacts["df_ml"]
X_embeddings = artifacts["X_embeddings"]
title_to_index = artifacts["title_to_index"]

# -------------------------------
# Title normalization
# -------------------------------
def normalize_title(title: str) -> str:
    if not isinstance(title, str):
        return ""
    return title.lower().strip()

#--------------------------------
# Closest Tittle
#--------------------------------
def get_closest_titles(title, n=5):
    return difflib.get_close_matches(
        title, title_to_index.keys(), n=n, cutoff=0.6
    )


# -------------------------------
# Recommendation function
# -------------------------------
def recommend(title: str, top_n: int = 5) -> pd.DataFrame:
    title = normalize_title(title)

    if title not in title_to_index:
        matches = get_closest_titles(title)
        return pd.DataFrame({
            "error": ["Title not found"],
            "suggestions": [matches]
    })

    idx = title_to_index[title]

    sim_scores = cosine_similarity(
        X_embeddings[idx].reshape(1, -1),
        X_embeddings
    )[0]

    similar_indices = sim_scores.argsort()[::-1][1: top_n + 1]

    results = df_ml.iloc[similar_indices][
        ["title", "listed_in", "rating"]
    ].copy()

    results["similarity_score"] = sim_scores[similar_indices]

    return results.reset_index(drop=True)