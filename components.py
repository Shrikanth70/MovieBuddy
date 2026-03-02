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
        --bg-dark: #0E1117;
        --bg-card: #1C212B;
        --gold: #E6B35A;
        --gold-white: linear-gradient(135deg, #E6B35A 0%, #FFFFFF 50%, #E6B35A 100%);
        --gold-glow: rgba(230, 179, 90, 0.4);
        --text-main: #FFFFFF;
        --text-muted: #8B949E;
        --radius-lg: 20px;
        --radius-md: 14px;
        --transition: 400ms cubic-bezier(0.16, 1, 0.3, 1);
        --font-main: 'Poppins', sans-serif;
    }

    * { font-family: var(--font-main); }

    /* Hide Sidebar toggle and sidebar itself */
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-main);
    }

    /* Hide Streamlit default elements */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}

    /* Background Texture */
    .bg-texture {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(circle at 50% 50%, rgba(230, 179, 90, 0.05) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
    }

    /* Hero Section */
    .hero {
        position: relative;
        height: 500px;
        border-radius: var(--radius-lg);
        background-size: cover;
        background-position: center 20%;
        margin-bottom: 40px;
        overflow: hidden;
        display: flex;
        align-items: flex-end;
        padding: 60px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .hero::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(0deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.6) 50%, rgba(14,17,23,0) 100%);
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 16px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    /* Movie Cards */
    .movie-card {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        overflow: hidden;
        transition: var(--transition);
        cursor: pointer;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 15px;
        position: relative;
    }

    .movie-card:hover {
        transform: translateY(-10px);
        border-color: var(--gold);
        box-shadow: 0 15px 35px rgba(0,0,0,0.6), 0 0 20px var(--gold-glow);
    }

    .card-img {
        width: 100%;
        aspect-ratio: 2/3;
        object-fit: cover;
    }

    .card-info {
        padding: 15px;
    }

    .card-title {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: var(--text-main);
    }

    .card-meta {
        font-size: 13px;
        color: var(--text-muted);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .rating { color: var(--gold); font-weight: 700; display: flex; align-items: center; gap: 4px; }

    /* Premium Text Logo Styling */
    .logo-link {
        text-decoration: none !important;
        display: inline-block;
        transition: var(--transition);
        margin-bottom: 5px;
        font-family: 'Poppins', sans-serif;
    }

    .logo-text {
        font-size: 40px;
        font-weight: 800;
        letter-spacing: 1.02px;
        line-height: 1;
        cursor: pointer;
        display: block;
    }

    .logo-movie { color: #FFAA00; }
    .logo-buddy { color: #FFFFFF; }

    .logo-link:hover {
        transform: scale(1.03);
        filter: drop-shadow(0 0 15px rgba(230, 179, 90, 0.3));
    }

    /* Search Input Styling */
    .stTextInput input {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 20px !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 10px var(--gold-glow) !important;
    }

    .gold-text { color: var(--gold); }
    </style>
    """, unsafe_allow_html=True)

def render_slideshow(movie, image_url):
    """Render a single slide for the trending movies slideshow."""
    if not movie:
        return
    
    title = movie.get("title")
    year = movie.get("release_date", "N/A")[:4]
    overview = movie.get("overview", "")
    rating = movie.get("vote_average", "N/A")
    
    if image_url == "placeholder.png":
        b64_img = get_base64_image("placeholder.png")
        image_url = f"data:image/png;base64,{b64_img}"
    
    st.markdown(f"""
    <div class="hero" style="background-image: url('{image_url}');">
        <div class="hero-content">
            <div class="hero-title">{title}</div>
            <div style="color: var(--gold); font-size: 18px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;">
                <span>{year}</span>
                <span style="color: rgba(255,255,255,0.4);">|</span>
                <span class="rating">⭐ {rating}</span>
                <span style="color: rgba(255,255,255,0.4);">|</span>
                <span style="color: var(--text-muted); font-weight: 400;">Trending This Week</span>
            </div>
            <p style="color: rgba(255,255,255,0.9); font-size: 14px; line-height: 1.6; margin-bottom: 24px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; max-width: 650px;">
                {overview}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_movie_card(movie, poster_url):
    """Helper for internal markdown movie card markup."""
    title = movie.get("title")
    year = movie.get("release_date", "N/A")[:4]
    rating = round(movie.get("vote_average", 0), 1)
    
    if poster_url == "placeholder.png":
        b64_img = get_base64_image("placeholder.png")
        poster_url = f"data:image/png;base64,{b64_img}"
        
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
