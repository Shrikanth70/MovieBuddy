import streamlit as st
import tmdb_service as tmdb
import components as ui

def render_trending_page():
    st.markdown('<div class="ott-title" style="font-size: 32px; margin-bottom: 20px;">Trending This Week</div>', unsafe_allow_html=True)
    weekly = tmdb.get_trending_weekly(limit=24)
    ui.render_movie_grid(weekly, key_prefix="page_trend", columns=5)

if __name__ == "__main__":
    ui.inject_custom_css()
    render_trending_page()
