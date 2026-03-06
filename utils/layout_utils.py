import streamlit as st

def set_global_page_config():
    st.set_page_config(
        page_title="MovieBuddy",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def inject_global_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Hide Streamlit elements */
        [data-testid="stSidebarNav"] {display: none;}
        header {visibility: hidden;}
        
        /* Remove Unwanted Whitespace */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0rem !important;
            padding-left: 5% !important;
            padding-right: 5% !important;
        }
        .stApp {
            background: #0D0F12;
            color: #E0E0E0;
        }
        [data-testid="stHeader"] { height: 0; }
        
        /* Card Hover Effects */
        div[data-testid="stImage"] img {
            border-radius: 12px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            aspect-ratio: 2/3;
            object-fit: cover;
        }
        div[data-testid="stImage"] img:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }

        /* Button Styling */
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
            background: rgba(255, 176, 0, 0.05);
            color: #FFB000;
            border: 1px solid rgba(255, 176, 0, 0.4);
            height: 42px;
        }
        .stButton button:hover {
            background: #FFB000;
            color: black;
            border-color: #FFB000;
        }
        
        /* Secondary elements */
        .gold-text { color: #FFB000; font-weight: 800; }
        .stCaption { opacity: 0.6; font-size: 0.85rem; margin-bottom: 5px; }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0D0F12; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #444; }

        /* Grid & Container Polish */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding: 12px !important;
            border-radius: 16px !important;
            background: rgba(255, 255, 255, 0.02);
            height: 100%;
        }
        
        /* Section Headers */
        h3 {
            margin-top: 2.5rem !important;
            margin-bottom: 1.5rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        /* PERMANENT: Movie Card Title Alignment */
        .movie-title-container {
            height: 40px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
            margin-bottom: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            line-height:1.2;
            color: white;
        }

        /* Navbar & Logo Styling */
        .top-navbar {
            padding: 0 5%;
            margin-bottom: 2rem;
        }
        .logo-text {
            color: #FFB000;
            font-size: 1.8rem;
            font-weight: 900;
            text-decoration: none;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .logo-text:hover {
            opacity: 0.8;
        }

        /* Spacing Fix */
        .stVerticalBlock { gap: 0rem !important; }
        </style>
    """, unsafe_allow_html=True)
