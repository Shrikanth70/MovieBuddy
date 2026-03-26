import streamlit as st
from services import supabase_api as auth_service
from components import movie_card as mc
from services import tmdb_api as tmdb

def render_watchlist_page():
    col_back, _ = st.columns([1.5, 8.5])
    with col_back:
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="/?home=true" target="_self" class="back-pill-btn">
                    <span style="margin-right: 8px;">←</span> BACK
                </a>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown("# My Watchlist")
    items, err = auth_service.get_watchlist(st.session_state.user.id)
    if items:
        mc.render_movie_grid(items, key_prefix="page_watch", cols_per_row=5)
    else:
        st.info("Your watchlist is empty. Add movies to see them here!")
