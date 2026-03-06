import streamlit as st
import layout
import navigation
import home
import search
import movies
import auth as auth_ui
import tmdb_service as tmdb
import supabase_service as auth_service

# 1. Global Setup (Config & CSS only - no widgets)
layout.set_global_page_config()
layout.inject_global_css()

# 2. Navigation State (ISSUE 2)
navigation.init_navigation_state()

def main():
    # PART 1 & 5 — STRICT AUTH GATE & SINGLE PAGE RENDERING
    if not st.session_state.get("user"):
        # Renders the auth page EXACTLY ONCE
        auth_ui.render_auth_page()
        return  # Stop execution here to prevent main app from rendering

    # --- MAIN APPLICATION (Only reached if logged in) ---
    
    # 3. Sidebar (ISSUE 3 - Icons)
    navigation.render_sidebar()

    # 4. Search Handler (ISSUE 4)
    query = navigation.handle_search_input()

    # 5. Routing Engine (Strict Single Page Rendering)
    
    # Priority 1: Details View
    if st.session_state.page == "details" and st.session_state.selected_movie_id:
        movies.render_movie_details(st.session_state.selected_movie_id)
        return

    # Priority 2: Search View (Mutual exclusion for homepage)
    if st.session_state.page == "search" and query:
        search.render_search_results(query)
        return

    # Priority 3: Standard Pages
    if st.session_state.page == "home":
        home.render_home()
    elif st.session_state.page == "watchlist":
        st.markdown("# My :orange[Watchlist]")
        items, err = auth_service.get_watchlist(st.session_state.user.id)
        if items:
            movies.render_movie_grid(items, key_prefix="watch")
        else:
            st.info("Empty watchlist.")
    elif st.session_state.page == "trending":
        st.markdown("# Trending :orange[Weekly]")
        weekly = tmdb.get_trending_weekly(limit=20)
        movies.render_movie_grid(weekly, key_prefix="trend")
    else:
        st.title(f"{st.session_state.page.title()} Coming Soon")

if __name__ == "__main__":
    main()
