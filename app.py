import streamlit as st
import requests
from PIL import Image
import io
import os

# =============================
# CONFIG
# =============================
API_BASE = "https://netflix-movies-and-tv-shows-clustering.onrender.com" or "http://127.0.0.1:8000"

POSTER_WIDTH = 280
POSTER_HEIGHT = 420

LOCAL_FALLBACK = "assets/no_poster.jpg"
ONLINE_FALLBACK = "https://via.placeholder.com/280x420?text=No+Poster"

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =============================
# HELPERS
# =============================
def api_get(endpoint, params=None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def truncate(text, n=130):
    if not text:
        return "Description not available."
    return text[:n] + "..." if len(text) > n else text


def format_rating(val):
    try:
        return f"{float(val):.1f}/10"
    except Exception:
        return "N/A"


def load_poster(url=None):
    try:
        if url:
            r = requests.get(url, timeout=10)
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
        elif os.path.exists(LOCAL_FALLBACK):
            img = Image.open(LOCAL_FALLBACK).convert("RGB")
        else:
            r = requests.get(ONLINE_FALLBACK, timeout=10)
            img = Image.open(io.BytesIO(r.content)).convert("RGB")

        return img.resize((POSTER_WIDTH, POSTER_HEIGHT))
    except Exception:
        return None

# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.header("Settings")

    top_n = st.slider(
        "Number of recommendations",
        min_value=4,
        max_value=12,
        value=8
    )

    st.subheader("Filters")

    sort_option = st.selectbox(
        "Sort by rating",
        ["None", "High → Low", "Low → High"],
        key="sort_rating"
    )

    if st.button("🧹 Clear Space"):
        st.session_state.clear()
        st.rerun()

    st.divider()

    # -------- Search Movie Details --------
    if st.session_state.get("search"):
        movie_details = api_get(
            "/movie/details",
            {"title": st.session_state["search"]}
        )

        if movie_details:
            st.subheader("🎬 Movie Details")
            st.caption("Based on search input")

            poster = load_poster(movie_details.get("poster_url"))
            if poster:
                st.image(poster, use_column_width=True)

            st.markdown(f"⭐ **Rating:** {format_rating(movie_details.get('vote_average'))}")
            st.markdown(f"⏱ **Runtime:** {movie_details.get('runtime') or 'N/A'}")

            st.markdown("**Overview**")
            st.caption(truncate(movie_details.get("overview"), 220))

            st.markdown("**Cast**")
            st.caption(movie_details.get("cast") or "N/A")

    st.divider()
   
# =============================
# HEADER
# =============================
st.title("🎬 Movie Recommender")
st.divider()

# =============================
# SEARCH
# =============================
query = st.text_input("Search for a movie", key="search")

# =============================
# RESULTS
# =============================
if query.strip():

    recs = api_get("/recommend", {"title": query, "top_n": top_n})

    if not recs:
        st.error("Movie not found.")
        st.stop()

    # -------- Fetch details once --------
    movies = []
    for rec in recs:
        details = api_get("/movie/details", {"title": rec["title"]}) or {}
        movies.append({
            "title": rec["title"],
            "details": details
        })

    # -------- Apply sorting --------
    if sort_option == "High → Low":
        movies.sort(
            key=lambda x: x["details"].get("vote_average") or 0,
            reverse=True
        )
    elif sort_option == "Low → High":
        movies.sort(
            key=lambda x: x["details"].get("vote_average") or 0
        )

    # -------- Render grid --------
    cols = st.columns(4)

    for i, movie in enumerate(movies):
        details = movie["details"]

        with cols[i % 4]:
            with st.container(border=True):

                poster = load_poster(details.get("poster_url"))
                if poster:
                    st.image(poster, use_column_width=True)

                # ---------- Title ----------
                st.markdown(
                    f"""
                    <div style="min-height:44px">
                        <h4 style="margin-bottom:6px">{movie['title']}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ---------- Meta ----------
                rating = format_rating(details.get("vote_average"))
                runtime = details.get("runtime") or "N/A"

                st.markdown(
                    f"<small>⭐ {rating} &nbsp;&nbsp; ⏱ {runtime}</small>",
                    unsafe_allow_html=True
                )

                # ---------- Overview (fixed height) ----------
                st.markdown(
                    f"""
                    <div style="
                        font-size:13px;
                        line-height:1.4;
                        min-height:78px;
                        max-height:78px;
                        overflow:hidden;
                    ">
                        {truncate(details.get('overview'))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ---------- Cast (fixed height) ----------
                cast = details.get("cast")
                cast_text = ", ".join(cast.split(",")[:3]) if cast else "N/A"

                st.markdown(
                    f"""
                    <div style="
                        font-size:12px;
                        min-height:34px;
                        max-height:34px;
                        overflow:hidden;
                    ">
                        <b>Cast:</b> {cast_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )