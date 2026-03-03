import streamlit as st
import tmdb_service as tmdb
import components as ui
import time
import recommendation as rec_engine
import datetime
import random

# Set page config
# Set page config
st.set_page_config(
    page_title="MovieBuddy | Premium Streaming",
    page_icon="🎞️",
    layout="wide"
)

# Inject Custom CSS
ui.inject_custom_css()

# Background Texture
st.markdown('<div class="bg-texture"></div>', unsafe_allow_html=True)

def render_movie_grid(movies, key_prefix="grid"):
    if not movies:
        st.warning("No movies found.")
        return
        
    for row in range(0, len(movies), 5):
        cols = st.columns(5)
        for idx, movie in enumerate(movies[row:row+5]):
            with cols[idx]:
                poster_url = tmdb.get_image_url(movie.get("poster_path"))
                st.markdown(ui.render_movie_card(movie, poster_url), unsafe_allow_html=True)
                if st.button("View Details", key=f"{key_prefix}_{movie.get('id')}_{row}_{idx}", use_container_width=True):
                    st.session_state.selected_movie_id = movie.get("id")
                    st.rerun()

def render_detail_view(movie_id):
    with st.spinner("Loading movie details..."):
        movie = tmdb.get_movie_details(movie_id)
        trailers = tmdb.get_movie_videos(movie_id)
        
        # Enhanced Recommendation Logic: Local ML -> TMDB Fallback
        local_rec_ids = rec_engine.recommend_by_id(movie_id)
        recommendations = []
        
        if local_rec_ids:
            # If we have local recommendations, fetch their TMDB details for posters/titles
            for r_id in local_rec_ids:
                r_details = tmdb.get_movie_details(r_id)
                if r_details:
                    recommendations.append(r_details)
        
        # Fallback to TMDB recommendations if local ones are empty or failed
        if not recommendations:
            recommendations = tmdb.get_movie_recommendations(movie_id, limit=8)
    
    if not movie:
        st.error("Could not load movie details.")
        if st.button("Back to Home"):
            st.session_state.selected_movie_id = None
            st.rerun()
        return

    # Detail Hero
    backdrop_url = tmdb.get_image_url(movie.get("backdrop_path"), size="original")
    ui.render_detail_hero(movie, backdrop_url)

    # OTT Providers Section
    providers = tmdb.get_watch_providers(movie_id)
    ui.render_watch_providers(providers)

    # Action Buttons
    col1, _ = st.columns([1, 4])
    with col1:
        watch_trailer = st.button("▶ WATCH TRAILER", use_container_width=True)
    
    if watch_trailer:
        if trailers:
            trailer_key = trailers[0].get("key")
            st.video(f"https://www.youtube.com/watch?v={trailer_key}")
        else:
            st.warning("Trailer not available.")

    st.markdown("---")
    
    # Recommendations Fix
    st.markdown('<h2>Recommended <span class="gold-text">Movies</span></h2>', unsafe_allow_html=True)
    if recommendations and len(recommendations) > 0:
        for row in range(0, len(recommendations), 4):
            cols = st.columns(4)
            for idx, rec in enumerate(recommendations[row:row+4]):
                with cols[idx]:
                    poster_url = tmdb.get_image_url(rec.get("poster_path"))
                    st.markdown(ui.render_movie_card(rec, poster_url), unsafe_allow_html=True)
                    if st.button("View Details", key=f"rec_{rec.get('id')}_{row}_{idx}", use_container_width=True):
                        st.session_state.selected_movie_id = rec.get("id")
                        st.rerun()
    else:
        st.info("No recommendations available.")

# --- Main Layout ---
def main():
    # Handle Home Reset via Query Params
    if st.query_params.get("home") == "true":
        st.session_state.selected_movie_id = None
        if "last_search" in st.session_state:
            del st.session_state["last_search"]
        st.query_params.clear()
        st.rerun()

    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None
    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0
    if "last_slide_time" not in st.session_state:
        st.session_state.last_slide_time = time.time()

    # Persistent Top Header (Logo + Search)
    head_col1, head_col2 = st.columns([4, 1])
    with head_col1:
        # Premium Text Logo (HTML Link)
        st.markdown('''
            <a href="/?home=true" target="_self" class="logo-link">
                <span class="logo-text">
                    <span class="logo-movie">Movie</span><span class="logo-buddy">Buddy</span>
                </span>
            </a>
        ''', unsafe_allow_html=True)
        
    with head_col2:
        search_query = st.text_input("", placeholder="Search movies...", key="movie_search_input", label_visibility="collapsed")

    # Routing Logic
    if search_query:
        if st.session_state.get("last_search") != search_query:
            st.session_state.selected_movie_id = None
            st.session_state.last_search = search_query
            
        if st.session_state.selected_movie_id:
            render_detail_view(st.session_state.selected_movie_id)
            return

        st.markdown(f'<h2>Search Results for <span class="gold-text">"{search_query}"</span></h2>', unsafe_allow_html=True)
        results = tmdb.search_movies(search_query)
        render_movie_grid(results[:15], key_prefix="search")
        st.markdown("---")
        return 

    if st.session_state.selected_movie_id:
        render_detail_view(st.session_state.selected_movie_id)
        return

    # Home Page - Featured Movie (Daily Rotation)
    trending_all = tmdb.get_trending_weekly(limit=20)
    # Filter valid movies (must have backdrop and overview)
    valid_trending = [m for m in trending_all if m.get("backdrop_path") and m.get("overview")]
    
    if valid_trending:
        # Option A: Daily rotation (deterministic based on date)
        today_seed = int(datetime.date.today().strftime("%Y%m%d"))
        featured_index = today_seed % len(valid_trending)
        
        # Calculate current slide index based on user navigation + daily rotation
        current_slide_index = (st.session_state.slide_index + featured_index) % len(valid_trending)
        current_slide = valid_trending[current_slide_index]
        
        backdrop_url = tmdb.get_image_url(current_slide.get("backdrop_path"), size="original")
        ui.render_slideshow(current_slide, backdrop_url)
        
        # Slideshow Navigation & Watch Button
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1, 8])
        with ctrl_col1:
            if st.button("❮ Prev"):
                st.session_state.slide_index = (st.session_state.slide_index - 1) % len(valid_trending)
                st.rerun()
        with ctrl_col2:
            if st.button("Next ❯"):
                st.session_state.slide_index = (st.session_state.slide_index + 1) % len(valid_trending)
                st.rerun()
        with ctrl_col3:
            if st.button("▶ WATCH NOW", key=f"hero_watch_{current_slide.get('id')}"):
                st.session_state.selected_movie_id = current_slide.get("id")
                st.rerun()

    # Recommendations Section (Top Rated)
    st.markdown('<h2 style="margin-top: 40px;">Featured <span class="gold-text">Movies</span></h2>', unsafe_allow_html=True)
    top_rated = tmdb.get_top_rated_movies(limit=10)
    render_movie_grid(top_rated, key_prefix="home")

    # Footer
    st.markdown("""
    <div style="margin-top: 80px; text-align: center; color: var(--text-muted); font-size: 13px; border-top: 1px solid rgba(255,255,255,0.08); padding: 30px 0;">
        🎬 MovieBuddy - Premium Cinematic Experience
        <br>
        Powered by TMDB API • Designed by <b>Shrikanth</b>
        <br>
        All rights reserved © 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()