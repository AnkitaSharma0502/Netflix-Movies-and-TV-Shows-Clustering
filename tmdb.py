import os
import requests
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"
TIMEOUT = 10


@lru_cache(maxsize=500)
def fetch_movie_data(title: str):
    """
    Fetch poster, rating, runtime, overview, cast
    from BOTH movie and tv endpoints.
    """
    if not TMDB_API_KEY:
        return {}

    try:
        # ---------- MOVIE SEARCH ----------
        r = requests.get(
            f"{BASE_URL}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": title},
            timeout=TIMEOUT
        )
        data = r.json()
        if data.get("results"):
            movie_id = data["results"][0]["id"]

            d = requests.get(
                f"{BASE_URL}/movie/{movie_id}",
                params={"api_key": TMDB_API_KEY, "append_to_response": "credits"},
                timeout=TIMEOUT
            ).json()

            return {
                "poster_url": IMG_BASE + d["poster_path"] if d.get("poster_path") else None,
                "vote_average": round(d.get("vote_average", 0), 1) if d.get("vote_average") else None,
                "runtime": f"{d.get('runtime')} min" if d.get("runtime") else None,
                "overview": d.get("overview"),
                "cast": ", ".join(c["name"] for c in d.get("credits", {}).get("cast", [])[:5]),
                
            }

        # ---------- TV SEARCH (FALLBACK) ----------
        r = requests.get(
            f"{BASE_URL}/search/tv",
            params={"api_key": TMDB_API_KEY, "query": title},
            timeout=TIMEOUT
        )
        data = r.json()
        if data.get("results"):
            tv_id = data["results"][0]["id"]

            d = requests.get(
                f"{BASE_URL}/tv/{tv_id}",
                params={"api_key": TMDB_API_KEY, "append_to_response": "credits"},
                timeout=TIMEOUT
            ).json()

            return {
                "poster_url": IMG_BASE + d["poster_path"] if d.get("poster_path") else None,
                "vote_average": round(d.get("vote_average", 0), 1) if d.get("vote_average") else None,
                "runtime": f"{d.get('episode_run_time',[None])[0]} min"
                            if d.get("episode_run_time") else None,
                "overview": d.get("overview"),
                "cast": ", ".join(c["name"] for c in d.get("credits", {}).get("cast", [])[:5]),
                "genres": ", ".join(g["name"] for g in d.get("genres", []))

            }

    except Exception:
        pass

    return {}