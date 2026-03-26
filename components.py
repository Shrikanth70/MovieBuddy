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
    .block-container {
        padding-top: 1rem; 
        padding-bottom: 2rem;
        max-width: 1400px !important;
        margin: auto !important;
    }

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

    /* Horizontal Movie Row */
    .movie-row-container {
        display: flex;
        overflow-x: auto;
        gap: 15px;
        padding-bottom: 20px;
        scrollbar-width: none; /* Firefox */
    }
    .movie-row-container::-webkit-scrollbar {
        display: none; /* Chrome/Safari */
    }
    
    .movie-card-wrapper {
        flex: 0 0 calc(20% - 12px); /* 5 cards per row */
        min-width: 180px;
    }

    .see-more-card {
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.05);
        border-radius: var(--radius-md);
        height: 100%;
        min-height: 270px;
        color: var(--gold);
        font-weight: 700;
        text-decoration: none;
        transition: var(--transition);
        border: 1px solid rgba(255,255,255,0.05);
    }
    .see-more-card:hover {
        background: rgba(230, 179, 90, 0.1);
        border-color: var(--gold);
        transform: translateY(-5px);
    }

    /* Hero Carousel styling */
    .carousel-container {
        position: relative;
        height: 500px;
        border-radius: var(--radius-lg);
        margin-bottom: 40px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .carousel-item {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center 20%;
        opacity: 0;
        transition: opacity 1s ease-in-out;
        display: flex;
        align-items: flex-end;
        padding: 60px;
        pointer-events: none;
    }

    .carousel-item.active {
        opacity: 1;
        pointer-events: auto;
        z-index: 10;
    }

    .carousel-item::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(0deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.6) 50%, rgba(14,17,23,0) 100%);
        z-index: -1;
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

    .hero-btn {
        display: inline-block;
        background: var(--gold);
        color: #000;
        padding: 12px 28px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(230, 179, 90, 0.3);
        transition: all 0.3s ease;
    }

    .hero-btn:hover {
        background: #fff;
        color: #000;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.4);
    }
    
    .carousel-controls {
        position: absolute;
        bottom: 60px;
        right: 60px;
        z-index: 20;
        display: flex;
        gap: 15px;
    }
    
    .carousel-btn {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        backdrop-filter: blur(5px);
        transition: all 0.2s;
    }
    
    .carousel-btn:hover {
        background: var(--gold);
        color: black;
        border-color: var(--gold);
        transform: scale(1.1);
    }

    .carousel-indicators {
        position: absolute;
        bottom: 25px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 8px;
        z-index: 20;
    }

    .carousel-indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        cursor: pointer;
        transition: all 0.3s;
    }

    .carousel-indicator.active {
        background: var(--gold);
        transform: scale(1.3);
        box-shadow: 0 0 10px var(--gold-glow);
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

    /* Robust Search Input Styling (Fixes invisible text on mobile/dark modes) */
    div[data-baseweb="input"] {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
    }
    
    .stTextInput input {
        color: white !important;
        -webkit-text-fill-color: white !important;
        background-color: transparent !important;
        caret-color: var(--gold) !important;
        padding: 12px 20px !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255,255,255,0.4) !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: var(--gold) !important;
        box-shadow: 0 0 10px var(--gold-glow) !important;
    }

    /* FIX: Robust Button Styling for Production */
    div.stButton > button {
        background: var(--gold) !important;
        color: #000000 !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(230, 179, 90, 0.2) !important;
    }

    div.stButton > button:hover {
        background: #FFFFFF !important;
        color: #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3) !important;
    }

    div.stButton > button:active {
        transform: translateY(0) !important;
    }

    /* OTT Section Styling */
    .ott-container {
        margin-top: 20px;
        padding: 20px;
        background: rgba(255,255,255,0.03);
        border-radius: var(--radius-md);
        border: 1px solid rgba(255,255,255,0.05);
    }

    .ott-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 15px;
        color: var(--gold);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .provider-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
    }

    .provider-logo {
        width: 45px;
        height: 45px;
        border-radius: 10px;
        object-fit: cover;
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.2s;
    }

    .provider-logo:hover {
        transform: scale(1.1);
        border-color: var(--gold);
    }
    
    /* Movie Details 2-Column */
    .details-container {
        display: flex;
        gap: 40px;
        margin-top: 20px;
        margin-bottom: 40px;
        background: rgba(14,17,23,0.8);
        border-radius: var(--radius-lg);
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.08);
    }
    
    .details-poster {
        flex: 0 0 300px;
    }
    
    .details-poster img {
        width: 100%;
        border-radius: var(--radius-md);
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    
    .details-info {
        flex: 1;
    }
    
    .review-card {
        background: rgba(255,255,255,0.05);
        border-radius: var(--radius-md);
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    /* MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        .carousel-container {
            height: 400px !important;
        }
        .carousel-item {
            padding: 30px !important;
        }
        .hero-title {
            font-size: 32px !important;
        }
        .logo-text {
            font-size: 30px !important;
        }
        .carousel-controls {
            bottom: 30px;
            right: 30px;
        }
    }

    @media (max-width: 480px) {
        .carousel-container {
            height: 380px !important;
        }
        .carousel-item {
            padding: 20px !important;
            padding-bottom: 60px !important;
        }
        .hero-title {
            font-size: 24px !important;
        }
        .hero-content p {
            font-size: 13px !important;
            -webkit-line-clamp: 3 !important;
        }
        .carousel-controls {
            display: none !important; /* Hide controls on mobile due to space, rely on indicator taps */
        }
        .carousel-indicators {
            bottom: 15px;
        }
        /* Mobile Grid Adjustment for Horizontal Scrolling */
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(6)) {
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            scrollbar-width: none !important;
            -ms-overflow-style: none !important;
            padding-bottom: 15px !important;
            gap: 12px !important;
        }
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(6))::-webkit-scrollbar {
            display: none !important;
        }
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(6)) > [data-testid="column"] {
            flex: 0 0 140px !important; /* Fixed width on mobile */
            width: 140px !important;
            min-width: 140px !important;
            margin-bottom: 0 !important;
        }
    }

    .gold-text { color: var(--gold); }
    </style>
    """, unsafe_allow_html=True)

def render_slideshow(movies):
    """Render a pure HTML/CSS/JS cinematic autoplay carousel for hero slides."""
    if not movies:
        return
        
    slides_html = ""
    indicators_html = ""
    
    for idx, movie in enumerate(movies):
        title = movie.get("title", "Unknown Title")
        year = movie.get("release_date", "N/A")[:4] if movie.get("release_date") else "N/A"
        overview = movie.get("overview", "")
        # Escape single quotes and newlines for HTML safety
        overview = overview.replace("'", "&#39;").replace('"', "&quot;").replace("\n", " ")
        title = title.replace("'", "&#39;").replace('"', "&quot;")
        
        rating = round(movie.get("vote_average", 0), 1)
        
        # Get backdrop url
        path = movie.get("backdrop_path")
        if not path:
            image_url = f"data:image/png;base64,{get_base64_image('placeholder.png')}"
        else:
            image_url = f"https://image.tmdb.org/t/p/original/{path}"
            
        active_class = "active" if idx == 0 else ""
        
        slides_html += f"""
        <div class="carousel-item {active_class}" style="background-image: url('{image_url}');">
            <div class="hero-content">
                <div class="hero-title">{title}</div>
                <div style="color: var(--gold); font-size: 18px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span>{year}</span>
                    <span style="color: rgba(255,255,255,0.4);">|</span>
                    <span class="rating">⭐ {rating}</span>
                    <span style="color: rgba(255,255,255,0.4);">|</span>
                    <span style="color: var(--text-muted); font-weight: 400;">Trending This Week</span>
                </div>
                <p style="color: rgba(255,255,255,0.9); font-size: 14px; line-height: 1.6; margin-bottom: 24px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; max-width: 650px;">
                    {overview}
                </p>
                <!-- Native <a> link triggers Streamlit script query params -->
                <a href="/?movie_id={movie.get('id')}" target="_parent" class="hero-btn">
                    ▶ View Details
                </a>
            </div>
        </div>
        """
        
        indicators_html += f'<div class="carousel-indicator {active_class}" onclick="jumpToSlide({idx})"></div>'
        
    carousel_html = f"""<div class="carousel-container" id="heroCarousel">
{slides_html}
<div class="carousel-controls">
<button class="carousel-btn" onclick="prevSlide()">❮</button>
<button class="carousel-btn" onclick="nextSlide()">❯</button>
</div>
<div class="carousel-indicators">
{indicators_html}
</div>
</div>
<script>
(function() {{
const container = document.getElementById('heroCarousel');
if (!container) return;
const slides = container.querySelectorAll('.carousel-item');
const indicators = container.querySelectorAll('.carousel-indicator');
let currentIndex = 0;
let intervalId = null;
const slideDuration = 6000;
function showSlide(index) {{
slides.forEach((el, i) => {{
el.classList.remove('active');
indicators[i].classList.remove('active');
if (i === index) {{
el.classList.add('active');
indicators[i].classList.add('active');
}}
}});
currentIndex = index;
}}
window.nextSlide = function() {{
const nextIndex = (currentIndex + 1) % slides.length;
showSlide(nextIndex);
}};
window.prevSlide = function() {{
const prevIndex = (currentIndex - 1 + slides.length) % slides.length;
showSlide(prevIndex);
}};
window.jumpToSlide = function(index) {{
showSlide(index);
}};
function startAutoplay() {{
if (intervalId) clearInterval(intervalId);
intervalId = setInterval(window.nextSlide, slideDuration);
}}
function stopAutoplay() {{
if (intervalId) clearInterval(intervalId);
}}
container.addEventListener('mouseenter', stopAutoplay);
container.addEventListener('mouseleave', startAutoplay);
container.addEventListener('touchstart', stopAutoplay, {{passive: true}});
container.addEventListener('touchend', startAutoplay, {{passive: true}});
startAutoplay();
}})();
</script>"""
    
    st.markdown(carousel_html, unsafe_allow_html=True)

def render_movie_card(movie, poster_url):
    """Helper for internal markdown movie card markup."""
    title = movie.get("title")
    year = movie.get("release_date", "N/A")[:4]
    rating = round(movie.get("vote_average", 0), 1)
    lang = movie.get("original_language", "xx").upper()
    
    if poster_url == "placeholder.png":
        b64_img = get_base64_image("placeholder.png")
        poster_url = f"data:image/png;base64,{b64_img}"
        
    return f"""<div class="movie-card" style="height: 100%; display: flex; flex-direction: column;">
    <div style="position: relative;">
        <img src="{poster_url}" class="card-img" style="aspect-ratio: 2/3; object-fit: cover; width: 100%;">
        <div style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: var(--gold); padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; border: 1px solid rgba(230,179,90,0.3); backdrop-filter: blur(4px);">
            {lang}
        </div>
    </div>
    <div class="card-info" style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-title">{title}</div>
        <div class="card-meta">
            <span>{year}</span>
            <span class="rating">★ {rating}</span>
        </div>
    </div>
</div>"""

def render_see_more_card():
    """Render a clickable card styled EXACTLY like a movie card for perfect grid alignment."""
    return f"""<div class="movie-card see-more-card" style="height: 100%; display: flex; flex-direction: column;">
    <div style="position: relative; width: 100%; padding-top: 150%; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.02);">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; width: 100%;">
            <div style="font-size: 32px; margin-bottom: 8px;">➕</div>
            <div style="color: var(--text-main); font-weight: 700; letter-spacing: 1px; font-size: 14px;">SEE MORE</div>
            <div style="color: var(--gold); font-size: 20px; margin-top: 8px;">➔</div>
        </div>
    </div>
    <div class="card-info" style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; visibility: hidden;">
        <div class="card-title">Placeholder Title</div>
        <div class="card-meta">
            <span>2099</span>
            <span class="rating">★ 0.0</span>
        </div>
    </div>
</div>"""

def render_detail_hero(movie, backdrop_url, poster_url):
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
        
    if poster_url == "placeholder.png":
        b64_img = get_base64_image("placeholder.png")
        poster_url = f"data:image/png;base64,{b64_img}"
        
    # We will use st.columns in app.py for the layout to allow Streamlit buttons,
    # but we can provide the backdrop container here.
    st.markdown(f"""<div style="position: absolute; top: 0; left: 0; right: 0; height: 60vh; background-image: url('{backdrop_url}'); background-size: cover; background-position: center 20%; opacity: 0.2; z-index: -1; mask-image: linear-gradient(to bottom, black 50%, transparent 100%); -webkit-mask-image: linear-gradient(to bottom, black 50%, transparent 100%);"></div>""", unsafe_allow_html=True)

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
    
    watch_link = providers.get("link", "#")
    
    found_any = False
    for label, items in categories:
        if items:
            found_any = True
            html_output += f'<div style="font-size: 13px; color: var(--text-muted); margin-bottom: 8px;">{label}</div>'
            html_output += '<div class="provider-grid">'
            for item in items:
                logo_url = f"https://image.tmdb.org/t/p/original{item.get('logo_path')}"
                name = item.get("provider_name")
                # Wrap in anchor tag for redirection
                html_output += f'<a href="{watch_link}" target="_blank" title="Watch on {name}"><img src="{logo_url}" class="provider-logo"></a>'
            html_output += '</div><div style="height: 15px;"></div>'
    
    if not found_any:
        html_output += '<div style="color: var(--text-muted);">Streaming info not available.</div>'
    
    html_output += '</div>'
    st.markdown(html_output, unsafe_allow_html=True)

def render_omdb_reviews(omdb_data):
    """Render the OMDB aggregate ratings block."""
    st.markdown('<h4 style="color: var(--gold); margin-top: 10px; margin-bottom: 20px; text-transform: uppercase; font-weight: 800; letter-spacing: 1px;">⭐ Ratings</h4>', unsafe_allow_html=True)

    if omdb_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            imdb = omdb_data.get("imdbRating", "N/A")
            st.markdown(f'<div style="text-align: center; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 24px; color: var(--gold); font-weight: bold;">⭐ {imdb}</div><div style="font-size: 13px; color: var(--text-muted);">IMDb Rating</div></div>', unsafe_allow_html=True)
            
        with col2:
            meta = omdb_data.get("Metascore", "N/A")
            st.markdown(f'<div style="text-align: center; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 24px; color: #66CC33; font-weight: bold;">🎬 {meta}</div><div style="font-size: 13px; color: var(--text-muted);">Metascore</div></div>', unsafe_allow_html=True)
            
        with col3:
            votes = omdb_data.get("imdbVotes", "N/A")
            st.markdown(f'<div style="text-align: center; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 24px; color: #4DA6FF; font-weight: bold;">👥 {votes}</div><div style="font-size: 13px; color: var(--text-muted);">IMDb Votes</div></div>', unsafe_allow_html=True)
            
        with col4:
            rotten = "N/A"
            ratings = omdb_data.get("Ratings", [])
            for r in ratings:
                if r.get("Source") == "Rotten Tomatoes":
                    rotten = r.get("Value")
                    break
            st.markdown(f'<div style="text-align: center; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 24px; color: #FA320A; font-weight: bold;">🍅 {rotten}</div><div style="font-size: 13px; color: var(--text-muted);">Rotten Tomatoes</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color: var(--text-muted);">Aggregate ratings not available</div>', unsafe_allow_html=True)

