import streamlit as st
import tmdb_service as tmdb
import movies as movie_util

def render_hero(movie):
    """Native hero banner using st.image and text components (ISSUE 8)."""
    backdrop_url = tmdb.get_image_url(movie.get("backdrop_path"), size="original")
    
    st.image(backdrop_url, use_container_width=True)
    st.title(movie.get("title"))
    st.write(movie.get("overview"))
    
    if st.button("▶ Watch Details", key="hero_details_btn", type="primary"):
        st.session_state.selected_movie_id = movie.get("id")
        st.session_state.page = "details"
        st.rerun()
    st.markdown("---")

def render_home():
    """Main home view."""
    trending = tmdb.get_trending_daily(limit=16)
    if trending:
        render_hero(trending[0])
        st.markdown("### Trending :orange[Today]")
        movie_util.render_movie_grid(trending[1:6], key_prefix="home_trend")
        
        st.markdown("### Top :orange[Rated]")
        top = tmdb.get_top_rated_movies(limit=5)
        movie_util.render_movie_grid(top, key_prefix="home_top")
