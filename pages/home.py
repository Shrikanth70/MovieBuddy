import streamlit as st
from services import tmdb_api as tmdb
from components import movie_card as mc
from components import carousel

def render_home_page():
    """Main dashboard (Slideshow + Grids)."""
    col_back, _ = st.columns([1.5, 8.5])
    with col_back:
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="/?home=true" target="_self" class="back-pill-btn">
                    <span style="margin-right: 8px;">←</span> BACK
                </a>
            </div>
        ''', unsafe_allow_html=True)
    carousel.render_trending_slideshow()
    
    st.markdown("### Trending Today")
    trending = tmdb.get_trending_daily(limit=11)
    mc.render_movie_grid(trending[1:11], key_prefix="home_trend", cols_per_row=5)
    
    st.markdown("### Top Rated")
    top = tmdb.get_top_rated_movies(limit=5)
    mc.render_movie_grid(top, key_prefix="home_top", cols_per_row=5)
