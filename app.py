import streamlit as st
import re

def strip_html(text):
    """Remove HTML tags from a string for safe URL usage."""
    return re.sub('<[^<]+?>', '', text)

import tmdb_service as tmdb
import omdb_service as omdb
import components as ui
import recommendation as rec_engine
import time
import datetime
import random

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

# Inject Custom CSS (with error handling)
try:
    ui.inject_custom_css()
except Exception as e:
    st.error(f"CSS injection failed: {e}")
    print(f"CSS Error: {e}")  # Terminal log

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

def render_movie_row(title, movies, key_prefix, category_id=None, max_items=5, show_see_more=True):
    """Render a premium horizontal scrollable row with native clickable overlays."""
    if not movies:
        return
        
def render_movie_row(title, movies, key_prefix, category_id=None, max_items=5, show_see_more=True):
    """Render a premium horizontal scrollable row with native clickable overlays."""
    if not movies:
        return
        
    st.markdown(f'<h3 style="margin-top: 30px; margin-bottom: 15px;">{title}</h3>', unsafe_allow_html=True)
    
    if max_items <= 6:
        # Use grid layout for small numbers
        cols = st.columns(max_items, gap="small")
        for idx, movie in enumerate(movies[:max_items]):
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
                    
        # See More card
        if show_see_more and category_id and len(movies) > max_items:
            with cols[max_items-1]:
                clean_title = strip_html(title).replace(' ', '+')
                st.markdown(f'''
                    <a href="?category_id={category_id}&title={clean_title}" target="_self" style="text-decoration: none; display: block;">
                        <div class="native-card-wrapper">
                            {ui.render_see_more_card()}
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
    else:
        # Use horizontal scroll for large numbers
        movie_html = '<div class="movie-scroll">'
        for movie in movies[:max_items]:
            movie_id = movie.get('id')
            poster_url = tmdb.get_image_url(movie.get("poster_path"))
            card_html = ui.render_movie_card(movie, poster_url)
            movie_html += '<a href="?movie_id=' + str(movie_id) + '" target="_self" style="text-decoration: none; display: block;">'
            movie_html += '<div class="movie-item">'
            movie_html += card_html
            movie_html += '</div>'
            movie_html += '</a>'
        movie_html += '</div>'
        st.markdown(movie_html, unsafe_allow_html=True)

def render_detail_view(movie_id):
    """Render movie details inline."""
    with st.spinner("Loading movie details..."):
        movie = tmdb.get_movie_details(movie_id)
        trailers = tmdb.get_movie_videos(movie_id)
        omdb_data = omdb.get_movie_reviews(movie.get("title"))
        
    if not movie:
        st.error("Could not load movie details.")
        if st.button("⬅ Back"):
            st.query_params.clear()
            st.rerun()
        return

    # Render Backdrop behind everything
    backdrop_url = tmdb.get_image_url(movie.get("backdrop_path"), size="original")
    poster_url = tmdb.get_image_url(movie.get("poster_path"))
    ui.render_detail_hero(movie, backdrop_url, poster_url)
    
    # Top Back Button
    col_b, _ = st.columns([1.5, 8.5])
    with col_b:
        st.markdown('<div class="back-btn-col">', unsafe_allow_html=True)
        if st.button("← Back", key=f"det_back_{movie_id}"):
            st.query_params.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    # 2-Column Layout
    col1, col2 = st.columns([1, 2.5], gap="large")
    
    with col1:
        st.markdown(f'<div class="details-poster"><img src="{poster_url}"></div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="details-info">', unsafe_allow_html=True)
        
        title = movie.get("title")
        year = movie.get("release_date", "N/A")[:4]
        runtime = f"{movie.get('runtime', 'N/A')} min"
        genres = ", ".join([g.get("name") for g in movie.get("genres", [])])
        overview = movie.get("overview", "")
        
        st.markdown(f'<h1 style="font-size: 48px; font-weight: 800; margin-bottom: 5px; line-height: 1.1;">{title}</h1>', unsafe_allow_html=True)
        st.markdown(f'<div style="color: var(--gold); font-size: 16px; font-weight: 600; margin-bottom: 20px;">{year} &nbsp;|&nbsp; {runtime} &nbsp;|&nbsp; {genres}</div>', unsafe_allow_html=True)
        
        st.markdown(f'<p style="color: rgba(255,255,255,0.9); font-size: 16px; line-height: 1.6; margin-bottom: 30px;">{overview}</p>', unsafe_allow_html=True)
        
        # Display aggregated OMDB Without Reviews
        ui.render_omdb_reviews(omdb_data)
        
        st.markdown('</div>', unsafe_allow_html=True) # End of details-info
        
    # Trailer and Where to Watch Side-by-Side (Full Width)
    st.markdown('<br>', unsafe_allow_html=True)
    col_vid, col_prov = st.columns([1.5, 1], gap="large")
    
    with col_vid:
        st.markdown('<div class="ott-title" style="margin-bottom: 10px;">🎬 Trailer</div>', unsafe_allow_html=True)
        if trailers:
            st.video(f"https://www.youtube.com/watch?v={trailers[0].get('key')}")
        else:
            st.markdown('<div style="color: var(--text-muted);">Trailer Unavailable</div>', unsafe_allow_html=True)
            
    with col_prov:
        cast, crew = tmdb.get_movie_credits(movie_id)
        st.markdown('<div class="ott-title">Cast & Crew</div>', unsafe_allow_html=True)
        
        # Combined Director & Writer display for cleaner hierarchy
        director = crew.get("director", "N/A")
        writer = crew.get("writer", "N/A")
        
        crew_html = f'<div style="margin-bottom: 15px; font-size: 14px;">'
        if director != "N/A":
            crew_html += f'<div style="margin-bottom: 5px;"><span style="color: var(--text-muted);">Director:</span> <span style="color: white; font-weight: 700;">{director}</span></div>'
        if writer != "N/A" and writer != director:
            crew_html += f'<div><span style="color: var(--text-muted);">Writer:</span> <span style="color: white; font-weight: 700;">{writer}</span></div>'
        elif writer != "N/A" and writer == director:
            # Handle same person case elegantly
            crew_html = f'<div style="margin-bottom: 15px; font-size: 14px;"><div style="margin-bottom: 5px;"><span style="color: var(--text-muted);">Director & Writer:</span> <span style="color: white; font-weight: 700;">{director}</span></div>'
        crew_html += '</div>'
        st.markdown(crew_html, unsafe_allow_html=True)
        
        # Cast display using horizontal scroll container
        if cast:
            cast_html = '<div class="cast-scroll">'
            for actor in cast[:8]:
                profile_path = actor.get("profile_path")
                img = f"https://image.tmdb.org/t/p/w185{profile_path}" if profile_path else "https://via.placeholder.com/120x120?text=No+Photo"
                name = actor.get('name', 'Unknown')
                character = actor.get('character', 'Actor')
                cast_html += '<div class="cast-item">'
                cast_html += f'<img src="{img}" class="cast-img" alt="{name}">'
                cast_html += f'<div class="cast-name">{name}</div>'
                cast_html += f'<div class="cast-role">{character}</div>'
                cast_html += '</div>'
            cast_html += '</div>'
            st.markdown(cast_html, unsafe_allow_html=True)
        
        # PROVIDER LINKS MAPPING
        providers = tmdb.get_watch_providers(movie_id)
        if providers:
            st.markdown('<div class="ott-title" style="margin-top: 25px;">Available On</div>', unsafe_allow_html=True)
            
            provider_map = {
                "Netflix": "https://www.netflix.com/",
                "Amazon Prime Video": "https://www.primevideo.com/",
                "Disney Plus": "https://www.disneyplus.com/",
                "Hotstar": "https://www.hotstar.com/",
                "Apple TV": "https://tv.apple.com/",
                "Google Play Movies": "https://play.google.com/store/movies",
                "YouTube": "https://www.youtube.com/",
                "JioCinema": "https://www.jiocinema.com/",
                "ZEE5": "https://www.zee5.com/"
            }
            
            stream_list = providers.get("flatrate", [])
            if stream_list:
                html_prov = '<div class="provider-grid">'
                for p in stream_list:
                    name = p.get("provider_name")
                    logo = f"https://image.tmdb.org/t/p/original{p.get('logo_path')}"
                    link = provider_map.get(name, "https://www.google.com/search?q=" + name.replace(" ", "+"))
                    html_prov += f'<a href="{link}" target="_blank" title="{name}"><img src="{logo}" class="provider-logo"></a>'
                html_prov += '</div>'
                st.markdown(html_prov, unsafe_allow_html=True)
            else:
                st.markdown('<div style="color: var(--text-muted);">Direct streaming links unavailable.</div>', unsafe_allow_html=True)

            
    # End of details layout
    
    # Recommendations Fix (Using Standard Movie Row)
    st.markdown('---')
    local_rec_ids = rec_engine.recommend_by_id(movie_id)
    recommendations = []
    if local_rec_ids:
        for r_id in local_rec_ids:
            r_details = tmdb.get_movie_details(r_id)
            if r_details: recommendations.append(r_details)
    if not recommendations:
        recommendations = tmdb.get_movie_recommendations(movie_id, limit=10)
        
    if recommendations:
        render_movie_row('Recommended <span class="gold-text">Movies</span>', recommendations, "rec", category_id=f"rec_{movie_id}", max_items=10, show_see_more=False)

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