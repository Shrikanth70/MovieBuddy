import streamlit as st
import tmdb_service as tmdb
import components as ui

def render_trending_page():
    col_back, _ = st.columns([1.5, 8.5])
    with col_back:
        st.markdown(f'''
            <div class="back-btn-container">
                <a href="/?home=true" target="_self" class="back-pill-btn">
                    <span style="margin-right: 8px;">←</span> BACK
                </a>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('<div class="ott-title" style="font-size: 32px; margin-bottom: 20px;">Trending This Week</div>', unsafe_allow_html=True)
    weekly = tmdb.get_trending_weekly(limit=24)
    ui.render_movie_grid(weekly, key_prefix="page_trend", columns=5)

if __name__ == "__main__":
    try:
        ui.inject_custom_css()
    except Exception as e:
        st.error(f"CSS injection failed: {e}")
        print(f"CSS Error: {e}")
    render_trending_page()
