import streamlit as st

def set_global_page_config():
    st.set_page_config(
        page_title="MovieBuddy",
        layout="wide",
        initial_sidebar_state="expanded"
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
        
        /* Premium Background & Sidebar */
        .stApp {
            background: #0D0F12;
            color: #E0E0E0;
        }
        
        [data-testid="stSidebar"] {
            background-color: rgba(18, 22, 27, 0.8) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
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
        </style>
    """, unsafe_allow_html=True)
