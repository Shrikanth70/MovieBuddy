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
        [data-testid="stSidebarNav"] {display: none;}
        .stButton button { width: 100%; border-radius: 10px; }
        .gold-text { color: #FFB000; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
