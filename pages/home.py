import streamlit as st
from services import tmdb_api as tmdb
from components import movie_card as mc
from components import carousel

def render_home_page():
    """Main dashboard (Slideshow + Grids)."""
    carousel.render_trending_slideshow()
    
    st.markdown("### Trending Today")
    trending = tmdb.get_trending_daily(limit=12)
    mc.render_movie_grid(trending[1:9], key_prefix="home_trend", cols_per_row=4)
    
    st.markdown("### Top Rated")
    top = tmdb.get_top_rated_movies(limit=4)
    mc.render_movie_grid(top, key_prefix="home_top", cols_per_row=4)
