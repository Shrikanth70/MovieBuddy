import streamlit as st
import tmdb_service as tmdb
from home_view import render_movie_grid

def render_search(query):
    """Render search results only."""
    st.markdown(f"## Search Results for: <span class='gold-text'>'{query}'</span>", unsafe_allow_html=True)
    
    with st.spinner(f"Searching for '{query}'..."):
        results = tmdb.search_movies(query)
        
    if results:
        render_movie_grid(results, key_prefix="search_res")
    else:
        st.warning(f"No results found for '{query}'.")
        if st.button("Back to Home"):
            st.session_state.query = ""
            st.session_state.page = "home"
            st.rerun()
