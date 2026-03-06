import streamlit as st
import layout
import navigation
import home
import search
import movies
import tmdb_service as tmdb
import supabase_service as auth

# 1. Global Setup (ISSUE 8)
layout.set_global_page_config()
layout.inject_global_css()

# 2. Navigation State (ISSUE 2)
navigation.init_navigation_state()

# --- Auth Gate ---
def show_auth():
    l, r = st.columns([1, 1], gap="large")
    with l:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1A4D2E 0%, #07090D 100%); padding: 4rem; border-radius: 30px; height: 600px; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(255,255,255,0.05); margin-top: 50px;">
                <h1 style="font-size: 48px; color: #FFB000;">MovieBuddy</h1>
                <p style="color: white; font-size: 18px; opacity: 0.8;">Your personal gateway to cinematic excellence.</p>
            </div>
        """, unsafe_allow_html=True)
    with r:
        st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
        auth_mode = st.radio("Mode", ["Login", "Sign Up"], horizontal=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Submit", type="primary", use_container_width=True):
            if auth_mode == "Login":
                res, err = auth.sign_in(email, password)
                if not err: st.session_state.user = res.user; st.rerun()
                else: st.error(err)
            else:
                res, err = auth.sign_up(email, password)
                if not err: st.success("Check your email!"); st.rerun()
                else: st.error(err)

def main():
    if not st.session_state.get("user"):
        show_auth()
        return

    # 3. Sidebar (ISSUE 3 - Icons)
    navigation.render_sidebar()

    # 4. Search Handler (ISSUE 4)
    query = navigation.handle_search_input()

    # 5. Routing Engine (ISSUE 1, 6 - Single Page Rendering)
    
    # Priority 1: Details View
    if st.session_state.page == "details" and st.session_state.selected_movie_id:
        movies.render_movie_details(st.session_state.selected_movie_id)
        return

    # Priority 2: Search View (Ensures HOME is not shown if search is active)
    if st.session_state.page == "search" and query:
        search.render_search_results(query)
        return

    # Priority 3: Home & Other Navigation
    if st.session_state.page == "home":
        home.render_home()
    elif st.session_state.page == "watchlist":
        st.markdown("# My <span class='gold-text'>Watchlist</span>", unsafe_allow_html=True)
        items, err = auth.get_watchlist(st.session_state.user.id)
        if items: movies.render_movie_grid(items, key_prefix="watch")
        else: st.info("Empty watchlist.")
    elif st.session_state.page == "trending":
        st.markdown("# Trending <span class='gold-text'>Weekly</span>", unsafe_allow_html=True)
        weekly = tmdb.get_trending_weekly(limit=20)
        movies.render_movie_grid(weekly, key_prefix="trend")
    else:
        st.title(f"{st.session_state.page.title()} Coming Soon")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
