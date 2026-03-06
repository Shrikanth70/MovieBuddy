import streamlit as st
import tmdb_service as tmdb
import components as ui # Keep some legacy helpers for now if needed

def render_movie_grid(movies, key_prefix="grid", cols_per_row=5):
    """Native Streamlit grid for movie cards."""
    if not movies:
        st.info("No movies to display.")
        return
        
    idx = 0
    while idx < len(movies):
        cols = st.columns(cols_per_row)
        for col in cols:
            if idx < len(movies):
                movie = movies[idx]
                poster_url = tmdb.get_image_url(movie.get("poster_path"))
                with col:
                    st.image(poster_url, use_container_width=True)
                    st.markdown(f"**{movie.get('title')}**")
                    st.caption(f"⭐ {movie.get('vote_average', 'N/A')}")
                    if st.button("Details", key=f"{key_prefix}_{movie.get('id')}_{idx}", use_container_width=True):
                        st.session_state.selected_movie_id = movie.get("id")
                        st.session_state.page = "details"
                        st.rerun()
                idx += 1

def render_hero(movie):
    """Native hero banner with background image."""
    backdrop_url = tmdb.get_image_url(movie.get("backdrop_path"), size="original")
    
    # We still use a bit of HTML for the background container aspect, but follow layout strictly
    st.markdown(f"""
    <div style="background-image: linear-gradient(to right, rgba(0,0,0,0.8), rgba(0,0,0,0)), url('{backdrop_url}'); 
                background-size: cover; height: 400px; border-radius: 15px; display: flex; align-items: center; padding: 40px; margin-bottom: 30px;">
        <div style="max-width: 50%;">
            <h1 style="font-size: 48px; margin-bottom: 10px;">{movie.get('title')}</h1>
            <p style="font-size: 16px; opacity: 0.8; margin-bottom: 20px;">{movie.get('overview')[:200]}...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Watch Trailer", key="hero_trailer_btn"):
        st.session_state.selected_movie_id = movie.get("id")
        st.session_state.page = "details"
        st.rerun()

def render_home():
    """Full homepage view."""
    trending = tmdb.get_trending_daily(limit=16)
    if trending:
        render_hero(trending[0])
        
        st.markdown("### Trending <span class='gold-text'>Now</span>", unsafe_allow_html=True)
        render_movie_grid(trending[1:11], key_prefix="home_trending")
        
        st.markdown("### Recommended for <span class='gold-text'>You</span>", unsafe_allow_html=True)
        top_rated = tmdb.get_top_rated_movies(limit=10)
        render_movie_grid(top_rated, key_prefix="home_rec")
