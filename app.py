import streamlit as st
import re

def strip_html(text):
    """Remove HTML tags from a string for safe URL usage."""
    return re.sub('<[^<]+?>', '', text)

import tmdb_service as tmdb
import omdb_service as omdb
import components as ui
import time
import datetime
import random
from pages import movie_details

# Set page config
st.set_page_config(
    page_title="MovieBuddy | Premium Streaming",
    page_icon="🎞️",
    layout="wide"
)

# NOTE ON STREAMLIT CLOUD HIBERNATION:
# On Streamlit Community Cloud, apps hibernate after inactivity.
# We use optimized caching (@st.cache_data) in tmdb_service.py to ensure 
# fast recovery and smooth performance upon wake-up.

# Inject Custom CSS
ui.inject_custom_css()

# Background Texture
st.markdown('<div class="bg-texture"></div>', unsafe_allow_html=True)

def navigate_to(page, **kwargs):
    """Push a new page to the navigation stack."""
    if "page_stack" not in st.session_state:
        st.session_state.page_stack = [{"page": "home"}]
    
    # Avoid pushing the exact same page twice
    current = st.session_state.page_stack[-1]
    if current.get("page") == page and current.get("kwargs") == kwargs:
        return
        
    st.session_state.page_stack.append({"page": page, "kwargs": kwargs})
    st.session_state.scroll_to_top = True
    st.rerun()

def navigate_back():
    """Pop the current page and return to the previous."""
    if "page_stack" in st.session_state and len(st.session_state.page_stack) > 1:
        st.session_state.page_stack.pop()
    else:
        st.session_state.page_stack = [{"page": "home"}]
    st.session_state.scroll_to_top = True
    st.rerun()

def render_movie_row(title, movies, key_prefix, category_id=None):
    """Render a premium horizontal scrollable row with native clickable overlays."""
    if not movies:
        return
        
    st.markdown(f'<h3 style="margin-top: 30px; margin-bottom: 15px;">{title}</h3>', unsafe_allow_html=True)
    cols = st.columns(6, gap="small")
    
    # Show up to 5 movies
    for idx, movie in enumerate(movies[:5]):
        with cols[idx]:
            movie_id = movie.get('id')
            poster_url = tmdb.get_image_url(movie.get("poster_path"))
            # Wrap in anchor for artifact-free navigation
            st.markdown(f'''
                <a href="?movie_id={movie_id}" target="_self" style="text-decoration: none; display: block;">
                    <div class="native-card-wrapper">
                        {ui.render_movie_card(movie, poster_url)}
                    </div>
                </a>
            ''', unsafe_allow_html=True)
                
    # See More card
    if category_id and len(movies) >= 6:
        with cols[5]:
            clean_title = strip_html(title).replace(' ', '+')
            # Wrap See More in anchor with clean title
            st.markdown(f'''
                <a href="?category_id={category_id}&title={clean_title}" target="_self" style="text-decoration: none; display: block;">
                    <div class="native-card-wrapper">
                        {ui.render_see_more_card()}
                    </div>
                </a>
            ''', unsafe_allow_html=True)

def render_detail_view(movie_id):
    """Bridge to the standalone detail page."""
    movie_details.render_movie_details_page()

def render_category_view(category_id, title):
    col_back, _ = st.columns([1.5, 8.5])
    with col_back:
        # Native back button for 100% styling reliability
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="/?home=true" target="_self" class="back-pill-btn">
                    <span style="margin-right: 8px;">←</span> BACK
                </a>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown(f'<h2 style="margin-top: 10px;">{title}</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Fetch data based on category mapping
    movies = []
    with st.spinner("Loading movies..."):
        if category_id == "new_releases":
            movies = tmdb.get_new_releases_worldwide(limit=40)
        elif category_id == "all_time":
            movies = tmdb.get_top_rated_movies(limit=40)
        elif category_id == "trending_te":
            movies = tmdb.get_trending_by_language("te", limit=40)
        elif category_id == "trending_hi":
            movies = tmdb.get_trending_by_language("hi", limit=40)
        elif category_id == "trending_ta":
            movies = tmdb.get_trending_by_language("ta", limit=40)
        elif category_id == "trending_kn":
            movies = tmdb.get_trending_by_language("kn", limit=40)
        elif category_id == "trending_ml":
            movies = tmdb.get_trending_by_language("ml", limit=40)
        elif category_id == "trending_indian":
            movies = tmdb.get_trending_indian(limit=40)
        elif category_id == "other_lang":
            movies = tmdb.get_other_languages_ott(limit=40)
        elif str(category_id).startswith("rec_"):
            m_id = category_id.split("_")[1]
            movies = tmdb.get_movie_recommendations(m_id, limit=20)
            
    if not movies:
        st.warning("No movies found in this category.")
        return
        
    for row in range(0, len(movies), 4):
        cols = st.columns(4)
        for idx, movie in enumerate(movies[row:row+4]):
            with cols[idx]:
                movie_id = movie.get('id')
                poster_url = tmdb.get_image_url(movie.get("poster_path"))
                # Wrap in anchor for artifact-free navigation
                st.markdown(f'''
                    <a href="?movie_id={movie_id}" target="_self" style="text-decoration: none; display: block;">
                        <div class="native-card-wrapper">
                            {ui.render_movie_card(movie, poster_url)}
                        </div>
                    </a>
                ''', unsafe_allow_html=True)

# --- Main Layout ---
def main():
    # Robust scroll-to-top fix
    if st.session_state.get("scroll_to_top"):
        st.components.v1.html("""
        <script>
        function scrollToTop() {
            try {
                window.scrollTo(0, 0);
                if (window.parent) {
                    window.parent.scrollTo(0, 0);
                    var mainContent = window.parent.document.querySelector('.main') || 
                                     window.parent.document.querySelector('.stApp');
                    if (mainContent) mainContent.scrollTop = 0;
                }
            } catch (e) {
                console.error("Scroll error:", e);
                window.scrollTo(0, 0);
            }
        }
        scrollToTop();
        window.onload = scrollToTop;
        setTimeout(scrollToTop, 10);
        setTimeout(scrollToTop, 100);
        </script>
        """, height=0)
        st.session_state.scroll_to_top = False

    # --- GLOBAL UI: Header, Logo, & Search Bar ---
    head_col1, head_col2 = st.columns([4, 2], gap="large")
    with head_col1:
        st.markdown(f'''
            <a href="/?home=true" target="_self" class="logo-link">
                <span class="logo-text"><span class="logo-movie">Movie</span><span class="logo-buddy">Buddy</span></span>
            </a>
        ''', unsafe_allow_html=True)
    with head_col2:
        search_query = st.text_input("Search", placeholder="Search movies, actors, genres...", key="global_search_input", label_visibility="collapsed")

    # Handle Search Globally
    if search_query:
        st.markdown(f'<h2>Search Results for <span class="gold-text">"{search_query}"</span></h2>', unsafe_allow_html=True)
        results = tmdb.search_movies(search_query)
        if results:
            for row in range(0, len(results), 5):
                cols = st.columns(5)
                for idx, movie in enumerate(results[row:row+5]):
                    with cols[idx]:
                        movie_id = movie.get('id')
                        poster_url = tmdb.get_image_url(movie.get("poster_path"))
                        st.markdown(f'''
                            <a href="?movie_id={movie_id}" target="_self" style="text-decoration: none; display: block;">
                                <div class="native-card-wrapper">
                                    {ui.render_movie_card(movie, poster_url)}
                                </div>
                            </a>
                        ''', unsafe_allow_html=True)
        else:
            st.info("No movies found.")
        return

    # --- ROUTING ENGINE ---
    params = st.query_params
    
    if "movie_id" in params:
        m_id = params["movie_id"]
        if isinstance(m_id, list): m_id = m_id[0]
        render_detail_view(int(m_id))
    elif "category_id" in params:
        cat_id = params["category_id"]
        if isinstance(cat_id, list): cat_id = cat_id[0]
        cat_title = params.get("title", "Category")
        if isinstance(cat_title, list): cat_title = cat_title[0]
        render_category_view(cat_id, cat_title)
    else:
        # ------------ HOME PAGE CONTENT ------------
        # Hero Slider
        if "hero_slides" not in st.session_state or not st.session_state.hero_slides:
            st.session_state.hero_slides = tmdb.get_now_playing_movies(limit=10)
        
        if st.session_state.hero_slides:
            ui.render_slideshow(st.session_state.hero_slides)
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

        # Content Rows logic
        used_movie_counts = {}
        def prioritize_movies(movies_list):
            row_final = []
            for m in movies_list:
                mid = m.get('id')
                if used_movie_counts.get(mid, 0) < 2:
                    row_final.append(m)
                    used_movie_counts[mid] = used_movie_counts.get(mid, 0) + 1
                if len(row_final) == 6: break
            return row_final

        def get_daily_shuffled_favorites():
            from datetime import date
            top_movies = tmdb.get_top_rated_movies(limit=40)
            if not top_movies: return []
            today_val = date.today().toordinal()
            rng = random.Random(today_val)
            shuffled = list(top_movies)
            rng.shuffle(shuffled)
            return shuffled

        # Premium Content Selection
        render_movie_row("New Releases Worldwide", prioritize_movies(tmdb.get_new_releases_worldwide(limit=40)), "new_releases", "new_releases")
        render_movie_row("New Indian Releases", prioritize_movies(tmdb.get_trending_indian(limit=40)), "ind", "trending_indian")
        render_movie_row("All-Time Favorites", prioritize_movies(get_daily_shuffled_favorites()), "fav", "all_time")
        
        # Other Languages (Unified)
        other_movies = tmdb.get_other_languages_ott(limit=40)
        render_movie_row("Trending Worldwide (Regional)", prioritize_movies(other_movies), "other", "other_lang")

    # --- GLOBAL UI: Footer ---
    st.markdown("""
    <div style="margin-top: 80px; text-align: center; color: var(--text-muted); font-size: 13px; border-top: 1px solid rgba(255,255,255,0.08); padding: 30px 0;">
        🎬 MovieBuddy - Premium Cinematic Experience
        <br>
        Powered by TMDB API & OMDb API • Designed by <b>Shrikanth</b>
        <br>
        All rights reserved © 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()