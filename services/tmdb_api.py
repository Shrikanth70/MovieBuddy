import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
try:
    API_KEY = st.secrets.get("TMDB_API_KEY")
except Exception:
    API_KEY = None

if not API_KEY:
    API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"

@st.cache_data(ttl=600)
def fetch_from_tmdb(endpoint, params=None):
    """Generic fetcher for TMDB with caching."""
    if not API_KEY:
        st.error("TMDB API Key missing.")
        return None
    
    url = f"{BASE_URL}/{endpoint}"
    default_params = {"api_key": API_KEY, "language": "en-US"}
    if params:
        default_params.update(params)
    
    try:
        response = requests.get(url, params=default_params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

def get_image_url(path, size="w500"):
    """Format full image URL."""
    if not path:
        return "placeholder.png"
    return f"https://image.tmdb.org/t/p/{size}/{path}"

def get_trending_daily(limit=16):
    data = fetch_from_tmdb("trending/movie/day")
    return data.get("results", [])[:limit] if data else []

def get_trending_weekly(limit=20):
    data = fetch_from_tmdb("trending/movie/week")
    return data.get("results", [])[:limit] if data else []

def get_top_rated_movies(limit=12):
    data = fetch_from_tmdb("movie/top_rated")
    return data.get("results", [])[:limit] if data else []

def get_movie_details(movie_id):
    return fetch_from_tmdb(f"movie/{movie_id}")

def get_movie_videos(movie_id):
    data = fetch_from_tmdb(f"movie/{movie_id}/videos")
    if data:
        return [v for v in data.get("results", []) if v.get("site") == "YouTube" and v.get("type") == "Trailer"]
    return []

def search_movies(query):
    if not query: return []
    data = fetch_from_tmdb("search/movie", params={"query": query})
    return data.get("results", []) if data else []

def get_imdb_id(movie_id):
    data = fetch_from_tmdb(f"movie/{movie_id}/external_ids")
    return data.get("imdb_id") if data else None
