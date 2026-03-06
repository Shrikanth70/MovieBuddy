import streamlit as st
from layout import navbar
from pages import home, search, movie_details, watchlist, trending
from auth import supabase_auth as auth_ui
from utils import state_manager as state
from utils import layout_utils

# 1. Global Setup
layout_utils.set_global_page_config()
layout_utils.inject_global_css()

# 2. State Initialization
state.init_session_state()

def render_current_page():
    """Central page router (STEP 1)."""
    page = st.session_state.get("page", "home")
    
    if page == "home":
        home.render_home_page()
    elif page == "search":
        search.render_search_page()
    elif page == "details":
        movie_details.render_movie_details_page()
    elif page == "watchlist":
        watchlist.render_watchlist_page()
    elif page == "trending":
        trending.render_trending_page()
    else:
        st.error(f"Page '{page}' not found.")

def main():
    # 3. Auth Gate
    if not st.session_state.get("user"):
        auth_ui.render_login_page()
        return

    # 4. Top Horizontal Navbar (Persistent Header)
    navbar.render_navbar()
    
    # Main Content Area
    render_current_page()

if __name__ == "__main__":
    main()
