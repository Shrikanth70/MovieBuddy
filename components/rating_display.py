import streamlit as st

def render_ratings(omdb_data):
    """Refined ratings display (STEP 7 & 10)."""
    if not omdb_data or omdb_data.get("Response") == "True" is False:
        return

    st.markdown("### Ratings")
    
    # Extract ratings
    ratings_dict = {r['Source']: r['Value'] for r in omdb_data.get('Ratings', [])}
    imdb_score = omdb_data.get("imdbRating", "N/A")
    rt_score = ratings_dict.get("Rotten Tomatoes", "N/A")
    meta_score = omdb_data.get("Metascore", "N/A")

    cols = st.columns(3)
    
    # IMDb
    with cols[0]:
        st.markdown(f"""
            <div style="background: #f5c518; color: black; padding: 10px; border-radius: 8px; text-align: center;">
                <div style="font-size: 12px; font-weight: bold;">IMDb</div>
                <div style="font-size: 20px; font-weight: 800;">{imdb_score}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Rotten Tomatoes
    with cols[1]:
        st.markdown(f"""
            <div style="background: #fa320a; color: white; padding: 10px; border-radius: 8px; text-align: center;">
                <div style="font-size: 12px; font-weight: bold;">Rotten Tomatoes</div>
                <div style="font-size: 20px; font-weight: 800;">{rt_score}</div>
            </div>
        """, unsafe_allow_html=True)

    # Metacritic
    with cols[2]:
        st.markdown(f"""
            <div style="background: #333; color: white; padding: 10px; border-radius: 8px; text-align: center;">
                <div style="font-size: 12px; font-weight: bold;">Metacritic</div>
                <div style="font-size: 20px; font-weight: 800;">{meta_score}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
