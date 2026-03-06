import streamlit as st
from services import tmdb_api as tmdb
from utils import state_manager as state

def render_movie_card(movie, key_prefix="card"):
    """Standardized movie card with hover-like details button."""
    poster_url = tmdb.get_image_url(movie.get("poster_path"))
    st.image(poster_url, use_container_width=True)
    st.markdown(f"**{movie.get('title')}**")
    st.caption(f"Rating: {movie.get('vote_average', 'N/A')}")
    
    if st.button("Details", key=f"{key_prefix}_{movie.get('id')}", use_container_width=True):
        state.navigate_to("details", movie.get("id"))

def render_movie_grid(movies, key_prefix="grid", cols_per_row=5):
    """Grid display for collections of movies."""
    if not movies: return
    for i in range(0, len(movies), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(movies):
                with col:
                    render_movie_card(movies[i + j], f"{key_prefix}_{i+j}")
