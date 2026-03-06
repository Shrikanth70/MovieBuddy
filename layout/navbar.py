import streamlit as st

def render_navbar():
    """Top navigation logic (Search Bar)."""
    # Sync visual search bar with session state
    query = st.text_input("🔍 Search for movies...", value=st.session_state.query, key="nav_search")
    
    if query != st.session_state.query:
        st.session_state.query = query
        if query:
            st.session_state.page = "search"
        else:
            st.session_state.page = "home"
        st.rerun()
    
    return query
