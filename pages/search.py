import streamlit as st
import tmdb_service as tmdb
import components as ui

def render_search_page():
    """Clean search results UI."""
    col_back, _ = st.columns([1.5, 8.5])
    with col_back:
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="/?home=true" target="_self" class="back-pill-btn">
                    <span style="margin-right: 8px;">←</span> BACK
                </a>
            </div>
        ''', unsafe_allow_html=True)
    # Use session state or params for the query
    query = st.session_state.get("movie_search_input") or st.query_params.get("q")
    
    if not query:
        st.info("Start typing in the search bar to find movies.")
        return
        
    st.markdown(f'<h2>Results for <span class="gold-text">"{query}"</span></h2>', unsafe_allow_html=True)
    results = tmdb.search_movies(query)
    
    if results:
        ui.render_movie_grid(results, key_prefix="search_res", columns=5)
    else:
        st.warning(f"No movies found for '{query}'.")

if __name__ == "__main__":
    render_search_page()
