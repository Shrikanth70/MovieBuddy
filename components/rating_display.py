import streamlit as st

def render_ratings(omdb_data):
    """Refined ratings display - Only shows available cards (STEP 7 & 10)."""
    if not omdb_data or omdb_data.get("Response") == "False":
        return

    # Extract ratings
    ratings_dict = {r['Source']: r['Value'] for r in omdb_data.get('Ratings', [])}
    imdb_score = omdb_data.get("imdbRating")
    rt_score = ratings_dict.get("Rotten Tomatoes")
    meta_score = omdb_data.get("Metascore")

    # Filter out "N/A" values
    valid_ratings = []
    if imdb_score and imdb_score != "N/A":
        valid_ratings.append(("IMDb", imdb_score, "#f5c518", "black"))
    if rt_score and rt_score != "N/A":
        valid_ratings.append(("Rotten Tomatoes", rt_score, "#fa320a", "white"))
    if meta_score and meta_score != "N/A":
        valid_ratings.append(("Metacritic", meta_score, "#333", "white"))

    if not valid_ratings:
        return

    st.markdown("### Ratings")
    cols = st.columns(len(valid_ratings))
    
    for i, (label, score, bg, text_color) in enumerate(valid_ratings):
        with cols[i]:
            st.markdown(f"""
                <div style="background: {bg}; color: {text_color}; padding: 10px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 12px; font-weight: bold;">{label}</div>
                    <div style="font-size: 20px; font-weight: 800;">{score}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
