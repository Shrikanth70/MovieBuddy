import streamlit as st
import streamlit.components.v1 as components_v1
import tmdb_service as tmdb
import omdb_service as omdb
import components as ui
import recommendation as rec_engine

def render_movie_details_page():
    """Immersive detail view (Standalone Page)."""
    # Get movie ID from query params or session state
    movie_id = st.query_params.get("movie_id") or st.session_state.get("selected_movie_id")
    
    if not movie_id:
        st.info("Select a movie from the home page to view details.")
        if st.button("Go to Home"):
            st.query_params.clear()
            st.rerun()
        return

    try:
        movie_id = int(movie_id)
    except:
        st.error("Invalid movie ID.")
        return

    with st.spinner("Loading movie details..."):
        movie = tmdb.get_movie_details(movie_id)
        trailers = tmdb.get_movie_videos(movie_id)
        omdb_data = omdb.get_movie_reviews(movie.get("title") if movie else "")
        
    if not movie:
        st.error("Could not load movie details.")
        if st.button("← Back to Home"):
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
        # Native back button for 100% styling reliability
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="/?home=true" target="_self" class="back-pill-btn">
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
        
        title = movie.get("title")
        year = movie.get("release_date", "N/A")[:4]
        runtime = f"{movie.get('runtime', 'N/A')} min"
        genres = ", ".join([g.get("name") for g in movie.get("genres", [])])
        overview = movie.get("overview", "")
        
        st.markdown(f'<h1 style="font-size: 48px; font-weight: 800; margin-bottom: 5px; line-height: 1.1;">{title}</h1>', unsafe_allow_html=True)
        st.markdown(f'<div style="color: rgba(255,255,255,0.65); font-size: 15px; font-weight: 600; margin-bottom: 20px; letter-spacing: 0.3px;">{year} &nbsp;|&nbsp; {runtime} &nbsp;|&nbsp; {genres}</div>', unsafe_allow_html=True)
        
        st.markdown(f'<p style="color: rgba(255,255,255,0.9); font-size: 16px; line-height: 1.6; margin-bottom: 30px;">{overview}</p>', unsafe_allow_html=True)
        
        # Display aggregated OMDB Without Reviews
        ui.render_omdb_reviews(omdb_data)
        
        st.markdown('</div>', unsafe_allow_html=True) # End of details-info
        
    # Trailer and Where to Watch Side-by-Side (Full Width)
    st.markdown('<br>', unsafe_allow_html=True)
    # Bottom Section: Trailer, Crew, and Cast
    st.markdown('<br>', unsafe_allow_html=True)
    b_col1, b_col2 = st.columns([1.5, 1], gap="large")
    
    cast, crew = tmdb.get_movie_credits(movie_id)
    
    with b_col1:
        st.markdown('<div class="ott-title" style="margin-bottom: 15px;">🎬 Trailer</div>', unsafe_allow_html=True)
        if trailers:
            st.video(f"https://www.youtube.com/watch?v={trailers[0].get('key')}")
        else:
            st.markdown('<div style="color: var(--text-muted); padding: 40px; background: rgba(255,255,255,0.03); border-radius: 12px; text-align: center;">Trailer Unavailable</div>', unsafe_allow_html=True)

    with b_col2:
        st.markdown('<div class="ott-title" style="margin-bottom: 15px;">Production</div>', unsafe_allow_html=True)
        director = crew.get("director", "N/A")
        writer = crew.get("writer", "N/A")
        
        crew_html = '<div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">'
        if director != "N/A":
            crew_html += f'<div style="margin-bottom: 12px;"><div style="color: var(--text-muted); font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Director</div><div style="font-size: 18px; font-weight: 700; color: white;">{director}</div></div>'
        if writer != "N/A" and writer != director:
            crew_html += f'<div><div style="color: var(--text-muted); font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Writer</div><div style="font-size: 18px; font-weight: 700; color: white;">{writer}</div></div>'
        crew_html += '</div>'
        st.markdown(crew_html, unsafe_allow_html=True)

    # Monolithic Cast Row (Iframe-based for absolute CSS isolation)
    if cast:
        st.markdown('<div class="ott-title" style="margin-top: 40px; margin-bottom: 20px;">Cast & Crew</div>', unsafe_allow_html=True)
        
        # Build the HTML for the cast row inside the iframe
        cast_items_html = ""
        for actor in cast[:12]:
            profile_path = actor.get("profile_path")
            img = f"https://image.tmdb.org/t/p/w185{profile_path}" if profile_path else "https://via.placeholder.com/100x150?text=No+Photo"
            name = actor.get('name', 'Unknown')
            char = actor.get('character', 'Character')
            
            cast_items_html += f'''
                <div class="cast-card">
                    <img src="{img}" class="cast-img">
                    <div class="cast-name" title="{name}">{name}</div>
                    <div class="cast-char" title="{char}">{char}</div>
                </div>
            '''
            
        iframe_html = f'''
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                color: white;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                overflow: hidden;
            }}
            .cast-row {{
                display: flex;
                gap: 20px;
                overflow-x: auto;
                padding: 10px 5px 30px 5px;
                scrollbar-width: none;
                -ms-overflow-style: none;
            }}
            .cast-row::-webkit-scrollbar {{ display: none; }}
            .cast-card {{
                flex: 0 0 100px;
                width: 100px;
                text-align: center;
                transition: transform 0.3s ease;
            }}
            .cast-img {{
                width: 100px;
                height: 150px;
                border-radius: 12px;
                object-fit: cover;
                box-shadow: 0 10px 25px rgba(0,0,0,0.7);
                border: 1px solid rgba(255,255,255,0.1);
                margin-bottom: 12px;
            }}
            .cast-name {{
                font-size: 11px;
                font-weight: 700;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                width: 100px;
                margin-bottom: 2px;
            }}
            .cast-char {{
                font-size: 10px;
                color: rgba(255,255,255,0.5);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                width: 100px;
            }}
        </style>
        <div class="cast-row">
            {cast_items_html}
        </div>
        '''
        components_v1.html(iframe_html, height=250, scrolling=False, width=None)

    # Recommendations
    st.markdown('---')
    recs = tmdb.get_movie_recommendations(movie_id, limit=10)
    if recs:
        st.markdown('<div class="ott-title" style="margin-bottom: 20px;">People also watched</div>', unsafe_allow_html=True)
        ui.render_movie_grid(recs, key_prefix="page_recs")

if __name__ == "__main__":
    try:
        ui.inject_custom_css()
    except Exception as e:
        st.error(f"CSS injection failed: {e}")
        print(f"CSS Error: {e}")
    # Background Texture
    st.markdown('<div class="bg-texture"></div>', unsafe_allow_html=True)
    render_movie_details_page()
