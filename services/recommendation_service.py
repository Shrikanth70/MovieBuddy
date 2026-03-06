import streamlit as st
from services import tmdb_api as tmdb

def get_movie_recommendations(movie_id, limit=10):
    """Multi-stage fallback for better UX."""
    # 1. Recommendations
    data = tmdb.fetch_from_tmdb(f"movie/{movie_id}/recommendations")
    recs = data.get("results", []) if data else []
    
    # 2. Similar
    if not recs:
        data_similar = tmdb.fetch_from_tmdb(f"movie/{movie_id}/similar")
        recs = data_similar.get("results", []) if data_similar else []
        
    # 3. Trending fallback
    if not recs:
        recs = tmdb.get_trending_daily()
        
    return recs[:limit]
