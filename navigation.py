import streamlit as st

def init_navigation_state():
    """Initialize navigation-related session state."""
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None

def render_sidebar():
    """Render the fixed sidebar using native Material Icons syntax."""
    with st.sidebar:
        st.title("MovieBuddy")
        
        # Navigation logic (ISSUE 3 - No emojis, native icons)
        nav_items = [
            ("home", "Home", "home"),
            ("trending", "Trending", "trending_up"),
            ("genres", "Genres", "movie"),
            ("watchlist", "Watchlist", "favorite"),
        ]
        
        for page_id, label, icon_name in nav_items:
            # Using Streamlit's native icon syntax: :material/icon_name:
            if st.button(f":material/{icon_name}: {label}", key=f"nav_{page_id}", use_container_width=True):
                st.session_state.page = page_id
                st.session_state.selected_movie_id = None
                st.session_state.query = ""
                st.rerun()
                
        st.markdown("---")
        
        if st.button(":material/logout: Logout", key="logout_btn", use_container_width=True):
            st.session_state.user = None
            st.rerun()

def handle_search_input():
    """Global search bar logic that controls page state."""
    # Issue 4: Search bar must update st.session_state.query and switch page to 'search'
    search_val = st.text_input("🔍 Search Movies...", value=st.session_state.query, key="global_search")
    
    if search_val != st.session_state.query:
        st.session_state.query = search_val
        if search_val:
            st.session_state.page = "search"
        else:
            st.session_state.page = "home"
        st.rerun()
    
    return search_val
