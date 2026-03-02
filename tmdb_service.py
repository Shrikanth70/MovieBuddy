import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"

@st.cache_data(ttl=600)
def fetch_from_tmdb(endpoint, params=None):
    """Generic fetcher for TMDB with caching."""
    if not API_KEY:
        st.error("TMDB API Key not found. Please check your .env file or Streamlit secrets.")
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
        st.error(f"Error fetching from TMDB: {e}")
        return None

def get_popular_movie():
    """Fetch the first popular movie for the hero section."""
    data = fetch_from_tmdb("movie/popular")
    if data and data.get("results"):
        return data["results"][0]
    return None

def get_top_rated_movies(limit=12):
    """Fetch top rated movies for the recommendations section."""
    data = fetch_from_tmdb("movie/top_rated")
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_trending_weekly(limit=5):
    """Fetch weekly trending movies for the sidebar."""
    data = fetch_from_tmdb("trending/movie/week")
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_popular_actors(limit=8):
    """Fetch popular people for the actors section."""
    data = fetch_from_tmdb("person/popular")
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_movie_details(movie_id):
    """Fetch full movie details including runtime and genres."""
    return fetch_from_tmdb(f"movie/{movie_id}")

def get_movie_videos(movie_id):
    """Fetch movie videos and filter for YouTube trailers."""
    data = fetch_from_tmdb(f"movie/{movie_id}/videos")
    if data and data.get("results"):
        trailers = [v for v in data["results"] if v.get("site") == "YouTube" and v.get("type") == "Trailer"]
        return trailers
    return []

def get_movie_recommendations(movie_id, limit=10):
    """Fetch movie recommendations based on a movie ID. Falls back to similar movies if empty."""
    # 1. Try recommendations endpoint
    data = fetch_from_tmdb(f"movie/{movie_id}/recommendations")
    recs = data.get("results", []) if data else []
    
    # 2. If empty, try similar movies endpoint
    if not recs:
        data_similar = fetch_from_tmdb(f"movie/{movie_id}/similar")
        recs = data_similar.get("results", []) if data_similar else []
        
    return recs[:limit]

def search_movies(query):
    """Search movies by title."""
    if not query:
        return []
    data = fetch_from_tmdb("search/movie", params={"query": query})
    if data and data.get("results"):
        return data["results"]
    return []

def get_image_url(path, size="w500"):
    """Format full image URL. Returns local placeholder if path is missing."""
    if not path:
        return "placeholder.png"
    return f"https://image.tmdb.org/t/p/{size}/{path}"
