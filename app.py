import streamlit as st
import tmdb_service as tmdb
import components as ui
import supabase_service as auth
import time
import recommendation as rec_engine
import datetime
import random

# Set page config
st.set_page_config(
    page_title="MovieBuddy | Premium Streaming",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS
ui.inject_custom_css()

# --- Session State Initialization ---
if "user" not in st.session_state:
    st.session_state.user = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"
if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None

# --- Auth Gate ---
def show_auth():
    # Use two main columns to match the reference design (Part 4)
    l, r = st.columns([1, 1], gap="large")
    
    with l:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1A4D2E 0%, #07090D 100%); padding: 4rem; border-radius: 30px; height: 800px; display: flex; flex-direction: column; justify-content: center; position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); margin-top: 50px;">
                <div style="font-size: 32px; font-weight: 800; color: #FFB000; margin-bottom: 2rem;">MovieBuddy</div>
                <h1 style="font-size: 48px; color: white; margin-bottom: 1.5rem; line-height: 1.1;">Get started with us</h1>
                <p style="color: rgba(255,255,255,0.7); margin-bottom: 3rem; font-size: 16px;">Complete these easy steps to register your account and start your cinematic journey.</p>
                
                <div style="display: flex; flex-direction: column; gap: 20px;">
                    <div style="display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="font-size: 24px;">✎</span>
                        <div>
                            <div style="font-weight: 700; color: white;">Sign up your account</div>
                            <div style="font-size: 13px; color: rgba(255,255,255,0.5);">Create your profile in seconds</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="font-size: 24px;">🔍</span>
                        <div>
                            <div style="font-weight: 700; color: white;">Discover movies</div>
                            <div style="font-size: 13px; color: rgba(255,255,255,0.5);">Get AI-powered recommendations</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="font-size: 24px;">🎬</span>
                        <div>
                            <div style="font-weight: 700; color: white;">Start watching</div>
                            <div style="font-size: 13px; color: rgba(255,255,255,0.5);">Personalize your experience</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with r:
        st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True) # Spacer
        container = st.container()
        with container:
            # Check for verification return
            if st.query_params.get("code"):
                st.success("✅ Email verified successfully! Please log in to continue.")
                st.query_params.clear()

            title_text = "Sign in to MovieBuddy" if st.session_state.get("auth_mode", "Login") == "Login" else "Create your account"
            st.markdown(f'<h2 style="text-align: center; font-size: 32px; margin-bottom: 30px;">{title_text}</h2>', unsafe_allow_html=True)
            
            # Message for post-signup
            if st.session_state.get("signup_success"):
                st.info("📩 Account created! Please check your email and click the verification link before logging in.")
                if st.button("Back to Login", use_container_width=True):
                    st.session_state.signup_success = False
                    st.session_state.auth_mode = "Login"
                    st.rerun()
                return

            auth_mode = st.radio("Mode", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed", key="auth_mode_selector")
            st.session_state["auth_mode"] = auth_mode
            
            email = st.text_input("Email Address", placeholder="Enter your email", key="auth_email")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="auth_password")
            
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            
            if auth_mode == "Login":
                if st.button("Sign In", use_container_width=True, type="primary"):
                    if not email or not password:
                        st.warning("Please enter both email and password.")
                    else:
                        with st.spinner("Authenticating..."):
                            res, err = auth.sign_in(email, password)
                            if err:
                                if "Email not confirmed" in err:
                                    st.error("❌ Your email is not verified yet. Please check your inbox.")
                                elif "Invalid login credentials" in err:
                                    st.error("❌ Invalid email or password.")
                                else:
                                    st.error(f"Error: {err}")
                            else:
                                st.session_state.user = res.user
                                st.rerun()
                st.markdown('<div style="text-align: center; color: var(--text-muted); font-size: 14px; margin-top: 20px;">Or continue with Google (Coming Soon)</div>', unsafe_allow_html=True)
            else:
                if st.button("Create Account", use_container_width=True, type="primary"):
                    if not email or not password:
                        st.warning("Please provide email and password for signup.")
                    else:
                        with st.spinner("Creating account..."):
                            res, err = auth.sign_up(email, password)
                            if err: st.error(f"Error: {err}")
                            else:
                                st.session_state.signup_success = True
                                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --- Content Renderers ---

def render_movie_grid(movies, key_prefix="grid", cols_per_row=5):
    if not movies:
        st.warning("No movies found.")
        return
        
    for row in range(0, len(movies), cols_per_row):
        cols = st.columns(cols_per_row)
        for idx, movie in enumerate(movies[row:row+cols_per_row]):
            with cols[idx]:
                poster_url = tmdb.get_image_url(movie.get("poster_path"))
                st.markdown(ui.render_movie_card(movie, poster_url), unsafe_allow_html=True)
                if st.button("View Details", key=f"{key_prefix}_{movie.get('id')}_{row}_{idx}", use_container_width=True):
                    st.session_state.selected_movie_id = movie.get("id")
                    st.rerun()

def render_detail_view(movie_id):
    # Fix: Inline JS Scroll Reset (Streamlit Cloud Compatible)
    st.markdown("""<script>window.parent.window.scrollTo({top: 0, behavior: "smooth"});</script>""", unsafe_allow_html=True)
    
    if st.button("❮ Back"):
        st.session_state.selected_movie_id = None
        st.rerun()

    with st.spinner("Loading movie details..."):
        movie = tmdb.get_movie_details(movie_id)
        trailers = tmdb.get_movie_videos(movie_id)
        imdb_id = tmdb.get_imdb_id(movie_id)
        omdb_data = tmdb.get_omdb_data(imdb_id) if imdb_id else None
        
        # Recommendations
        recommendations = tmdb.get_movie_recommendations(movie_id, limit=8)
    
    if not movie:
        st.error("Could not load movie details.")
        return

    # Detail Content
    backdrop_url = tmdb.get_image_url(movie.get("backdrop_path"), size="original")
    ui.render_detail_hero(movie, backdrop_url)

    # Watchlist Action
    is_saved = auth.is_in_watchlist(st.session_state.user.id, movie_id)
    btn_label = "❤️ In Watchlist" if is_saved else "➕ Add to Watchlist"
    if st.button(btn_label, use_container_width=True):
        if is_saved:
            auth.remove_from_watchlist(st.session_state.user.id, movie_id)
        else:
            auth.add_to_watchlist(st.session_state.user.id, movie)
        st.rerun()

    # OMDb Ratings
    if omdb_data and omdb_data.get("Response") == "True":
        st.markdown('<h3 class="gold-text">Movie Insights</h3>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("IMDb Rating", omdb_data.get("imdbRating", "N/A"))
        with c2: st.metric("Awards", omdb_data.get("Awards", "N/A"))
        with c3: st.metric("Box Office", omdb_data.get("BoxOffice", "N/A"))
    
    # Trailer
    if trailers:
        st.markdown("### Official Trailer")
        st.video(f"https://www.youtube.com/watch?{trailers[0].get('key')}")

    st.markdown("### You Might Also Like")
    render_movie_grid(recommendations, key_prefix="detail_rec", cols_per_row=4)

def render_home_page():
    # Hero Banner (Trending Daily #1)
    daily_trending = tmdb.get_trending_daily(limit=20)
    if daily_trending:
        hero_movie = daily_trending[0]
        backdrop_url = tmdb.get_image_url(hero_movie.get("backdrop_path"), size="original")
        ui.render_hero_banner(hero_movie, backdrop_url)
        if st.button("▶ WATCH NOW", key="hero_watch", use_container_width=True):
            st.session_state.selected_movie_id = hero_movie.get("id")
            st.rerun()

    # Trending Now Carousel (Part 5)
    st.markdown('<h2 style="margin: 40px 0 20px 0;">Trending <span class="gold-text">Now</span></h2>', unsafe_allow_html=True)
    ui.render_carousel(daily_trending[1:11], tmdb, key_prefix="home_trending")

    # Top Rated Section
    st.markdown('<h2 style="margin: 40px 0 20px 0;">Top <span class="gold-text">Rated</span></h2>', unsafe_allow_html=True)
    top_rated = tmdb.get_top_rated_movies(limit=10)
    render_movie_grid(top_rated, key_prefix="home_top", cols_per_row=5)

def render_watchlist():
    st.markdown('<h1>My <span class="gold-text">Watchlist</span></h1>', unsafe_allow_html=True)
    items, err = auth.get_watchlist(st.session_state.user.id)
    if err: st.error(err)
    elif not items:
        st.info("Your watchlist is empty. Start adding some movies!")
    else:
        render_movie_grid(items, key_prefix="watchlist_grid")

# --- Main Logic ---
def main():
    if not st.session_state.user:
        show_auth()
        return

    # Sidebar Navigation
    ui.render_sidebar(user_email=st.session_state.user.email)

    # Main Content Area
    # If a movie is selected, show details regardless of current page
    if st.session_state.selected_movie_id:
        render_detail_view(st.session_state.selected_movie_id)
        return

    # Routing
    page = st.session_state.active_page
    if page == "Home":
        render_home_page()
    elif page == "Watchlist":
        render_watchlist()
    elif page == "Trending":
        st.markdown('<h1>Trending <span class="gold-text">Movies</span></h1>', unsafe_allow_html=True)
        trending = tmdb.get_trending_weekly(limit=20)
        render_movie_grid(trending, key_prefix="trending_page")
    else:
        st.title(f"{page} Coming Soon")

if __name__ == "__main__":
    main()
