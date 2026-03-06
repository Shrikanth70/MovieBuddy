import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Safe loading of OMDB_API_KEY
try:
    OMDB_API_KEY = st.secrets["OMDB_API_KEY"]
except Exception:
    OMDB_API_KEY = os.getenv("OMDB_API_KEY")

@st.cache_data(ttl=600)
def get_movie_reviews(title):
    """Fetch movie ratings and reviews from OMDb."""
    if not OMDB_API_KEY:
        st.warning("OMDb API Key not found. Please check your .env file or Streamlit secrets.")
        return None
        
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return {
                "imdbRating": data.get("imdbRating"),
                "Metascore": data.get("Metascore"),
                "imdbVotes": data.get("imdbVotes"),
                "Ratings": data.get("Ratings", [])
            }
        return None
    except Exception as e:
        st.error(f"Error fetching from OMDb: {e}")
        return None
