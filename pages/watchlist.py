import streamlit as st
from services import supabase_api as auth_service
from components import movie_card as mc
from services import tmdb_api as tmdb

def render_watchlist_page():
    st.markdown("# My :orange[Watchlist]")
    items, err = auth_service.get_watchlist(st.session_state.user.id)
    if items:
        mc.render_movie_grid(items, key_prefix="page_watch")
    else:
        st.info("Your watchlist is empty. Add movies to see them here!")
