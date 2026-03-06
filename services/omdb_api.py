import requests
import streamlit as st
import os

try:
    OMDB_API_KEY = st.secrets.get("OMDB_API_KEY")
except Exception:
    OMDB_API_KEY = None

if not OMDB_API_KEY:
    OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def get_omdb_data(imdb_id):
    """Fetch enriched metadata from OMDb."""
    if not imdb_id or not OMDB_API_KEY:
        return None
    
    url = "http://www.omdbapi.com/"
    params = {"i": imdb_id, "apikey": OMDB_API_KEY}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None
