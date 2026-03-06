import streamlit as st
import time
from services import tmdb_api as tmdb
from utils import state_manager as state

def render_trending_slideshow():
    """Rotating banner component (ISSUE 3)."""
    trending = tmdb.get_trending_daily(limit=5)
    if not trending: return

    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0
    if "last_slide_time" not in st.session_state:
        st.session_state.last_slide_time = time.time()

    # Timer logic
    if time.time() - st.session_state.last_slide_time > 5.0:
        st.session_state.slide_index = (st.session_state.slide_index + 1) % len(trending)
        st.session_state.last_slide_time = time.time()
        st.rerun()

    movie = trending[st.session_state.slide_index]
    backdrop = tmdb.get_image_url(movie.get("backdrop_path"), size="original")
    
    st.image(backdrop, use_container_width=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.title(movie.get("title"))
        st.caption(f"{movie.get('release_date','N/A')[:4]} | Rating: {movie.get('vote_average')}")
        st.write(movie.get("overview"))
        if st.button("Learn More", key=f"slide_btn_{movie.get('id')}", type="primary"):
            state.navigate_to("details", movie.get("id"))
    
    with c2:
        # Navigation dots
        dots = st.columns(len(trending))
        for i in range(len(trending)):
            if i == st.session_state.slide_index: dots[i].write("●")
            elif dots[i].button("○", key=f"dot_{i}"):
                st.session_state.slide_index = i
                st.session_state.last_slide_time = time.time()
                st.rerun()
    st.markdown("---")
