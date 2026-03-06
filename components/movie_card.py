import streamlit as st
from services import tmdb_api as tmdb
from utils import state_manager as state

def render_movie_card(movie, key_prefix="card"):
    """Standardized movie card with single-click navigation (on_click)."""
    poster_url = tmdb.get_image_url(movie.get("poster_path"))
    st.image(poster_url, use_container_width=True)
    
    # PERMANENT: Fixed height title container for symmetric grid alignment
    st.markdown(f"""
        <div class="movie-title-container">
            {movie.get('title')}
        </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"Rating: {movie.get('vote_average', 'N/A')}")
    
    # Single-click navigation via callback
    movie_id = movie.get("id")
    st.button(
        "Details", 
        key=f"{key_prefix}_{movie_id}", 
        use_container_width=True,
        on_click=state.navigate_to,
        args=("details", movie_id)
    )

def render_movie_grid(movies, key_prefix="grid", cols_per_row=5):
    """Refined grid display (5 Columns - Perfect Symmetry)."""
    if not movies: return
    for i in range(0, len(movies), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(movies):
                with col:
                    with st.container(border=True):
                        render_movie_card(movies[i + j], f"{key_prefix}_{i+j}")
