import base64
import os
import streamlit as st
import time
import json

@st.cache_data
def get_base64_image(image_path):
    """Convert local image to base64 string for HTML embedding."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


    # Import Poppins font
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Montserrat:wght@400;700;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    :root {
        --bg-dark: #0E1117;
        --bg-card: #1C212B;
        --accent: #E50914; /* Netflix Red */
        --accent-glow: rgba(229, 9, 20, 0.4);
        --gold: #FFC107; /* Amber/Gold */
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
        background-image: radial-gradient(circle at 50% 50%, rgba(229, 9, 20, 0.05) 0%, transparent 100%);
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
        color: var(--accent);
        font-weight: 700;
        text-decoration: none;
        transition: var(--transition);
        border: 1px solid rgba(255,255,255,0.05);
    }
    .see-more-card:hover {
        background: rgba(229, 9, 20, 0.1);
        border-color: var(--accent);
        transform: translateY(-5px);
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
        text-decoration: none !important;
        display: block;
    }

    .movie-card, .hero-btn, .carousel-btn, .carousel-indicator, .see-more-card { cursor: pointer !important; }
    
    /* THE NATIVE BRIDGE: ZERO-ARTIFACT OVERLAY */
    .native-card-wrapper {
        position: relative;
        width: 100%;
        margin-bottom: 5px;
    }
    
    /* card-btn-container: a positioned container that puts the invisible button on top of the card */
    .card-btn-container {
        position: absolute !important;
        inset: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 10;
    }
    
    /* Hover effect driven by CSS wrapper class */
    .native-card-wrapper:hover .movie-card {
        transform: translateY(-8px);
        border-color: #E50914;
        box-shadow: 0 15px 35px rgba(0,0,0,0.8);
    }
    /* Restore the hover overlay tooltip visibility */
    .native-card-wrapper:hover .card-overlay-hint {
        opacity: 1 !important;
    }
    .native-card-wrapper:hover .card-overlay-hint span {
        transform: translateY(0) !important;
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

    .rating { color: var(--accent); font-weight: 700; display: flex; align-items: center; gap: 4px; }

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

    .logo-movie { color: var(--accent); }
    .logo-buddy { color: #FFFFFF; }

    .logo-link:hover {
        transform: scale(1.03);
        filter: drop-shadow(0 0 15px rgba(229, 9, 20, 0.3));
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
        caret-color: var(--accent) !important;
        padding: 12px 20px !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255,255,255,0.4) !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 10px var(--accent-glow) !important;
    }

    /* FIX: Robust Button Styling for Production */
    div.stButton > button {
        background: var(--accent) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.2) !important;
    }

    div.stButton > button:hover {
        background: #FFFFFF !important;
        color: #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3) !important;
    }

    /* Artifact-Free Navigation: All cards now use native <a> tags */
    .native-card-wrapper {
        position: relative;
        transition: var(--transition) !important;
        z-index: 1;
        cursor: pointer;
        display: block;
    }
    .native-card-wrapper:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important;
    }

    /* Back pill button: Native absolute control */
    .back-btn-container {
        margin: 20px 0;
    }
    .back-pill-btn {
        display: inline-flex;
        align-items: center;
        background: rgba(255,255,255,0.06) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        padding: 10px 24px !important;
        border-radius: 30px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        text-decoration: none !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    .back-pill-btn:hover {
        background: white !important;
        color: #111 !important;
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(255,255,255,0.15) !important;
        border-color: white !important;
    }

    /* Back button: pill — legacy override (kept for safety) */
    .stApp .back-btn-col button,
    .stApp .back-btn-col div.stButton > button {
        background: rgba(255,255,255,0.06) !important;
        color: white !important;
        border-radius: 30px !important;
    }

    /* Native Hero Nav Buttons: Forced specificity, perfectly centered and circular */
    .hero-nav-btn {
        position: absolute !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 50px !important;
        height: 50px !important;
        background: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        font-size: 24px !important;
        z-index: 100 !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    .hero-nav-btn:hover {
        background: var(--accent) !important;
        transform: translateY(-50%) scale(1.1) !important;
        box-shadow: 0 0 25px var(--accent-glow) !important;
        border-color: white !important;
    }
    .hero-nav-btn.prev { left: 20px !important; }
    .hero-nav-btn.next { right: 20px !important; }

    /* Cast Names: Absolute Single-Line Ellipsis (Broad Targeting) */
    .cast-name-clean,
    .cast-name-clean div,
    .cast-name-clean span {
        text-align: center !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        color: white !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        width: 100px !important;
        display: block !important;
        line-height: 1.4 !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }
    .hero-nav-wrapper button:hover {
        background: var(--accent) !important;
        transform: scale(1.1) !important;
        border-color: white !important;
        box-shadow: 0 0 25px var(--accent-glow) !important;
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
        color: var(--accent);
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
        border-color: var(--accent);
    }

    /* Cast Section Styling */
    .cast-scroll {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 10px 0;
        scrollbar-width: thin;
        scrollbar-color: var(--accent) transparent;
    }
    .cast-scroll::-webkit-scrollbar { height: 6px; }
    .cast-scroll::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 10px; }

    .cast-item {
        flex: 0 0 120px;
        text-align: center;
    }
    .cast-img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 10px;
        border: 2px solid rgba(255,255,255,0.1);
    }
    .cast-name { font-size: 13px; font-weight: 700; color: white; display: block; }
    .cast-role { font-size: 11px; color: var(--text-muted); }
    
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
        .details-container { padding: 20px; gap: 20px; }
    }

    .accent-text { color: var(--accent); }
    </style>
    """, unsafe_allow_html=True)

def render_slideshow(movies):
    """Render a seamless, client-side JS cinematic slideshow that avoids Streamlit reloads."""
    if not movies:
        return
        
    # Prepare slide data for JS
    slides_data = []
    for m in movies:
        title = m.get('title', 'Unknown').replace("'", "\\'")
        overview = m.get('overview', '').replace("'", "\\'").replace("\n", " ")
        year = m.get('release_date', 'N/A')[:4]
        rating = round(m.get('vote_average', 0), 1)
        mid = m.get('id')
        backdrop = f"https://image.tmdb.org/t/p/original{m.get('backdrop_path')}" if m.get('backdrop_path') else "placeholder.png"
        slides_data.append({
            "id": mid,
            "title": title,
            "overview": overview,
            "year": year,
            "rating": rating,
            "backdrop": backdrop
        })
    
    slides_json = json.dumps(slides_data)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; background: transparent; overflow: hidden; }}
        
        .slider-wrapper {{
            position: relative;
            width: 100%;
            height: 500px;
            border-radius: 20px;
            overflow: hidden;
            background: #000;
        }}
        
        .slides-container {{
            display: flex;
            width: 100%;
            height: 100%;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .slide {{
            flex: 0 0 100%;
            height: 100%;
            position: relative;
            background-size: cover;
            background-position: center 20%;
            display: flex;
            align-items: flex-end;
            padding: 60px;
            cursor: pointer;
            text-decoration: none;
        }}
        
        .slide-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(0deg, rgba(14,17,23,1) 0%, rgba(14,17,23,0.3) 70%, transparent 100%);
            z-index: 1;
        }}
        
        .slide-content {{
            position: relative;
            z-index: 2;
            max-width: 700px;
            color: white;
        }}
        
        .badge {{
            display: inline-block;
            background: rgba(229,9,20,0.2);
            color: #E50914;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 12px;
            border: 1px solid rgba(229,9,20,0.2);
            letter-spacing: 1.5px;
        }}
        
        .title {{ font-size: 52px; font-weight: 900; line-height: 1.1; margin-bottom: 10px; }}
        .meta {{ font-size: 18px; font-weight: 700; margin-bottom: 20px; display: flex; gap: 15px; align-items: center; }}
        .year-box {{ border: 1px solid rgba(255,255,255,0.3); padding: 2px 10px; border-radius: 6px; }}
        .rating {{ color: #FFC107; }}
        .overview {{ color: rgba(255,255,255,0.8); font-size: 15px; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        
        .nav-btn {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 50px;
            height: 50px;
            background: rgba(0, 0, 0, 0.5);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 100;
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            font-size: 20px;
            transition: all 0.3s;
        }}
        .nav-btn:hover {{ background: #E50914; transform: translateY(-50%) scale(1.1); }}
        .prev {{ left: 20px; }}
        .next {{ right: 20px; }}
        
        .indicators {{
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 8px;
            z-index: 100;
        }}
        .dot {{ width: 20px; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.2); transition: all 0.3s; cursor: pointer; }}
        .dot.active {{ width: 40px; background: #E50914; }}
    </style>
    </head>
    <body>
        <div class="slider-wrapper">
            <div class="slides-container" id="slides-container">
                <!-- Slides injected by JS -->
            </div>
            <div class="nav-btn prev" onclick="move(-1)">❮</div>
            <div class="nav-btn next" onclick="move(1)">❯</div>
            <div class="indicators" id="indicators"></div>
        </div>

        <script>
            const slides = {slides_json};
            const container = document.getElementById('slides-container');
            const indicators = document.getElementById('indicators');
            let currentIdx = 0;
            let autoTimer;

            function init() {{
                slides.forEach((s, i) => {{
                    // Create slide element
                    const slide = document.createElement('div');
                    slide.className = 'slide';
                    slide.style.backgroundImage = `url(${{{{s.backdrop}}}})`;
                    slide.onclick = () => { window.parent.location.href = `/?movie_id=${{{{s.id}}}}`; };
                    
                    slide.innerHTML = `
                        <div class="slide-overlay"></div>
                        <div class="slide-content">
                            <div class="badge">Featured Selection</div>
                            <div class="title">${{{{s.title}}}}</div>
                            <div class="meta">
                                <span class="year-box">${{{{s.year}}}}</span>
                                <span>|</span>
                                <span class="rating">⭐ ${{{{s.rating}}}}</span>
                            </div>
                            <p class="overview">${{{{s.overview}}}}</p>
                        </div>
                    `;
                    container.appendChild(slide);

                    // Create indicator dot
                    const dot = document.createElement('div');
                    dot.className = 'dot' + (i === 0 ? ' active' : '');
                    dot.onclick = () => goTo(i);
                    indicators.appendChild(dot);
                }});
                
                startAuto();
            }}

            function goTo(idx) {{
                currentIdx = idx;
                update();
                resetAuto();
            }}

            function move(step) {{
                currentIdx = (currentIdx + step + slides.length) % slides.length;
                update();
                resetAuto();
            }}

            function update() {{
                container.style.transform = `translateX(-${{{{currentIdx * 100}}}}%)`;
                Array.from(indicators.children).forEach((dot, i) => {{
                    dot.className = 'dot' + (i === currentIdx ? ' active' : '');
                }});
            }}

            function startAuto() {{
                autoTimer = setInterval(() => move(1), 8000);
            }}

            function resetAuto() {{
                clearInterval(autoTimer);
                startAuto();
            }}

            init();
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html, height=530)

def render_movie_card(movie, poster_url):
    """Render a clickable card using a self-targeting link."""
    title = movie.get("title")
    year = movie.get("release_date", "N/A")[:4]
    rating = round(movie.get("vote_average", 0), 1)
    lang = movie.get("original_language", "xx").upper()
    mid = movie.get("id")
    
    if poster_url == "placeholder.png":
        b64_img = get_base64_image("placeholder.png")
        poster_url = f"data:image/png;base64,{b64_img}"
        
    return f"""
    <div class="movie-card">
        <div style="position: relative;">
            <img src="{poster_url}" class="card-img">
            <div style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: var(--accent); padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; border: 1px solid rgba(229,9,20,0.3); backdrop-filter: blur(4px);">
                {lang}
            </div>
            <div class="card-overlay-hint" style="position: absolute; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; opacity: 0; transition: var(--transition); backdrop-filter: blur(4px); z-index: 5;">
                <span style="background: var(--accent); color: white; padding: 10px 20px; border-radius: 8px; font-weight: 800; font-size: 12px; letter-spacing: 1.5px; transform: translateY(20px); transition: var(--transition); box-shadow: 0 4px 15px rgba(229,9,20,0.4);">VIEW DETAILS</span>
            </div>
        </div>
        <div class="card-info">
            <div class="card-title">{title}</div>
            <div class="card-meta">
                <span>{year}</span>
                <span class="rating">★ {rating}</span>
            </div>
        </div>
    </div>"""

def render_see_more_card():
    """Render a clickable card styled EXACTLY like a movie card for perfect grid alignment."""
    return f"""<div class="movie-card see-more-card" style="height: 100%; display: flex; flex-direction: column; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.03);">
    <div style="position: relative; width: 100%; aspect-ratio: 2/3; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.02);">
        <div style="text-align: center; width: 100%;">
            <div style="font-size: 32px; margin-bottom: 8px;">➕</div>
            <div style="color: var(--text-main); font-weight: 700; letter-spacing: 1px; font-size: 14px;">SEE MORE</div>
            <div style="color: var(--accent); font-size: 20px; margin-top: 8px;">➔</div>
        </div>
    </div>
    </div>
    <div class="card-info" style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-title" style="color: var(--text-muted);">Explore All</div>
        <div class="card-meta">
            <span>&nbsp;</span>
            <span class="rating">&nbsp;</span>
        </div>
    </div>
</div>"""

def render_movie_grid(movies, key_prefix="grid", columns=5):
    """Render a responsive movie grid with native anchor links (artifact-free)."""
    for i in range(0, len(movies), columns):
        grid_cols = st.columns(columns)
        for j, movie in enumerate(movies[i:i+columns]):
            with grid_cols[j]:
                movie_id = movie.get('id')
                poster_path = movie.get("poster_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "placeholder.png"
                
                # Wrap movie card in a clickable anchor link pointing to its details
                card_html = render_movie_card(movie, poster_url)
                st.markdown(f'''
                    <a href="?movie_id={movie_id}" target="_self" style="text-decoration: none; display: block; height: 100%;">
                        <div class="native-card-wrapper">
                            {card_html}
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
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
    st.markdown('<h4 style="color: rgba(255,255,255,0.7); margin-top: 10px; margin-bottom: 20px; text-transform: uppercase; font-weight: 800; letter-spacing: 1px;">⭐ Ratings</h4>', unsafe_allow_html=True)

    if omdb_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            imdb = omdb_data.get("imdbRating", "N/A")
            st.markdown(f'<div style="text-align: center; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 24px; color: #FFFFFF; font-weight: bold;">⭐ {imdb}</div><div style="font-size: 13px; color: var(--text-muted);">IMDb Rating</div></div>', unsafe_allow_html=True)
            
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

def render_native_hero(movie, poster_url):
    """Render a premium featured movie hero using st.components.v1.html to bypass markdown sanitization."""
    title = movie.get('title', 'Featured').replace("'", "&#39;").replace('"', '&quot;')
    overview = movie.get('overview', '').replace("'", "&#39;").replace('"', '&quot;').replace('\n', ' ')
    rating = round(movie.get('vote_average', 0), 1)
    year = movie.get('release_date', '2024')[:4]
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; background: transparent; overflow: hidden; }}
        .hero {{ position: relative; height: 480px; width: 100%; border-radius: 20px; overflow: hidden; background: #000; }}
        .hero-bg {{ position: absolute; inset: 0; background-image: url('{poster_url}'); background-size: cover; background-position: center 20%; opacity: 0.7; z-index: 1; }}
        .hero-grad1 {{ position: absolute; inset: 0; background: radial-gradient(circle at 20% 50%, rgba(14,17,23,0.9) 0%, rgba(14,17,23,0.3) 70%, transparent 100%); z-index: 2; }}
        .hero-grad2 {{ position: absolute; inset: 0; background: linear-gradient(0deg, #0e1117 0%, transparent 50%); z-index: 2; }}
        .hero-content {{ position: absolute; bottom: 50px; left: 50px; z-index: 3; max-width: 650px; text-align: left; }}
        .hero-badge {{ display: inline-block; background: rgba(229,9,20,0.2); color: #E50914; padding: 4px 12px; border-radius: 4px; font-size: 11px; font-weight: 800; text-transform: uppercase; margin-bottom: 12px; border: 1px solid rgba(229,9,20,0.2); letter-spacing: 1px; }}
        .hero-title {{ font-size: 48px; font-weight: 900; color: white; margin-bottom: 12px; line-height: 1.05; text-shadow: 0 4px 12px rgba(0,0,0,0.6); }}
        .hero-meta {{ display: flex; gap: 12px; align-items: center; color: rgba(255,255,255,0.7); font-weight: 600; font-size: 14px; margin-bottom: 16px; }}
        .hero-meta .year {{ border: 1px solid rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 4px; }}
        .hero-meta .star {{ color: #FFC107; }}
        .hero-overview {{ font-size: 14px; color: rgba(255,255,255,0.75); line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
    </style>
    </head>
    <body>
        <div class="hero">
            <div class="hero-bg"></div>
            <div class="hero-grad1"></div>
            <div class="hero-grad2"></div>
            <div class="hero-content">
                <div class="hero-badge">FEATURED SELECTION</div>
                <div class="hero-title">{title}</div>
                <div class="hero-meta">
                    <span class="year">{year}</span>
                    <span class="star">★ {rating}</span>
                    <span>Exclusive</span>
                </div>
                <p class="hero-overview">{overview}</p>
            </div>
        </div>
    </body>
    </html>
    """
    st.components.v1.html(html, height=500, scrolling=False)

