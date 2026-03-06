import streamlit as st
from services import tmdb_api as tmdb
from components import movie_card as mc

def render_search_page():
    """Clean search results UI (ISSUE 4)."""
    query = st.session_state.query
    if not query:
        st.info("Start typing in the search bar above to find movies.")
        return
        
    st.markdown(f"## Results for: {query}")
    results = tmdb.search_movies(query)
    
    if results:
        mc.render_movie_grid(results, key_prefix="search_res", cols_per_row=5)
    else:
        st.warning(f"No movies found for '{query}'.")
