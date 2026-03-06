import streamlit as st
from services import tmdb_api as tmdb
from components import movie_card as mc

def render_trending_page():
    st.markdown("# Trending This Week")
    weekly = tmdb.get_trending_weekly(limit=20)
    mc.render_movie_grid(weekly, key_prefix="page_trend", cols_per_row=4)
