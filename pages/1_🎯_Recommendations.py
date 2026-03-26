import streamlit as st
from recommendation import recommend
from utils import search_movie, get_poster

st.set_page_config(page_title="Recommendations", layout="wide")

st.title("🎯 Get Movie Recommendations")

col_back, _ = st.columns([1.5, 8.5])
with col_back:
    st.markdown(f'''
        <div class="back-btn-container">
            <a href="/?home=true" target="_self" class="back-pill-btn">
                <span style="margin-right: 8px;">←</span> BACK
            </a>
        </div>
    ''', unsafe_allow_html=True)

# Load movie titles from ML dataset
import pickle
import os

pkl_path = "movies.pkl"
try:
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)
        if isinstance(data, tuple):
            movies = data[0]
        else:
            movies = data
except:
    movies = pd.DataFrame(columns=['title'])

if not movies.empty:
    selected_movie = st.selectbox(
        "Choose a movie to find similar ones",
        movies['title'].values
    )
else:
    st.error("Movie dataset not found.")
    st.stop()

if st.button("Recommend Similar Movies"):
    with st.spinner("Finding recommendations..."):
        recommended_titles = recommend(selected_movie)
        
    if recommended_titles:
        st.markdown(f"### Because you liked **{selected_movie}**")
        
        # Use premium grid for recommendations
        recs_data = []
        for title in recommended_titles:
            import tmdb_service as tmdb
            results = tmdb.search_movies(title)
            if results:
                recs_data.append(results[0])
        
        if recs_data:
            import components as ui
            ui.render_movie_grid(recs_data, key_prefix="rec_page", columns=4)
        else:
            for title in recommended_titles:
                st.write(f"• {title}")
    else:
        st.info("No similar movies found in our local database.")