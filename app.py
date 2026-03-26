import streamlit as st
import tmdb_service as tmdb
import omdb_service as omdb
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
    """Render a premium horizontal scrollable row of movies (Netflix-style)."""
    if not movies:
        return
        
    st.markdown(f'<h3 style="margin-top: 30px; margin-bottom: 15px;">{title}</h3>', unsafe_allow_html=True)
    
    # We use a single markdown block for the entire row to ensure smooth horizontal scrolling
    row_html = '<div class="movie-row-container">'
    
    # Populate movies
    for movie in movies[:15]: # Show up to 15 in the row
        poster_url = tmdb.get_image_url(movie.get("poster_path"))
        card_html = ui.render_movie_card(movie, poster_url)
        row_html += f'<div class="movie-card-wrapper">{card_html}</div>'
        
    # See More Card
    see_more_link = f"/?category_id={category_id}&title={title}"
    row_html += f"""
    <div class="movie-card-wrapper">
        <a href="{see_more_link}" target="_parent" style="text-decoration: none;">
            {ui.render_see_more_card()}
        </a>
    </div>
    """
    
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

def render_detail_view(movie_id):
    with st.spinner("Loading movie details..."):
        movie = tmdb.get_movie_details(movie_id)
        trailers = tmdb.get_movie_videos(movie_id)
        omdb_data = omdb.get_movie_reviews(movie.get("title"))
        
    if not movie:
        st.error("Could not load movie details.")
        if st.button("⬅ Back"):
            navigate_back()
        return

    # Render Backdrop behind everything
    backdrop_url = tmdb.get_image_url(movie.get("backdrop_path"), size="original")
    poster_url = tmdb.get_image_url(movie.get("poster_path"))
    ui.render_detail_hero(movie, backdrop_url, poster_url)
    
    # Top Back Button
    col_b, _ = st.columns([1, 9])
    with col_b:
        if st.button("Back", key=f"det_back_{movie_id}", use_container_width=True):
            navigate_back()
            
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
        cast, director = tmdb.get_movie_credits(movie_id)
        st.markdown('<div class="ott-title">Cast & Crew</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color: var(--text-muted); margin-bottom: 15px;">Director: <span style="color: white; font-weight: 700;">{director}</span></div>', unsafe_allow_html=True)
        
        cast_html = '<div class="cast-scroll">'
        for actor in cast[:6]:
            profile_path = actor.get("profile_path")
            img = f"https://image.tmdb.org/t/p/w185{profile_path}" if profile_path else "https://via.placeholder.com/100x100?text=No+Photo"
            name = actor.get("name")
            role = actor.get("character")
            cast_html += f"""
            <div class="cast-item">
                <img src="{img}" class="cast-img">
                <span class="cast-name">{name}</span>
                <span class="cast-role">{role}</span>
            </div>
            """
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
        render_movie_row('Recommended <span class="gold-text">Movies</span>', recommendations, "rec", category_id=f"rec_{movie_id}")

def render_category_view(category_id, title):
    """Grid layout for See More pages."""
    col_back, _ = st.columns([1, 9])
    with col_back:
        if st.button("Back", key=f"back_{category_id}", use_container_width=True):
            navigate_back()
        
    st.markdown(f'<h2 style="margin-top: 10px;">{title}</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Fetch data based on category mapping
    movies = []
    with st.spinner("Loading movies..."):
        if category_id == "all_time":
            movies = tmdb.get_top_rated_movies(limit=40)
        elif category_id == "recent_ott":
            movies = tmdb.get_recent_ott_movies(limit=40)
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
                poster_url = tmdb.get_image_url(movie.get("poster_path"))
                st.markdown(ui.render_movie_card(movie, poster_url), unsafe_allow_html=True)

# --- Main Layout ---
def main():
    # Robust scroll-to-top fix: only fires when specifically requested via session state
    if st.session_state.get("scroll_to_top"):
        st.components.v1.html("""
        <script>
        function scrollToTop() {
            try {
                // Target both the iframe window and the parent window
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
        // Fire multiple times to ensure various browser life-cycles are caught
        scrollToTop();
        window.onload = scrollToTop;
        setTimeout(scrollToTop, 10);
        setTimeout(scrollToTop, 100);
        </script>
        """, height=0)
        st.session_state.scroll_to_top = False

    if "page_stack" not in st.session_state:
        st.session_state.page_stack = [{"page": "home"}]

    # --- 1. Query Param Deep-Link Handling ---
    params = st.query_params
    
    # Check for movie_id
    if "movie_id" in params:
        m_id = params["movie_id"]
        if isinstance(m_id, list): m_id = m_id[0]
        
        # Check current page to avoid infinite rerun loops
        active_page = st.session_state.page_stack[-1]
        is_already_on_this_movie = (active_page.get("page") == "details" and 
                                   str(active_page.get("kwargs", {}).get("movie_id")) == str(m_id))
        
        if not is_already_on_this_movie:
            # Clear params before navigating to keep URL clean on next interaction
            st.query_params.clear()
            navigate_to("details", movie_id=int(m_id))
            st.rerun()

    # Check for category_id
    if "category_id" in params:
        cat_id = params["category_id"]
        if isinstance(cat_id, list): cat_id = cat_id[0]
        cat_title = params.get("title", "Category")
        if isinstance(cat_title, list): cat_title = cat_title[0]
        
        active_page = st.session_state.page_stack[-1]
        is_already_on_this_cat = (active_page.get("page") == "category" and 
                                 active_page.get("kwargs", {}).get("category_id") == cat_id)
        
        if not is_already_on_this_cat:
            st.query_params.clear()
            navigate_to("category", category_id=cat_id, title=cat_title)
            st.rerun()

    if params.get("home") == "true":
        st.query_params.clear()
        st.session_state.page_stack = [{"page": "home"}]
        st.session_state.scroll_to_top = True
        st.rerun()

    # Persistent Top Header
    head_col1, head_col2 = st.columns([4, 1])
    with head_col1:
        st.markdown(f'''
            <a href="/?home=true" target="_self" class="logo-link">
                <span class="logo-text">
                    <span class="logo-movie">Movie</span><span class="logo-buddy">Buddy</span>
                </span>
            </a>
        ''', unsafe_allow_html=True)
        
    with head_col2:
        search_query = st.text_input("", placeholder="Search movies...", key="movie_search_input", label_visibility="collapsed")

    # If active search, hijack navigation to show results
    if search_query:
        if st.session_state.get("last_search") != search_query:
            st.session_state.last_search = search_query
            st.session_state.page_stack = [{"page": "search_results", "kwargs": {"query": search_query}}]
            st.rerun()

    # Get current page from stack
    current_page = st.session_state.page_stack[-1]
    page_name = current_page.get("page")
    kwargs = current_page.get("kwargs", {})

    # Route Request
    if page_name == "details":
        render_detail_view(kwargs.get("movie_id"))
        return
    elif page_name == "category":
        render_category_view(kwargs.get("category_id"), kwargs.get("title"))
        return
    elif page_name == "search_results":
        query = kwargs.get("query")
        st.markdown(f'<h2>Search Results for <span class="gold-text">"{query}"</span></h2>', unsafe_allow_html=True)
        results = tmdb.search_movies(query)
        if results:
            for row in range(0, len(results), 5):
                cols = st.columns(5)
                for idx, movie in enumerate(results[row:row+5]):
                    with cols[idx]:
                        poster_url = tmdb.get_image_url(movie.get("poster_path"))
                        st.markdown(ui.render_movie_card(movie, poster_url), unsafe_allow_html=True)
        else:
            st.warning("No results found.")
            if st.button("⬅ Back Home"):
                navigate_to("home")
        return

    # ------------ HOME PAGE ------------
    if "hero_slides" not in st.session_state or not st.session_state.hero_slides:
        try:
            slides = tmdb.get_now_playing_movies(limit=10)
        except (AttributeError, Exception):
            slides = []
        
        # Fallback to general trending if now_playing fails or is empty
        if not slides:
            try:
                slides = tmdb.get_trending_weekly(limit=10)
            except (AttributeError, Exception):
                slides = []
            
        st.session_state.hero_slides = slides

    if st.session_state.hero_slides:
        ui.render_slideshow(st.session_state.hero_slides)

    # Netflix-Style Rows
    # Create a deduplication set to limit movie repetition to a maximum of 2 times across all rows
    used_movie_counts = {}

    def prioritize_movies(movies_list):
        """Filter list to max 2 occurrences per movie and return exactly enough to trigger See More (6) or less."""
        row_final = []
        for m in movies_list:
            mid = m.get('id')
            if used_movie_counts.get(mid, 0) < 2:
                row_final.append(m)
                used_movie_counts[mid] = used_movie_counts.get(mid, 0) + 1
            if len(row_final) == 6: # Return 6 to trigger See More (since it requires > 5)
                break
        return row_final

    def get_daily_shuffled_favorites():
        """Get top rated movies shuffled deterministically by current day to prevent daily duplicate rotation."""
        import random
        from datetime import date
        top_movies = tmdb.get_top_rated_movies(limit=40)
        if not top_movies:
            return []
        today = date.today().toordinal()
        rng = random.Random(today)
        shuffled = list(top_movies)
        rng.shuffle(shuffled)
        return shuffled

    render_movie_row("Just Arrived on OTT", prioritize_movies(tmdb.get_recent_ott_movies(limit=40)), "recent_ott", "recent_ott")
    render_movie_row("All-Time Favorites", prioritize_movies(get_daily_shuffled_favorites()), "fav", "all_time")
    render_movie_row("Trending Indian Movies", prioritize_movies(tmdb.get_trending_indian(limit=40)), "ind", "trending_indian")
    render_movie_row("Trending Telugu OTT Movies", prioritize_movies(tmdb.get_trending_by_language("te", limit=40)), "te", "trending_te")
    render_movie_row("Trending Hindi OTT Movies", prioritize_movies(tmdb.get_trending_by_language("hi", limit=40)), "hi", "trending_hi")
    render_movie_row("Trending Tamil OTT Movies", prioritize_movies(tmdb.get_trending_by_language("ta", limit=40)), "ta", "trending_ta")
    render_movie_row("Trending Kannada OTT Movies", prioritize_movies(tmdb.get_trending_by_language("kn", limit=40)), "kn", "trending_kn")
    render_movie_row("Trending Malayalam OTT Movies", prioritize_movies(tmdb.get_trending_by_language("ml", limit=40)), "ml", "trending_ml")
    
    # Other Languages
    other_movies = tmdb.get_other_languages_ott(limit=40)
    render_movie_row("Trending Other Languages OTT Movies", prioritize_movies(other_movies), "other", "other_lang")

    # Footer
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