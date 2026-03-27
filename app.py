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

def get_nav_history():
    """Initialize or get the navigation history from session state."""
    if "nav_history" not in st.session_state:
        st.session_state.nav_history = [{"page": "home", "params": {}}]
    return st.session_state.nav_history

def push_nav_state(page, params=None):
    """Add current page to navigation history with loop prevention."""
    history = get_nav_history()
    params = params or {}
    
    # Avoid pushing duplicate consecutive entries
    if history and history[-1].get("page") == page and history[-1].get("params") == params:
        return
        
    # If we are navigating to the exact state that is one-step back in history,
    # treat it as a 'back' navigation and truncate history rather than appending.
    if len(history) >= 2:
        prev_state = history[-2]
        if prev_state.get("page") == page and prev_state.get("params") == params:
            history.pop()
            st.session_state.nav_history = history
            return
            
    history.append({"page": page, "params": params})
    st.session_state.nav_history = history

def get_back_url():
    """Get the URL to navigate back to the previous page."""
    history = get_nav_history()
    if len(history) > 1:
        prev_state = history[-2]
        page = prev_state.get("page", "home")
        params = prev_state.get("params", {})
        
        if page == "home":
            return "/"
        elif page == "movie_detail":
            movie_id = params.get("movie_id")
            return f"/?movie_id={movie_id}" if movie_id else "/"
        elif page == "category":
            category_id = params.get("category_id")
            title = params.get("title", "Category")
            return f"/?category_id={category_id}&title={title}" if category_id else "/"
        elif page == "search":
            query = params.get("query")
            return f"/?q={query}" if query else "/"
    
    return "/"  # Default fallback to home

def navigate_to_movie(movie_id):
    """Navigate to movie detail with history tracking."""
    push_nav_state("movie_detail", {"movie_id": movie_id})
    if "nav_history" in st.session_state:
        st.session_state.nav_history = st.session_state.nav_history

def render_movie_row(title, movies, key_prefix, category_id=None):
    """Render a premium horizontal scrollable row with native clickable overlays.
    
    Supports both movies and TV shows/series.
    """
    if not movies:
        return
        
    st.markdown(f'<h3 class="section-title">{title}</h3>', unsafe_allow_html=True)
    
    # Always use horizontal scroll to prevent wrapping
    movie_html = '<div class="movie-scroll">'
    for movie in movies:
        item_id = movie.get('id')
        # Detect media type - prefer explicit media_type field, fallback to checking for TV-specific fields
        media_type = movie.get('media_type', 'movie')
        if 'first_air_date' in movie and 'title' not in movie:
            media_type = 'tv'
        
        poster_url = tmdb.get_image_url(movie.get("poster_path"))
        card_html = ui.render_movie_card(movie, poster_url)
        
        # Build query params based on media type
        if media_type == 'tv':
            href = f"?tv_id={item_id}"
        else:
            href = f"?movie_id={item_id}"
        
        movie_html += f'<a href="{href}" target="_self" style="text-decoration: none; display: block;">'
        movie_html += '<div class="movie-item">'
        movie_html += card_html
        movie_html += '</div>'
        movie_html += '</a>'
    
    movie_html += '</div>'
    st.markdown(movie_html, unsafe_allow_html=True)

def render_detail_view(movie_id=None, tv_id=None):
    """Render movie or TV show details inline."""
    # Determine if it's a movie or TV show
    is_tv = tv_id is not None
    content_id = tv_id if is_tv else movie_id
    media_type = "tv" if is_tv else "movie"
    
    # Track that we're viewing a detail page
    nav_params = {"tv_id": tv_id} if is_tv else {"movie_id": movie_id}
    push_nav_state("movie_detail", nav_params)
    
    with st.spinner("Loading details..."):
        if is_tv:
            content = tmdb.get_tv_details(content_id)
            trailers = tmdb.get_tv_videos(content_id)
            cast, crew = tmdb.get_tv_credits(content_id)
        else:
            content = tmdb.get_movie_details(content_id)
            trailers = tmdb.get_movie_videos(content_id)
            cast, crew = tmdb.get_movie_credits(content_id)
            omdb_data = omdb.get_movie_reviews(content.get("title") if content else "")
        
    if not content:
        st.error(f"Could not load {'TV show' if is_tv else 'movie'} details.")
        if st.button("⬅ Back"):
            st.query_params.clear()
            st.rerun()
        return

    # Store previous params for back navigation
    if "previous_params" not in st.session_state:
        prev = dict(st.query_params)
        if "movie_id" in prev or "tv_id" in prev:
            if "movie_id" in prev: del prev["movie_id"]
            if "tv_id" in prev: del prev["tv_id"]
        st.session_state.previous_params = prev

    # Render Backdrop behind everything
    backdrop_url = tmdb.get_image_url(content.get("backdrop_path"), size="original")
    poster_url = tmdb.get_image_url(content.get("poster_path"))
    ui.render_detail_hero(content, backdrop_url, poster_url)
    
    # Top Back Button - Use dynamic back URL
    back_url = get_back_url()
    col_b, _ = st.columns([1.5, 8.5])
    with col_b:
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="{back_url}" target="_self" class="back-pill-btn">
                    <span style="margin-right: 8px;">←</span> BACK
                </a>
            </div>
        ''', unsafe_allow_html=True)
            
    # 2-Column Layout
    col1, col2 = st.columns([1, 2.5], gap="large")
    
    with col1:
        st.markdown(f'<div class="details-poster"><img src="{poster_url}"></div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="details-info">', unsafe_allow_html=True)
        
        # Handle title differences between movies and TV
        if is_tv:
            title = content.get("name", "Unknown")
            year = content.get("first_air_date", "N/A")[:4]
            status = content.get("status", "Unknown")
            meta_line = f"{year} &nbsp;|&nbsp; {status}"
        else:
            title = content.get("title", "Unknown")
            year = content.get("release_date", "N/A")[:4]
            runtime = f"{content.get('runtime', 'N/A')} min"
            meta_line = f"{year} &nbsp;|&nbsp; {runtime}"
        
        genres = ", ".join([g.get("name") for g in content.get("genres", [])])
        overview = content.get("overview", "")
        
        st.markdown(f'<h1 style="font-size: 48px; font-weight: 800; margin-bottom: 5px; line-height: 1.1;">{title}</h1>', unsafe_allow_html=True)
        
        if genres:
            meta_line += f" &nbsp;|&nbsp; {genres}"
        st.markdown(f'<div style="color: var(--gold); font-size: 16px; font-weight: 600; margin-bottom: 20px;">{meta_line}</div>', unsafe_allow_html=True)
        
        st.markdown(f'<p style="color: rgba(255,255,255,0.9); font-size: 16px; line-height: 1.6; margin-bottom: 30px;">{overview}</p>', unsafe_allow_html=True)
        
        # Display aggregated OMDB reviews only for movies
        if not is_tv:
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
        st.markdown('<div class="ott-title">Cast & Crew</div>', unsafe_allow_html=True)
        
        # Display crew info
        director = crew.get("director", "N/A")
        writer = crew.get("writer", "N/A")
        
        crew_html = f'<div style="margin-bottom: 15px; font-size: 14px;">'
        if director != "N/A":
            crew_label = "Creator" if is_tv else "Director"
            crew_html += f'<div style="margin-bottom: 5px;"><span style="color: var(--text-muted);">{crew_label}:</span> <span style="color: white; font-weight: 700;">{director}</span></div>'
        if not is_tv and writer != "N/A" and writer != director:
            crew_html += f'<div><span style="color: var(--text-muted);">Writer:</span> <span style="color: white; font-weight: 700;">{writer}</span></div>'
        elif not is_tv and writer != "N/A" and writer == director:
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
        
        # PROVIDER LINKS MAPPING - Only for movies
        if not is_tv:
            providers = tmdb.get_watch_providers(content_id)
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
    
    # Recommendations section (only for movies)
    if not is_tv:
        st.markdown('---')
        try:
            local_rec_ids = rec_engine.recommend_by_id(movie_id)
            recommendations = []
            if local_rec_ids:
                for r_id in local_rec_ids:
                    r_details = tmdb.get_movie_details(r_id)
                    if r_details: recommendations.append(r_details)
            if not recommendations:
                recommendations = tmdb.get_movie_recommendations(movie_id, limit=10)
                
            if recommendations:
                render_movie_row('Recommended <span class="gold-text">Movies</span>', recommendations, "rec")
        except:
            # Graceful fallback if recommendations engine fails
            pass
        
def render_category_view(category_id, title):
    # Track category view in history
    push_nav_state("category", {"category_id": category_id, "title": title})
    
    # Get back URL
    back_url = get_back_url()
    col_back, _ = st.columns([1.5, 8.5])
    with col_back:
        # Native back button for 100% styling reliability
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="{back_url}" target="_self" class="back-pill-btn">
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
    # Initialize session state
    if "query" not in st.session_state:
        st.session_state.query = ""
    
    # Persist search query on refresh
    params = st.query_params
    if "q" in params and not st.session_state.query:
        st.session_state.query = params["q"]
    
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
        st.markdown('<div class="search-input-wrapper">', unsafe_allow_html=True)
        search_query = st.text_input("Search", placeholder="Search movies, actors, genres...", value=st.session_state.query, key="global_search_input", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    # Update query state
    if search_query != st.session_state.query:
        st.session_state.query = search_query
        if search_query:
            st.query_params["q"] = search_query
        else:
            if "q" in st.query_params:
                del st.query_params["q"]
        st.rerun()

    # Handle Search Globally
    if search_query:
        # Store previous params for back navigation
        if "previous_params" not in st.session_state:
            st.session_state.previous_params = dict(params)
        
        # Push search to history
        push_nav_state("search", {"query": search_query})
        
        # Back button for search page - use dynamic back URL
        back_url = get_back_url()
        st.markdown(f'<a href="{back_url}" target="_self" class="back-pill-btn">← Back</a>', unsafe_allow_html=True)
        
        st.markdown(f'<h2>Search Results for <span class="gold-text">"{search_query}"</span></h2>', unsafe_allow_html=True)
        results = tmdb.search_movies(search_query)
        if results:
            # Always use horizontal scroll to prevent wrapping
            movie_html = '<div class="movie-row-container">'
            for movie in results:
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
        else:
            st.info("No movies found.")
        
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
        
        return

    # --- ROUTING ENGINE ---
    params = st.query_params
    
    if "movie_id" in params:
        m_id = params["movie_id"]
        if isinstance(m_id, list): m_id = m_id[0]
        render_detail_view(movie_id=int(m_id))
    elif "tv_id" in params:
        tv_id = params["tv_id"]
        if isinstance(tv_id, list): tv_id = tv_id[0]
        render_detail_view(tv_id=int(tv_id))
    elif "category_id" in params:
        cat_id = params["category_id"]
        if isinstance(cat_id, list): cat_id = cat_id[0]
        cat_title = params.get("title", "Category")
        if isinstance(cat_title, list): cat_title = cat_title[0]
        render_category_view(cat_id, cat_title)
    else:
        # ------------ HOME PAGE CONTENT ------------
        # Ensure home is in history
        if len(get_nav_history()) == 1 or (len(get_nav_history()) > 1 and get_nav_history()[-1].get("page") != "home"):
            push_nav_state("home", {})
        
        # Hero Slider with expanded diverse content and rotation logic
        if "hero_slides" not in st.session_state or not st.session_state.hero_slides:
            # Fetch diverse hero content from multiple sources (movies + shows, multiple genres)
            diverse_slides = tmdb.get_diverse_hero_content(limit=15)
            st.session_state.hero_slides = diverse_slides[:15] if diverse_slides else []
        
        # Initialize hero rotation index (changes on each app refresh/session restart)
        if "hero_rotation_index" not in st.session_state:
            # Use session-based rotation - index changes each time session is created
            st.session_state.hero_rotation_index = random.randint(0, max(0, len(st.session_state.hero_slides) - 1))
        
        if st.session_state.hero_slides:
            # Rotate slides so first hero movie changes on refresh
            rotated_slides = st.session_state.hero_slides[st.session_state.hero_rotation_index:] + st.session_state.hero_slides[:st.session_state.hero_rotation_index]
            ui.render_slideshow(rotated_slides)

        def get_daily_shuffled_favorites():
            """Return exactly 10 movies that change daily based on current date."""
            from datetime import date
            top_movies = tmdb.get_top_rated_movies(limit=50)
            if not top_movies: return []
            today_val = date.today().toordinal()
            rng = random.Random(today_val)
            shuffled = list(top_movies)
            rng.shuffle(shuffled)
            return shuffled[:10]  # Return exactly 10

        # Premium Content Selection - Show all movies directly in scrollable rows
        render_movie_row("New Releases Worldwide", tmdb.get_new_releases_worldwide(limit=30), "new_releases")
        render_movie_row("Indian Movies in OTT", tmdb.get_trending_indian(limit=30), "ind")
        render_movie_row("All-Time Favorites", get_daily_shuffled_favorites(), "fav")
        
        # Other Languages (Unified)
        other_movies = tmdb.get_other_languages_ott(limit=30)
        render_movie_row("Trending Worldwide (Regional)", other_movies, "other")

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