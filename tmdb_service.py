import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
# Use Streamlit secrets with fallback to environment variables
try:
    API_KEY = st.secrets["TMDB_API_KEY"]
except Exception:
    API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    st.error("TMDB API Key not found. Please check your Streamlit secrets or .env file.")
    st.stop()

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"

@st.cache_data(ttl=43200)
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

import datetime

def get_now_playing_movies(limit=10):
    """Fetch newly released movies for the hero section."""
    data = fetch_from_tmdb("movie/now_playing", params={"page": 1})
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_trending_weekly(limit=5):
    """Fetch weekly trending movies for the sidebar."""
    data = fetch_from_tmdb("trending/movie/week")
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_trending_by_language(language_code, limit=20):
    """Fetch trending OTT movies by original language."""
    # Date ~90 days ago
    ninety_days_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    
    # Use discover endpoint to filter by language, sort by popularity
    # We require OTT by filtering on monetization type "flatrate" in the discover endpoint usually.
    # TMDB supports `with_watch_monetization_types` natively.
    params = {
        "with_original_language": language_code,
        "sort_by": "popularity.desc",
        "primary_release_date.gte": ninety_days_ago,
        "vote_count.gte": 10,  # Lowered for more diversity in new releases
        "include_adult": False
    }
    data = fetch_from_tmdb("discover/movie", params=params)
    if data and data.get("results"):
        return data["results"][:limit]
    return []
    
def get_new_releases_worldwide(limit=20):
    """Fetch globally released movies without OTT restriction."""
    sixty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
    params = {
        "sort_by": "popularity.desc",
        "primary_release_date.gte": sixty_days_ago,
        "vote_count.gte": 100,
        "include_adult": False
    }
    data = fetch_from_tmdb("discover/movie", params=params)
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_recent_ott_movies(limit=20):
    """Fetch newly arrived OTT movies generically."""
    sixty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
    params = {
        "sort_by": "popularity.desc",
        "primary_release_date.gte": sixty_days_ago,
        "vote_count.gte": 20,
        "with_watch_monetization_types": "flatrate",
        "watch_region": "IN"
    }
    data = fetch_from_tmdb("discover/movie", params=params)
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_other_languages_ott(limit=20):
    """Fetch OTT movies excluding English, Hindi, and Telugu."""
    ninety_days_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    params = {
        "sort_by": "popularity.desc",
        "primary_release_date.gte": ninety_days_ago,
        "vote_count.gte": 50,
        "without_original_language": "en,hi,te",
        "with_watch_monetization_types": "flatrate",
        "watch_region": "IN"
    }
    data = fetch_from_tmdb("discover/movie", params=params)
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

def get_movie_credits(movie_id):
    """Fetch cast and crew for a movie. Returns (cast_list, crew_dict)."""
    data = fetch_from_tmdb(f"movie/{movie_id}/credits")
    if not data:
        return [], {"director": "N/A", "writer": "N/A"}
        
    cast = data.get("cast", [])[:12] # Top 12 actors
    crew = data.get("crew", [])
    
    # Extract Director and Writer
    directors = [c.get("name") for c in crew if c.get("department") == "Directing" and c.get("job") == "Director"]
    writers = [c.get("name") for c in crew if c.get("department") == "Writing" and c.get("job") in ["Screenplay", "Writer", "Story"]]
    
    # Deduplicate and format
    director_str = ", ".join(list(dict.fromkeys(directors))) if directors else "N/A"
    writer_str = ", ".join(list(dict.fromkeys(writers))) if writers else "N/A"
    
    # If same person is both, we handle display logic in the UI component
    return cast, {"director": director_str, "writer": writer_str}

def get_trending_indian(limit=120):
    """Fetch a large pool of trending OTT movies from major Indian regional languages by fetching each separately."""
    ninety_days_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    languages = ["te", "hi", "ta", "kn", "ml"]
    
    all_results = []
    # Fetch 20 movies per language
    for lang in languages:
        params = {
            "with_original_language": lang,
            "sort_by": "popularity.desc",
            "primary_release_date.gte": ninety_days_ago,
            "vote_count.gte": 5,  # Maximum diversity for 'New' content
            "include_adult": False
        }
        data = fetch_from_tmdb("discover/movie", params=params)
        if data and data.get("results"):
            all_results.extend(data["results"])
            
    # Deduplicate by ID and sort by popularity
    unique_movies = {m['id']: m for m in all_results}.values()
    sorted_movies = sorted(unique_movies, key=lambda x: x.get('popularity', 0), reverse=True)
    
    return sorted_movies[:limit]

def get_movie_reviews(movie_id, limit=3):
    """Fetch user reviews for a movie from TMDB."""
    data = fetch_from_tmdb(f"movie/{movie_id}/reviews")
    if data and data.get("results"):
        return data["results"][:limit]
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

def get_watch_providers(movie_id):
    """Fetch watch providers (OTT) for a movie."""
    data = fetch_from_tmdb(f"movie/{movie_id}/watch/providers")
    if data and data.get("results"):
        results = data.get("results", {})
        # Prioritize IN, then US, then any available
        return results.get("IN") or results.get("US") or next(iter(results.values()), None)
    return None

def get_image_url(path, size="w500"):
    """Format full image URL. Returns local placeholder if path is missing."""
    if not path:
        return "placeholder.png"
    return f"https://image.tmdb.org/t/p/{size}/{path}"
