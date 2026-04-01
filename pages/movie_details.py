import streamlit as st
import streamlit.components.v1 as components_v1
import tmdb_service as tmdb
import omdb_service as omdb
import components as ui
import recommendation as rec_engine
import base64
from html import escape

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

    # Fetch data
    movie = tmdb.get_movie_details(movie_id)
    if not movie:
        st.error("Movie not found.")
        return

    # Back button
    ui.render_back_button()

    # Hero Banner
    backdrop = tmdb.BACKDROP_BASE_URL + movie.get("backdrop_path") if movie.get("backdrop_path") else ""
    poster = tmdb.IMAGE_BASE_URL + movie.get("poster_path") if movie.get("poster_path") else ""
    
    # Custom CSS for this page
    st.markdown(f"""
        <style>
        .detail-hero {{
            position: relative;
            width: 100%;
            height: 50vh;
            background-image: linear-gradient(to bottom, rgba(0,0,0,0.5), #000000), url('{backdrop}');
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            display: flex;
            align-items: flex-end;
            padding: 40px;
            margin-bottom: 30px;
        }}
        .detail-content {{
            display: flex;
            gap: 40px;
            margin-top: -100px;
            position: relative;
            z-index: 2;
            padding: 0 40px;
        }}
        .detail-poster {{
            width: 250px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }}
        .detail-info {{
            flex: 1;
            padding-top: 110px;
        }}
        .genre-pill {{
            background: rgba(229, 9, 20, 0.2);
            color: #E50914;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-right: 8px;
            border: 1px solid rgba(229, 9, 20, 0.3);
        }}
        .cast-scroll {{
            display: flex;
            overflow-x: auto;
            gap: 15px;
            padding: 10px 0;
            scrollbar-width: none;
        }}
        .cast-scroll::-webkit-scrollbar {{ display: none; }}
        .cast-card {{
            min-width: 120px;
            text-align: center;
        }}
        .cast-img {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 8px;
            border: 2px solid #333;
        }}
        </style>
        
        <div class="detail-hero">
            <div>
                <h1 style="font-size: 3rem; margin-bottom: 10px;">{movie.get('title')}</h1>
                <div style="margin-bottom: 20px;">
                    <span style="color: #46d369; font-weight: bold; margin-right: 15px;">
                        {int(movie.get('vote_average', 0)*10)}% Match
                    </span>
                    <span style="color: #aaa; margin-right: 15px;">{movie.get('release_date', '')[:4]}</span>
                    <span style="color: #aaa; border: 1px solid #aaa; padding: 0 4px; font-size: 0.7rem; margin-right: 15px;">HD</span>
                    <span style="color: #aaa;">{movie.get('runtime', 0)} min</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Content Layout
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        st.image(poster, use_container_width=True)
        # Watchlist button (handled by state)
        if st.button("+ Add to Watchlist", use_container_width=True):
            st.toast(f"Added {movie.get('title')} to your watchlist!")

    with col2:
        # Genres
        genres_html = "".join([f'<span class="genre-pill">{g.get("name")}</span>' for g in movie.get("genres", [])])
        st.markdown(genres_html, unsafe_allow_html=True)
        
        st.markdown(f"<p style='font-size: 1.1rem; color: #ddd; margin-top:20px;'>{movie.get('overview')}</p>", unsafe_allow_html=True)
        
        # Crew Info
        cast, crew = tmdb.get_movie_credits(movie_id)
        st.markdown(f'<div style="margin-top: 20px; color: #aaa;"><p><span style="color: #777;">Director:</span> <span style="color: #eee;">{crew.get("director")}</span></p><p><span style="color: #777;">Writers:</span> <span style="color: #eee;">{crew.get("writer")}</span></p></div>', unsafe_allow_html=True)

    # Video Trailer
    st.markdown("### Trailer & Clips")
    videos = tmdb.get_movie_videos(movie_id)
    if videos:
        trailer_key = videos[0].get("key")
        st.markdown(f'<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 12px; background: #111;"><iframe src="https://www.youtube-nocookie.com/embed/{trailer_key}?rel=0&modestbranding=1" title="Movie Trailer" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" sandbox="allow-scripts allow-same-origin allow-presentation allow-forms" allowfullscreen loading="lazy"></iframe></div>', unsafe_allow_html=True)
    else:
        st.info("No trailers available for this title.")

    # Cast Section
    st.markdown("### Top Cast")
    if cast:
        cast_items_html = ""
        for actor in cast:
            img = actor.get('profile_path')
            img_url = tmdb.IMAGE_BASE_URL + img if img else "https://ui-avatars.com/api/?name=" + actor.get('name')
            cast_items_html += f'''
                <div class="cast-card">
                    <img src="{img_url}" class="cast-img">
                    <div style="font-size: 0.8rem; font-weight: bold; color: #eee; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100px;">{actor.get('name')}</div>
                    <div style="font-size: 0.7rem; color: #888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100px;">{actor.get('character')}</div>
                </div>
            '''
        
        iframe_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ background: transparent; color: white; margin: 0; font-family: sans-serif; overflow-x: auto; -webkit-overflow-scrolling: touch; }}
                .cast-scroll {{ display: flex; gap: 20px; padding: 10px 0; }}
                .cast-card {{ flex: 0 0 100px; text-align: center; }}
                .cast-img {{ width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-bottom: 8px; border: 2px solid #333; }}
                ::-webkit-scrollbar {{ display: none; }}
            </style>
        </head>
        <body>
            <div class="cast-scroll">
                {cast_items_html}
            </div>
        </body>
        </html>
        '''
        # B64 encoding avoids markdown indentation traps and escaping issues
        b64_html = base64.b64encode(iframe_html.encode()).decode()
        st.markdown(f'<iframe src="data:text/html;base64,{b64_html}" style="width: 100%; height: 250px; border: none; overflow: hidden; background: #000;" sandbox="allow-scripts allow-same-origin"></iframe>', unsafe_allow_html=True)

    # Recommendations
    st.markdown('---')
    st.markdown("### Similar Titles You Might Like")
    recs = tmdb.get_movie_recommendations(movie_id)
    if recs:
        ui.render_movie_row("", recs, f"detail_rec_{movie_id}")
    else:
        st.info("No similar titles found.")

if __name__ == "__main__":
    render_movie_details_page()
