import streamlit as st
import tmdb_service as tmdb
import supabase_service as auth

def render_movie_grid(movies, key_prefix="grid", cols_per_row=5):
    """Universal native movie grid."""
    if not movies:
        return
        
    for i in range(0, len(movies), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(movies):
                movie = movies[i + j]
                with col:
                    poster_url = tmdb.get_image_url(movie.get("poster_path"))
                    st.image(poster_url, use_container_width=True)
                    st.markdown(f"**{movie.get('title')}**")
                    st.caption(f"⭐ {movie.get('vote_average', 'N/A')}")
                    if st.button("Details", key=f"{key_prefix}_{movie.get('id')}_{i+j}", use_container_width=True):
                        st.session_state.selected_movie_id = movie.get("id")
                        st.session_state.page = "details"
                        st.rerun()

def render_movie_details(movie_id):
    """Detailed movie view."""
    if st.button("❮ Back"):
        st.session_state.selected_movie_id = None
        st.session_state.page = "home"
        st.rerun()
        
    movie = tmdb.get_movie_details(movie_id)
    if not movie:
        st.error("Movie not found.")
        return
        
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(tmdb.get_image_url(movie.get("poster_path")), use_container_width=True)
        is_saved = auth.is_in_watchlist(st.session_state.user.id, movie_id)
        if st.button("❤️ In Watchlist" if is_saved else "➕ Add to Watchlist", use_container_width=True):
            if is_saved: auth.remove_from_watchlist(st.session_state.user.id, movie_id)
            else: auth.add_to_watchlist(st.session_state.user.id, movie)
            st.rerun()
    
    with c2:
        st.title(movie.get("title"))
        st.markdown(f"**{movie.get('release_date', 'N/A')[:4]}** | {movie.get('runtime', 'N/A')} min | ⭐ {movie.get('vote_average', 'N/A')}")
        st.write(movie.get("overview"))
        
        trailers = tmdb.get_movie_videos(movie_id)
        if trailers:
            st.markdown("### Trailer")
            st.video(f"https://www.youtube.com/watch?v={trailers[0].get('key')}")
