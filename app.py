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
    """Render a 6-column grid of movies with a See More button as the 6th card."""
    if not movies:
        return
        
    st.markdown(f'<h3 style="margin-top: 30px; margin-bottom: 15px;">{title}</h3>', unsafe_allow_html=True)
    
    # Always create 6 columns for consistency (5 movies + 1 see more)
    cols = st.columns(6)
    
    # Render up to 5 movies
    for idx, movie in enumerate(movies[:5]):
        with cols[idx]:
            poster_url = tmdb.get_image_url(movie.get("poster_path"))
            st.markdown(ui.render_movie_card(movie, poster_url), unsafe_allow_html=True)
            if st.button("View Details", key=f"{key_prefix}_btn_{movie.get('id')}", use_container_width=True):
                navigate_to("details", movie_id=movie.get("id"))
                
    with cols[5]:
        st.markdown(ui.render_see_more_card(), unsafe_allow_html=True)
        if st.button("See More", key=f"{key_prefix}_seemore", use_container_width=True):
            navigate_to("category", category_id=category_id, title=title)

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
        providers = tmdb.get_watch_providers(movie_id)
        ui.render_watch_providers(providers)
            
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
        elif category_id == "trending_en":
            movies = tmdb.get_trending_by_language("en", limit=40)
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
                if st.button("View Details", key=f"cat_{movie.get('id')}_{row}_{idx}", use_container_width=True):
                    navigate_to("details", movie_id=movie.get("id"))

# --- Main Layout ---
def main():
    # Always-on scroll-to-top fix: fires on every page load and navigation
    st.components.v1.html("""
    <script>
    function scrollToTop() {
        // Target the Streamlit main container
        var main = window.parent.document.querySelector('section.main');
        if (main) main.scrollTop = 0;
        // Also scroll the parent window itself
        window.parent.scrollTo(0, 0);
        // Target the block-container as well
        var block = window.parent.document.querySelector('.block-container');
        if (block) block.scrollTop = 0;
    }
    // Fire immediately
    scrollToTop();
    // Fire again after short delays to catch late renders
    setTimeout(scrollToTop, 50);
    setTimeout(scrollToTop, 150);
    setTimeout(scrollToTop, 300);
    </script>
    """, height=0)

    if "page_stack" not in st.session_state:
        st.session_state.page_stack = [{"page": "home"}]

    if st.query_params.get("home") == "true":
        st.session_state.page_stack = [{"page": "home"}]
        if "last_search" in st.session_state:
            del st.session_state["last_search"]
        st.query_params.clear()
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
                        if st.button("View Details", key=f"src_{movie.get('id')}_{row}_{idx}", use_container_width=True):
                            navigate_to("details", movie_id=movie.get("id"))
        else:
            st.warning("No results found.")
            if st.button("⬅ Back Home"):
                navigate_to("home")
        return

    # ------------ HOME PAGE ------------
    if "hero_slides" not in st.session_state or not st.session_state.hero_slides:
        slides = tmdb.get_now_playing_movies(limit=10)
        
        # Fallback to general trending if now_playing fails or is empty
        if not slides:
            slides = tmdb.get_trending_weekly(limit=10)
            
        st.session_state.hero_slides = slides

    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0

    if st.session_state.hero_slides:
        current_slide = st.session_state.hero_slides[st.session_state.slide_index]
        backdrop_url = tmdb.get_image_url(current_slide.get("backdrop_path"), size="original")
        ui.render_slideshow(current_slide, backdrop_url)
        
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1, 8])
        with ctrl_col1:
            if st.button("❮ ", use_container_width=True):
                st.session_state.slide_index = (st.session_state.slide_index - 1) % len(st.session_state.hero_slides)
                st.rerun()
        with ctrl_col2:
            if st.button(" ❯", use_container_width=True):
                st.session_state.slide_index = (st.session_state.slide_index + 1) % len(st.session_state.hero_slides)
                st.rerun()
        with ctrl_col3:
            if st.button(" ▶View Details", key=f"hero_watch_{current_slide.get('id')}"):
                navigate_to("details", movie_id=current_slide.get("id"))

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

    render_movie_row("Just Arrived on OTT", prioritize_movies(tmdb.get_recent_ott_movies(limit=40)), "recent_ott", "recent_ott")
    render_movie_row("Trending Telugu OTT Movies", prioritize_movies(tmdb.get_trending_by_language("te", limit=40)), "te", "trending_te")
    render_movie_row("Trending Hindi OTT Movies", prioritize_movies(tmdb.get_trending_by_language("hi", limit=40)), "hi", "trending_hi")
    render_movie_row("Trending English OTT Movies", prioritize_movies(tmdb.get_trending_by_language("en", limit=40)), "en", "trending_en")
    
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