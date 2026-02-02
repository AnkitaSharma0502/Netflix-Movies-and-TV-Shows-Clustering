from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pickle
import difflib
from sklearn.metrics.pairwise import cosine_similarity

from tmdb import  fetch_movie_data
app = FastAPI(title="Movie Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Load artifacts
# ----------------------------
with open("netflix_recommender_artifacts.pkl", "rb") as f:
    artifacts = pickle.load(f)

df = artifacts["df_ml"]
X = artifacts["X_embeddings"]
title_to_index = artifacts["title_to_index"]

# ----------------------------
# Helpers
# ----------------------------
def normalize(title: str) -> str:
    return title.lower().strip()

def close_matches(title: str, n=5):
    return difflib.get_close_matches(title, title_to_index.keys(), n=n, cutoff=0.6)

# ----------------------------
# Recommendation
# ----------------------------
def recommend_movies(title: str, top_n: int):
    title = normalize(title)

    if title not in title_to_index:
        raise HTTPException(
            status_code=404,
            detail={"error": "Movie not found", "suggestions": close_matches(title)}
        )

    idx = title_to_index[title]
    scores = cosine_similarity(X[idx].reshape(1, -1), X)[0]
    indices = scores.argsort()[::-1][1: top_n + 1]

    return [{"title": df.iloc[i]["title"]} for i in indices]

# ----------------------------
# Routes
# ----------------------------
@app.get("/recommend")
def recommend(title: str = Query(...), top_n: int = Query(12)):
    return recommend_movies(title, top_n)

from tmdb import fetch_movie_data

@app.get("/movie/details")
def movie_details(title: str):
    data = fetch_movie_data(title)

    return {
        "title": title,
        "poster_url": data.get("poster_url"),
        "vote_average": data.get("vote_average"),
        "runtime": data.get("runtime"),
        "overview": data.get("overview"),
        "cast": data.get("cast"),
    }