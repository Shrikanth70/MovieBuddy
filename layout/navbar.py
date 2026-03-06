import streamlit as st
from utils import state_manager as state

def render_navbar():
    """Senior Architect Horizontal Navbar (LOGO | Nav | Search | User)."""
    
    # Navbar columns (LOGO | Home | Trending | Watchlist | Spacer | Search | Logout)
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.8, 0.7, 0.8, 0.8, 0.4, 3, 1])
    
    with c1:
        # Styled Text Logo (Not a button)
        st.markdown('<a href="/" target="_self" class="logo-text">MovieBuddy</a>', unsafe_allow_html=True)
    
    with c2:
        if st.button("Home", key="nav_home", use_container_width=True):
            state.navigate_to("home")
    with c3:
        if st.button("Trending", key="nav_trend", use_container_width=True):
            state.navigate_to("trending")
    with c4:
        if st.button("Watchlist", key="nav_watch", use_container_width=True):
            state.navigate_to("watchlist")
    
    with c5:
        st.write("") # Spacer column
    
    with c6:
        query = st.text_input("Search", placeholder="Search movies...", value=st.session_state.query, key="nav_search", label_visibility="collapsed")
        if query != st.session_state.query:
            st.session_state.query = query
            st.session_state.page = "search" if query else "home"
            st.rerun()

    with c7:
        if st.button("Logout", key="nav_logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    st.markdown("---")
