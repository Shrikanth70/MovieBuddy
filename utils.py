import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_trending():
    url = f"{BASE_URL}/trending/movie/day?api_key={API_KEY}"
    data = requests.get(url).json()
    return data["results"]

def search_movie(title):
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={title}"
    data = requests.get(url).json()
    return data["results"]

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"
    return requests.get(url).json()

def get_poster(path):
    if path:
        return IMAGE_URL + path
    return None