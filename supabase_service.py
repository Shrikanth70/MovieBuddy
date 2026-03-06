import streamlit as st
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Configuration
try:
    URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    APP_URL = st.secrets.get("APP_URL") or os.getenv("APP_URL") or "http://localhost:8501"
except Exception:
    URL = os.getenv("SUPABASE_URL")
    KEY = os.getenv("SUPABASE_KEY")
    APP_URL = os.getenv("APP_URL") or "http://localhost:8501"

if not URL or not KEY:
    st.error("Supabase credentials not found. Please check your config.")
    st.stop()

supabase = create_client(URL, KEY)

def sign_up(email, password):
    """Register a new user with email and password and a redirect URL."""
    try:
        response = supabase.auth.sign_up({
            "email": email, 
            "password": password,
            "options": {
                "email_redirect_to": APP_URL
            }
        })
        return response, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    """Authenticate an existing user."""
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response, None
    except Exception as e:
        return None, str(e)

def sign_out():
    """Sign out the current user."""
    try:
        supabase.auth.sign_out()
        return True, None
    except Exception as e:
        return False, str(e)

def get_watchlist(user_id):
    """Fetch all movies in the user's watchlist."""
    try:
        response = supabase.table("watchlist").select("*").eq("user_id", user_id).execute()
        return response.data, None
    except Exception as e:
        return [], str(e)

def add_to_watchlist(user_id, movie):
    """Add a movie to the user's watchlist."""
    try:
        data = {
            "user_id": user_id,
            "movie_id": movie.get("id"),
            "title": movie.get("title"),
            "poster_path": movie.get("poster_path"),
            "vote_average": movie.get("vote_average")
        }
        response = supabase.table("watchlist").insert(data).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def remove_from_watchlist(user_id, movie_id):
    """Remove a movie from the user's watchlist."""
    try:
        response = supabase.table("watchlist").delete().eq("user_id", user_id).eq("movie_id", movie_id).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def is_in_watchlist(user_id, movie_id):
    """Check if a movie is already in the user's watchlist."""
    try:
        response = supabase.table("watchlist").select("id").eq("user_id", user_id).eq("movie_id", movie_id).execute()
        return len(response.data) > 0
    except Exception:
        return False
