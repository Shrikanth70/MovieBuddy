import streamlit as st
import tmdb_service as tmdb
import movies as movie_util

def render_search_results(query):
    """Search results only (ISSUE 1)."""
    st.markdown(f"## Showing results for: :orange['{query}']")
    results = tmdb.search_movies(query)
    if results:
        movie_util.render_movie_grid(results, key_prefix="search")
    else:
        st.info("No movies found.")
