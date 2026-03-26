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
    """Render a premium horizontal scrollable row with native clickable overlays."""
    if not movies:
        return
        
    st.markdown(f'<h3 style="margin-top: 30px; margin-bottom: 15px;">{title}</h3>', unsafe_allow_html=True)
    cols = st.columns(6, gap="small")
    
    # Show up to 5 movies
    for idx, movie in enumerate(movies[:5]):
        with cols[idx]:
            poster_url = tmdb.get_image_url(movie.get("poster_path"))
            # The card itself
            st.markdown(f'<div class="native-card-wrapper">{ui.render_movie_card(movie, poster_url)}<div class="card-btn-container">', unsafe_allow_html=True)
            # The invisible overlay button
            if st.button("\u00A0", key=f"nav_{key_prefix}_{movie['id']}_{idx}", help=""):
                st.query_params.movie_id = movie['id']
                st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)
                
    # See More card
    if category_id and len(movies) >= 6:
        with cols[5]:
            st.markdown(f'<div class="native-card-wrapper">{ui.render_see_more_card()}<div class="card-btn-container">', unsafe_allow_html=True)
            if st.button("\u00A0", key=f"see_{key_prefix}_{category_id}", help=""):
                st.query_params.category_id = category_id
                st.query_params.title = title
                st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

def render_detail_view(movie_id):
    # Persistent Top Header
    head_col1, head_col2 = st.columns([4, 2], gap="large")
    with head_col1:
        st.markdown(f'''
            <a href="/?home=true" target="_self" class="logo-link">
                <span class="logo-text"><span class="logo-movie">Movie</span><span class="logo-buddy">Buddy</span></span>
            </a>
        ''', unsafe_allow_html=True)
    with head_col2:
        search_query = st.text_input("Search", placeholder="Search movies, actors, genres...", key="detail_search_input", label_visibility="collapsed")

    if search_query:
        # Search Results
        st.markdown(f'<h2>Search Results for <span class="gold-text">"{search_query}"</span></h2>', unsafe_allow_html=True)
        results = tmdb.search_movies(search_query)
        if results:
            for row in range(0, len(results), 5):
                cols = st.columns(5)
                for idx, movie in enumerate(results[row:row+5]):
                    with cols[idx]:
                        st.markdown('<div class="native-card-wrapper">', unsafe_allow_html=True)
                        st.markdown(ui.render_movie_card(movie, tmdb.get_image_url(movie.get("poster_path"))), unsafe_allow_html=True)
                        if st.button("\u00A0", key=f"detail_search_nav_{movie['id']}_{row}_{idx}", help=""):
                            st.query_params.movie_id = movie['id']
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No movies found.")
        return

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
        
        # Cast display using Streamlit columns
        if cast:
            cast_cols = st.columns(min(len(cast), 8))
            for i, actor in enumerate(cast[:8]):
                with cast_cols[i]:
                    profile_path = actor.get("profile_path")
                    img = f"https://image.tmdb.org/t/p/w185{profile_path}" if profile_path else "https://via.placeholder.com/100x150?text=No+Photo"
                    st.image(img, width=100)
                    st.markdown(f"<div style='text-align: center; font-size: 13px; font-weight: 700; color: white; margin-bottom: 5px;'>{actor.get('name', 'Unknown')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; font-size: 11px; color: #8B949E;'>{actor.get('character', 'Actor')}</div>", unsafe_allow_html=True)
        
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
    # Persistent Top Header
    head_col1, head_col2 = st.columns([4, 2], gap="large")
    with head_col1:
        st.markdown(f'''
            <a href="/?home=true" target="_self" class="logo-link">
                <span class="logo-text"><span class="logo-movie">Movie</span><span class="logo-buddy">Buddy</span></span>
            </a>
        ''', unsafe_allow_html=True)
    with head_col2:
        search_query = st.text_input("Search", placeholder="Search movies, actors, genres...", key="category_search_input", label_visibility="collapsed")

    if search_query:
        # Search Results
        st.markdown(f'<h2>Search Results for <span class="gold-text">"{search_query}"</span></h2>', unsafe_allow_html=True)
        results = tmdb.search_movies(search_query)
        if results:
            for row in range(0, len(results), 5):
                cols = st.columns(5)
                for idx, movie in enumerate(results[row:row+5]):
                    with cols[idx]:
                        st.markdown('<div class="native-card-wrapper">', unsafe_allow_html=True)
                        st.markdown(ui.render_movie_card(movie, tmdb.get_image_url(movie.get("poster_path"))), unsafe_allow_html=True)
                        if st.button("\u00A0", key=f"category_search_nav_{movie['id']}_{row}_{idx}", help=""):
                            st.query_params.movie_id = movie['id']
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No movies found.")
        return

    col_back, _ = st.columns([1.5, 8.5])
    with col_back:
        st.markdown('<div class="back-btn-col">', unsafe_allow_html=True)
        if st.button("← Back", key=f"back_{category_id}"):
            st.query_params.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
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
                st.markdown(f'<div class="native-card-wrapper">{ui.render_movie_card(movie, poster_url)}<div class="card-btn-container">', unsafe_allow_html=True)
                if st.button("\u00A0", key=f"grid_{category_id}_{movie['id']}_{row}_{idx}", help=""):
                    st.query_params.movie_id = movie['id']
                    st.rerun()
                st.markdown('</div></div>', unsafe_allow_html=True)

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

    # --- ROUTING ENGINE ---
    params = st.query_params
    
    if "movie_id" in params:
        m_id = params["movie_id"]
        if isinstance(m_id, list): m_id = m_id[0]
        render_detail_view(int(m_id))
        return

    if "category_id" in params:
        cat_id = params["category_id"]
        if isinstance(cat_id, list): cat_id = cat_id[0]
        cat_title = params.get("title", "Category")
        if isinstance(cat_title, list): cat_title = cat_title[0]
        render_category_view(cat_id, cat_title)
        return

    # Persistent Top Header with better balance
    head_col1, head_col2 = st.columns([4, 2], gap="large")
    with head_col1:
        st.markdown(f'''
            <a href="/?home=true" target="_self" class="logo-link">
                <span class="logo-text"><span class="logo-movie">Movie</span><span class="logo-buddy">Buddy</span></span>
            </a>
        ''', unsafe_allow_html=True)
    with head_col2:
        search_query = st.text_input("Search", placeholder="Search movies, actors, genres...", key="movie_search_input", label_visibility="collapsed")

    if search_query:
        # Search Results
        st.markdown(f'<h2>Search Results for <span class="gold-text">"{search_query}"</span></h2>', unsafe_allow_html=True)
        results = tmdb.search_movies(search_query)
        if results:
            for row in range(0, len(results), 5):
                cols = st.columns(5)
                for idx, movie in enumerate(results[row:row+5]):
                    with cols[idx]:
                        st.markdown('<div class="native-card-wrapper">', unsafe_allow_html=True)
                        st.markdown(ui.render_movie_card(movie, tmdb.get_image_url(movie.get("poster_path"))), unsafe_allow_html=True)
                        if st.button("\u00A0", key=f"search_nav_{movie['id']}_{row}_{idx}", help=""):
                            st.query_params.movie_id = movie['id']
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No movies found.")
        return

    # ------------ HOME PAGE FEATURED (Native) ------------
    if "hero_index" not in st.session_state:
        st.session_state.hero_index = 0
        
    if "hero_slides" not in st.session_state or not st.session_state.hero_slides:
        st.session_state.hero_slides = tmdb.get_now_playing_movies(limit=10) or tmdb.get_trending_weekly(limit=10)

    if st.session_state.hero_slides:
        # Use premium improved slideshow with native-safe parent navigation
        ui.render_slideshow(st.session_state.hero_slides)
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    # Netflix-Style Rows

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