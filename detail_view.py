import streamlit as st
import tmdb_service as tmdb
import supabase_service as auth

def render_details(movie_id):
    """Movie details page."""
    if st.button("❮ Back"):
        st.session_state.selected_movie_id = None
        st.session_state.page = "home"
        st.rerun()
        
    movie = tmdb.get_movie_details(movie_id)
    if not movie:
        st.error("Movie not found.")
        return
        
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(tmdb.get_image_url(movie.get("poster_path")), use_container_width=True)
        
        # Watchlist toggle
        is_saved = auth.is_in_watchlist(st.session_state.user.id, movie_id)
        if st.button("❤️ In Watchlist" if is_saved else "➕ Add to Watchlist", use_container_width=True):
            if is_saved:
                auth.remove_from_watchlist(st.session_state.user.id, movie_id)
            else:
                auth.add_to_watchlist(st.session_state.user.id, movie)
            st.rerun()

    with col2:
        st.title(movie.get("title"))
        st.markdown(f"**Year:** {movie.get('release_date', 'N/A')[:4]} | **Runtime:** {movie.get('runtime', 'N/A')} min")
        st.markdown(f"**Rating:** ⭐ {movie.get('vote_average', 'N/A')}")
        st.write(movie.get("overview"))
        
        # OMDb Ratings
        imdb_id = tmdb.get_imdb_id(movie_id)
        if imdb_id:
            omdb_data = tmdb.get_omdb_data(imdb_id)
            if omdb_data and omdb_data.get("Response") == "True":
                st.markdown("---")
                c1, c2 = st.columns(2)
                c1.metric("Awards", omdb_data.get("Awards", "N/A"))
                c2.metric("Box Office", omdb_data.get("BoxOffice", "N/A"))

        # Trailer
        trailers = tmdb.get_movie_videos(movie_id)
        if trailers:
            st.markdown("---")
            st.markdown("### Official Trailer")
            st.video(f"https://www.youtube.com/watch?v={trailers[0].get('key')}")
