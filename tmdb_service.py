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
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    sixty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
    params = {
        "sort_by": "popularity.desc",
        "primary_release_date.gte": sixty_days_ago,
        "primary_release_date.lte": today,
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

def get_newly_released_indian_movies(limit=30):
    """Fetch genuine newly released theatrical Indian movies from last 45 days.
    
    Focuses on recent theatrical releases across major Indian languages.
    Uses a narrower time window (45 days vs 90) and lower vote count to catch recent releases.
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    forty_five_days_ago = (datetime.datetime.now() - datetime.timedelta(days=45)).strftime("%Y-%m-%d")
    languages = ["te", "hi", "ta", "kn", "ml"]
    
    all_results = []
    # Fetch movies per language with recent release focus
    for lang in languages:
        params = {
            "with_original_language": lang,
            "region": "IN",  # Focus on Indian region
            "sort_by": "primary_release_date.desc",  # Sort by release date (most recent first)
            "primary_release_date.gte": forty_five_days_ago,
            "primary_release_date.lte": today,
            "vote_count.gte": 3,  # Lower threshold to catch newer films
            "include_adult": False
        }
        data = fetch_from_tmdb("discover/movie", params=params)
        if data and data.get("results"):
            all_results.extend(data["results"])
            
    # Deduplicate by ID and sort by release date (most recent first)
    unique_movies = {m['id']: m for m in all_results}.values()
    sorted_movies = sorted(unique_movies, key=lambda x: x.get('release_date', '0000-00-00'), reverse=True)
    
    return sorted_movies[:limit]

def get_trending_indian(limit=120):
    """Fetch a large pool of trending OTT movies from major Indian regional languages by fetching each separately.
    
    This represents OTT-based content, not theatrical releases.
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    ninety_days_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    languages = ["te", "hi", "ta", "kn", "ml"]
    
    all_results = []
    # Fetch 20 movies per language
    for lang in languages:
        params = {
            "with_original_language": lang,
            "sort_by": "popularity.desc",
            "primary_release_date.gte": ninety_days_ago,
            "primary_release_date.lte": today,
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

def get_trending_tv(limit=20):
    """Fetch trending TV shows and web series."""
    data = fetch_from_tmdb("trending/tv/week")
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_popular_tv(limit=20):
    """Fetch popular TV shows."""
    data = fetch_from_tmdb("tv/popular")
    if data and data.get("results"):
        return data["results"][:limit]
    return []

def get_mixed_shows(limit=30):
    """Fetch a curated mix of trending and newly aired TV shows."""
    all_shows = []
    
    # Focus on newly aired or upcoming TV shows
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    thirty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Get trending TV shows (real-time trending)
    trending = fetch_from_tmdb("trending/tv/week")
    if trending and trending.get("results"):
        for show in trending["results"]:
            show['media_type'] = 'tv'  # Ensure media_type is set
            all_shows.append(show)
    
    # Get recently aired TV shows using discover (last 30 days)
    params = {
        "sort_by": "first_air_date.desc",
        "first_air_date.gte": thirty_days_ago,
        "first_air_date.lte": today,
        "vote_count.gte": 50,  # Ensure watched shows
        "include_adult": False
    }
    recent = fetch_from_tmdb("tv/on_the_air", params=params)
    if recent and recent.get("results"):
        for show in recent["results"]:
            show['media_type'] = 'tv'  # Ensure media_type is set
            all_shows.append(show)
    
    # Deduplicate by ID and sort by first_air_date (newest first)
    unique_shows = {s['id']: s for s in all_shows}.values()
    sorted_shows = sorted(unique_shows, key=lambda x: x.get('first_air_date', '0000-00-00'), reverse=True)
    
    return sorted_shows[:limit]

def get_tv_details(tv_id):
    """Fetch full TV show details including runtime and genres."""
    return fetch_from_tmdb(f"tv/{tv_id}")

def get_tv_videos(tv_id):
    """Fetch TV show videos and filter for YouTube trailers."""
    data = fetch_from_tmdb(f"tv/{tv_id}/videos")
    if data and data.get("results"):
        trailers = [v for v in data["results"] if v.get("site") == "YouTube" and v.get("type") == "Trailer"]
        return trailers
    return []

def get_tv_credits(tv_id):
    """Fetch cast and crew for a TV show. Returns (cast_list, crew_dict)."""
    data = fetch_from_tmdb(f"tv/{tv_id}/credits")
    if not data:
        return [], {"director": "N/A", "writer": "N/A"}
        
    cast = data.get("cast", [])[:12]
    crew = data.get("crew", [])
    
    # Extract Creator and Executive Producer or leading crew role
    creators = [c.get("name") for c in crew if c.get("job") == "Creator"]
    directors = [c.get("name") for c in crew if c.get("department") == "Directing" and c.get("job") == "Director"]
    
    creator_str = ", ".join(list(dict.fromkeys(creators))) if creators else "N/A"
    director_str = ", ".join(list(dict.fromkeys(directors))) if directors else "N/A"
    
    # Prefer creator info for TV shows
    primary = creator_str if creator_str != "N/A" else director_str
    
    return cast, {"director": primary, "writer": "N/A"}

def get_diverse_hero_content(limit=15):
    """Fetch diverse hero content from multiple sources for rich variety."""
    all_content = []
    
    # Trending movies
    trending_m = fetch_from_tmdb("trending/movie/week")
    if trending_m and trending_m.get("results"):
        for movie in trending_m["results"]:
            movie['media_type'] = 'movie'  # Ensure media_type is set
            all_content.append(movie)
    
    # Popular movies
    popular_m = fetch_from_tmdb("movie/popular")
    if popular_m and popular_m.get("results"):
        for movie in popular_m["results"]:
            movie['media_type'] = 'movie'  # Ensure media_type is set
            all_content.append(movie)
    
    # Top-rated movies (broader appeal)
    top_m = fetch_from_tmdb("movie/top_rated")
    if top_m and top_m.get("results"):
        for movie in top_m["results"]:
            movie['media_type'] = 'movie'  # Ensure media_type is set
            all_content.append(movie)
    
    # Trending TV shows for variety
    trending_tv = fetch_from_tmdb("trending/tv/week")
    if trending_tv and trending_tv.get("results"):
        for show in trending_tv["results"]:
            show['media_type'] = 'tv'  # Ensure media_type is set
            all_content.append(show)
    
    # Deduplicate and sort by popularity
    unique_content = {(c.get('id'), c.get('media_type', 'movie')): c for c in all_content}.values()
    sorted_content = sorted(unique_content, key=lambda x: x.get('popularity', 0), reverse=True)
    
    return sorted_content[:limit]

def get_image_url(path, size="w500"):
    """Format full image URL. Returns local placeholder if path is missing."""
    if not path:
        return "placeholder.png"
    return f"https://image.tmdb.org/t/p/{size}/{path}"
