import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

try:
    URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
except Exception:
    URL = os.getenv("SUPABASE_URL")
    KEY = os.getenv("SUPABASE_KEY")

if not URL or not KEY:
    st.error("Supabase configuration missing (URL/KEY).")
    st.stop()

supabase: Client = create_client(URL, KEY)

def sign_up(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return res, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res, None
    except Exception as e:
        return None, str(e)

def get_watchlist(user_id):
    try:
        res = supabase.table("watchlist").select("*").eq("user_id", user_id).execute()
        return res.data, None
    except Exception as e:
        return None, str(e)

def add_to_watchlist(user_id, movie):
    try:
        data = {
            "user_id": user_id,
            "movie_id": movie.get("id"),
            "title": movie.get("title"),
            "poster_path": movie.get("poster_path"),
            "vote_average": movie.get("vote_average")
        }
        res = supabase.table("watchlist").insert(data).execute()
        return res.data, None
    except Exception as e:
        return None, str(e)

def remove_from_watchlist(user_id, movie_id):
    try:
        res = supabase.table("watchlist").delete().eq("user_id", user_id).eq("movie_id", movie_id).execute()
        return res.data, None
    except Exception as e:
        return None, str(e)

def is_in_watchlist(user_id, movie_id):
    try:
        res = supabase.table("watchlist").select("id").eq("user_id", user_id).eq("movie_id", movie_id).execute()
        return len(res.data) > 0
    except Exception:
        return False
