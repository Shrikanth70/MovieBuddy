import streamlit as st
from utils import state_manager as state

def render_sidebar():
    """Stationary sidebar logic."""
    with st.sidebar:
        st.title("MovieBuddy")
        
        nav_items = [
            ("home", "Home", "home"),
            ("trending", "Trending", "trending_up"),
            ("watchlist", "Watchlist", "favorite"),
        ]
        
        for p_id, label, icon in nav_items:
            if st.button(f":material/{icon}: {label}", key=f"side_{p_id}", use_container_width=True):
                state.navigate_to(p_id)
                
        st.markdown("---")
        if st.button(":material/logout: Sign Out", key="logout_btn", use_container_width=True):
            st.session_state.user = None
            st.rerun()
