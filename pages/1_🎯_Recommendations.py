import streamlit as st
from recommendation import recommend
from utils import search_movie, get_poster

st.set_page_config(page_title="Recommendations", layout="wide")

st.title("🎯 Get Movie Recommendations")

# Load movie titles from ML dataset
import pickle
movies = pickle.load(open("movies.pkl", "rb"))

selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

if st.button("Recommend Similar Movies"):

    recommended_movies = recommend(selected_movie)

    cols = st.columns(3)

    for idx, movie in enumerate(recommended_movies):
        with cols[idx % 3]:

            search_results = search_movie(movie)

            if len(search_results) > 0:
                poster_path = search_results[0]["poster_path"]
                poster = get_poster(poster_path)
                if poster:
                    st.image(poster)

            st.write(movie)