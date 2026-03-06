import streamlit as st

def init_session_state():
    """Centralized state initialization (STEP 2)."""
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None
    if "user" not in st.session_state:
        st.session_state.user = None

def navigate_to(page, movie_id=None):
    """Universal navigation helper (STEP 6)."""
    st.session_state.page = page
    st.session_state.selected_movie_id = movie_id
    # Reset search query when navigating via menu
    if page != "search":
        st.session_state.query = ""
    st.rerun()
