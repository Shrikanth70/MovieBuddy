import streamlit as st
from services import tmdb_api as tmdb
from services import omdb_api as omdb
from services import recommendation_service as rec_service
from components import movie_card as mc
from services import supabase_api as auth_service
from utils import state_manager as state

def render_movie_details_page():
    """Immersive detail view (STEP 4 - Refactored to avoid layout bypass)."""
    movie_id = st.session_state.get("selected_movie_id")
    if not movie_id:
        state.navigate_to("home")
        return
        
    if st.button(":material/arrow_back: Back"):
        state.navigate_to("home")
        
    movie = tmdb.get_movie_details(movie_id)
    if not movie:
        st.error("Movie not found.")
        return
        
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(tmdb.get_image_url(movie.get("poster_path")), use_container_width=True)
        is_saved = auth_service.is_in_watchlist(st.session_state.user.id, movie_id)
        btn_label = "In Watchlist" if is_saved else "Add to Watchlist"
        btn_icon = "favorite" if is_saved else "add"
        if st.button(f":material/{btn_icon}: {btn_label}", use_container_width=True):
            if is_saved: auth_service.remove_from_watchlist(st.session_state.user.id, movie_id)
            else: auth_service.add_to_watchlist(st.session_state.user.id, movie)
            st.rerun()
    
    with c2:
        st.title(movie.get("title"))
        st.markdown(f"**{movie.get('release_date', 'N/A')[:4]}** | {movie.get('runtime', 'N/A')} min | Rating: {movie.get('vote_average', 'N/A')}")
        
        # OMDb Ratings (Integrated Component)
        imdb_id = tmdb.get_imdb_id(movie_id)
        omdb_data = omdb.get_omdb_data(imdb_id)
        from components import rating_display
        rating_display.render_ratings(omdb_data)

        st.write(movie.get("overview"))
        
        trailers = tmdb.get_movie_videos(movie_id)
        if trailers:
            st.markdown("### Trailer")
            st.video(f"https://www.youtube.com/watch?v={trailers[0].get('key')}")

    st.markdown("---")
    st.markdown("### People also watched")
    recs = rec_service.get_movie_recommendations(movie_id)
    mc.render_movie_grid(recs, key_prefix="detail_recs")
