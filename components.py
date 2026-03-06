import base64
import os
import streamlit as st

@st.cache_data
def get_base64_image(image_path):
    """Convert local image to base64 string for HTML embedding."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def inject_custom_css():
    """Inject premium cinematic CSS into Streamlit."""
    # Import Poppins font
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Montserrat:wght@400;700;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    :root {
        --bg-dark: #07090D;
        --bg-card: #12161F;
        --bg-sidebar: #0D1117;
        --gold: #FFB000;
        --green: #2ECC71;
        --gold-glow: rgba(255, 176, 0, 0.3);
        --green-glow: rgba(46, 204, 113, 0.3);
        --text-main: #FFFFFF;
        --text-muted: #8B949E;
        --radius-lg: 20px;
        --radius-md: 14px;
        --transition: 400ms cubic-bezier(0.16, 1, 0.3, 1);
        --font-main: 'Poppins', sans-serif;
    }

    * { font-family: var(--font-main); }

    /* Hide Streamlit default elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-main);
    }
    .block-container {padding-top: 0rem; padding-bottom: 2rem; max-width: 100% !important;}

    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    .sidebar-logo {
        padding: 2rem 1.5rem;
        font-size: 24px;
        font-weight: 800;
        color: var(--gold);
        letter-spacing: 1px;
    }

    .nav-item {
        padding: 12px 20px;
        margin: 4px 15px;
        border-radius: 12px;
        cursor: pointer;
        transition: var(--transition);
        display: flex;
        align-items: center;
        gap: 12px;
        color: var(--text-muted);
        text-decoration: none;
    }

    .nav-item:hover, .nav-item.active {
        background: rgba(255, 176, 0, 0.1);
        color: var(--gold);
    }
    
    .nav-item.active {
        border-left: 3px solid var(--gold);
    }

    /* Auth Page Styling */
    .auth-container {
        display: flex;
        height: 100vh;
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        background: var(--bg-dark);
    }

    .auth-left {
        flex: 1;
        background: linear-gradient(135deg, #1A4D2E 0%, #07090D 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 4rem;
        position: relative;
        overflow: hidden;
    }

    .auth-left::after {
        content: '🎬';
        position: absolute;
        top: -50px;
        right: -50px;
        font-size: 300px;
        opacity: 0.05;
        transform: rotate(15deg);
    }

    .auth-right {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }

    .auth-card {
        width: 100%;
        max-width: 450px;
        background: var(--bg-card);
        padding: 3rem;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    /* Hero Banner Redesign */
    .hero-banner {
        position: relative;
        width: 100%;
        height: 600px;
        background-size: cover;
        background-position: center 20%;
        border-radius: 30px;
        overflow: hidden;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        padding: 0 60px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .hero-banner::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(7,9,13,0.9) 0%, rgba(7,9,13,0.5) 50%, rgba(7,9,13,0) 100%);
    }

    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 600px;
    }

    .hero-title {
        font-size: 64px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 20px;
    }

    /* Detail Hero */
    .hero {
        position: relative;
        height: 550px;
        border-radius: 30px;
        background-size: cover;
        background-position: center 20%;
        margin-bottom: 40px;
        overflow: hidden;
        display: flex;
        align-items: center;
        padding: 0 60px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .hero::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(0deg, rgba(7,9,13,1) 0%, rgba(7,9,13,0.7) 50%, rgba(7,9,13,0.3) 100%);
    }

    /* Movie Carousel Styling */
    .carousel-container {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 10px 5px 30px 5px;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    .carousel-container::-webkit-scrollbar { display: none; }

    .carousel-item {
        min-width: 200px;
        flex: 0 0 auto;
    }

    /* Movie Cards */
    .movie-card {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        overflow: hidden;
        transition: var(--transition);
        border: 1px solid rgba(255,255,255,0.05);
        min-width: 220px;
        position: relative;
    }

    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: var(--gold);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px var(--gold-glow);
    }

    .card-img {
        width: 100%;
        aspect-ratio: 2/3;
        object-fit: cover;
    }

    .card-info { padding: 15px; }
    .card-title { font-size: 15px; font-weight: 700; margin-bottom: 6px; color: var(--text-main); }
    .card-meta { font-size: 13px; color: var(--text-muted); display: flex; justify-content: space-between; }
    .rating { color: var(--gold); font-weight: 700; }

    /* Button Styling */
    div.stButton > button {
        background: var(--gold) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div.stButton > button:hover {
        background: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def render_auth_page():
    """Render the premium modern authentication page."""
    st.markdown("""
        <div class="auth-container">
            <div class="auth-left">
                <div style="font-size: 32px; font-weight: 800; color: #FFB000; margin-bottom: 2rem;">MovieBuddy</div>
                <h1 style="font-size: 48px; color: white; margin-bottom: 2rem;">Get started with us</h1>
                <p style="color: rgba(255,255,255,0.7); margin-bottom: 3rem;">Complete these easy steps to register your account and start your cinematic journey.</p>
                
                <div style="display: flex; flex-direction: column; gap: 20px;">
                    <div style="display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px;">
                        <span style="font-size: 24px;">✎</span>
                        <div>
                            <div style="font-weight: 700;">Sign up your account</div>
                            <div style="font-size: 13px; color: rgba(255,255,255,0.5);">Create your profile in seconds</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px;">
                        <span style="font-size: 24px;">🔍</span>
                        <div>
                            <div style="font-weight: 700;">Discover movies</div>
                            <div style="font-size: 13px; color: rgba(255,255,255,0.5);">Get AI-powered recommendations</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px;">
                        <span style="font-size: 24px;">🎬</span>
                        <div>
                            <div style="font-weight: 700;">Start watching</div>
                            <div style="font-size: 13px; color: rgba(255,255,255,0.5);">Personalize your experience</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="auth-right">
                <div id="auth-form-container"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar(user_email=None):
    """Render the vertical sidebar navigation."""
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">MovieBuddy</div>', unsafe_allow_html=True)
        
        # Navigation items
        pages = {
            "Home": "🏠",
            "Trending": "🔥",
            "Genres": "🎭",
            "Watchlist": "❤️",
            "Recently Viewed": "🕒"
        }
        
        selection = None
        for page, icon in pages.items():
            if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True):
                st.session_state.active_page = page
                st.rerun()
        
        st.markdown('<div style="margin-top: auto; padding: 20px;">', unsafe_allow_html=True)
        if user_email:
            st.markdown(f'<div style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px;">👤 {user_email}</div>', unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_hero_banner(movie, backdrop_url):
    """Render the redesigned widescreen hero banner."""
    title = movie.get("title")
    year = movie.get("release_date", "N/A")[:4]
    overview = movie.get("overview", "")
    rating = movie.get("vote_average", "N/A")
    
    st.markdown(f"""
    <div class="hero-banner" style="background-image: url('{backdrop_url}');">
        <div class="hero-content">
            <h1 class="hero-title">{title}</h1>
            <div style="color: var(--gold); font-size: 18px; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 15px;">
                <span>{year}</span>
                <span style="color: rgba(255,255,255,0.3);">|</span>
                <span>⭐ {rating}</span>
                <span style="color: rgba(255,255,255,0.3);">|</span>
                <span style="color: var(--text-muted); font-weight: 400;">Featured Recommendation</span>
            </div>
            <p style="color: rgba(255,255,255,0.8); font-size: 15px; line-height: 1.6; margin-bottom: 30px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">
                {overview}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_movie_card(movie, poster_url):
    """Update movie card for the new grid/carousel look."""
    title = movie.get("title")
    year = movie.get("release_date", "N/A")[:4]
    rating = round(movie.get("vote_average", 0), 1)
    
    return f"""
    <div class="movie-card">
        <img src="{poster_url}" class="card-img">
        <div class="card-info">
            <div class="card-title">{title}</div>
            <div class="card-meta">
                <span>{year}</span>
                <span class="rating">★ {rating}</span>
            </div>
        </div>
    </div>
    """
    
def render_carousel(movies, tmdb_helper, key_prefix="carousel"):
    """Render a horizontal movie carousel using HTML/CSS."""
    if not movies:
        return
        
    html = '<div class="carousel-container">'
    for movie in movies:
        poster_url = tmdb_helper.get_image_url(movie.get("poster_path"))
        title = movie.get("title")
        rating = round(movie.get("vote_average", 0), 1)
        
        # We need a way to make these clickable. In Streamlit, we'll use a button below for now
        # OR we can inject a script to handle clicks if we have a way to pass the ID back.
        # For pure Streamlit, a horizontal scroll with st.columns is hard, so we'll use this for visual
        # and standard columns for interaction, OR just use st.columns with a scrollbar container.
        html += f'''
        <div class="carousel-item">
            <div class="movie-card">
                <img src="{poster_url}" class="card-img">
                <div class="card-info">
                    <div class="card-title">{title}</div>
                    <div class="card-meta">
                        <span class="rating">★ {rating}</span>
                    </div>
                </div>
            </div>
        </div>
        '''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    
    # Interaction: Individual detail buttons below for the carousel items
    # (Since JS callbacks to Streamlit are complex without components)
    cols = st.columns(len(movies))
    for idx, movie in enumerate(movies):
        with cols[idx]:
            if st.button("Details", key=f"{key_prefix}_{movie.get('id')}_{idx}", use_container_width=True):
                st.session_state.selected_movie_id = movie.get("id")
                st.rerun()

def render_detail_hero(movie, backdrop_url):
    """Render the high-impact movie detail hero."""
    title = movie.get("title")
    year = movie.get("release_date", "N/A")[:4]
    rating = round(movie.get("vote_average", 0), 1)
    runtime = f"{movie.get('runtime', 'N/A')} min"
    genres = ", ".join([g.get("name") for g in movie.get("genres", [])])
    overview = movie.get("overview", "")
    
    if backdrop_url == "placeholder.png":
        b64_img = get_base64_image("placeholder.png")
        backdrop_url = f"data:image/png;base64,{b64_img}"
        
    st.markdown(f"""
    <div class="hero" style="height: 550px; background-image: url('{backdrop_url}'); background-position: top center;">
        <div class="hero-content" style="max-width: 900px;">
            <div class="hero-title" style="font-size: 56px;">{title}</div>
            <div style="color: var(--gold); font-weight: 700; margin-bottom: 12px; font-size: 18px; display: flex; align-items: center; gap: 15px;">
                <span>{year}</span>
                <span style="color: rgba(255,255,255,0.4);">|</span>
                <span>{runtime}</span>
                <span style="color: rgba(255,255,255,0.4);">|</span>
                <span class="rating">⭐ {rating}</span>
            </div>
            <div style="color: var(--text-muted); font-size: 15px; margin-bottom: 30px;">
                {genres}
            </div>
            <h3 style="color: var(--text-main); font-size: 22px; margin-bottom: 15px;">Synopsis</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 16px; line-height: 1.8; margin-bottom: 32px;">
                {overview}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_watch_providers(providers):
    """Render streaming availability logos."""
    if not providers:
        st.markdown('<div class="ott-container"><div class="ott-title">Streaming Info</div><div style="color: var(--text-muted);">Not available in your region.</div></div>', unsafe_allow_html=True)
        return

    # Categories: flatrate (Stream), buy, rent
    categories = [
        ("Stream", providers.get("flatrate", [])),
        ("Rent", providers.get("rent", [])),
        ("Buy", providers.get("buy", []))
    ]

    html_output = '<div class="ott-container">'
    html_output += '<div class="ott-title">Where to Watch</div>'
    
    found_any = False
    for label, items in categories:
        if items:
            found_any = True
            html_output += f'<div style="font-size: 13px; color: var(--text-muted); margin-bottom: 8px;">{label}</div>'
            html_output += '<div class="provider-grid">'
            for item in items:
                logo_url = f"https://image.tmdb.org/t/p/original{item.get('logo_path')}"
                name = item.get("provider_name")
                html_output += f'<img src="{logo_url}" title="{name}" class="provider-logo">'
            html_output += '</div><div style="height: 15px;"></div>'
    
    if not found_any:
        html_output += '<div style="color: var(--text-muted);">Streaming info not available.</div>'
    
    html_output += '</div>'
    st.markdown(html_output, unsafe_allow_html=True)
