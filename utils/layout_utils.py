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
        
        /* Premium Background */
        .stApp {
            background: #0D0F12;
            color: #E0E0E0;
        }

        /* Card Hover Effects */
        div[data-testid="stImage"] img {
            border-radius: 12px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        div[data-testid="stImage"] img:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }

        /* Button Styling */
        .stButton button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
            background: rgba(255, 176, 0, 0.1);
            color: #FFB000;
            border: 1px solid #FFB000;
        }
        .stButton button:hover {
            background: #FFB000;
            color: black;
            border-color: #FFB000;
        }
        
        /* Secondary elements */
        .gold-text { color: #FFB000; font-weight: 800; }
        .stCaption { opacity: 0.6; font-size: 0.85rem; }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0D0F12; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #444; }

        /* Grid & Container Polish */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding: 10px !important;
            border-radius: 15px !important;
            background: rgba(255, 255, 255, 0.02);
        }
        
        /* Section Headers */
        h3 {
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        /* Movie Card Title Alignment */
        .movie-title-container {
            height: 45px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            margin-bottom: 5px;
            font-weight: 600;
            font-size: 0.95rem;
            line-height: 1.2;
        }

        /* Top Navbar Styling */
        .top-navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: rgba(13, 15, 18, 0.95);
            backdrop-filter: blur(15px);
            z-index: 999;
            display: flex;
            align-items: center;
            padding: 0 5%;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Content Padding for Fixed Navbar */
        .main-content {
            margin-top: 80px;
        }
        /* Logo Button Styling */
        div[data-testid="stHeader"] + div button[key="nav_logo"], 
        button[key="nav_logo"] {
            background: transparent !important;
            border: none !important;
            color: #FFB000 !important;
            font-size: 1.5rem !important;
            font-weight: 800 !important;
            padding: 0 !important;
            text-align: left !important;
        }
        </style>
    """, unsafe_allow_html=True)
