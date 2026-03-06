import streamlit as st

def set_global_page_config():
    """Set the initial Streamlit page configuration."""
    st.set_page_config(
        page_title="MovieBuddy | Home",
        page_icon="🎞️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def inject_global_css():
    """Inject all global CSS for the dashboard, including fixed sidebar logic."""
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Montserrat:wght@400;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    
    <style>
    :root {
        --bg-dark: #07090D;
        --bg-card: #12161F;
        --bg-sidebar: #0D1117;
        --gold: #FFB000;
        --text-main: #FFFFFF;
        --text-muted: #8B949E;
        --radius: 12px;
        --transition: 0.3s ease;
    }

    * { font-family: 'Poppins', sans-serif; }

    /* Hide Streamlit default elements */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-main);
    }

    /* Fixed Sidebar Logic */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
        position: fixed !important;
    }

    @media (min-width: 992px) {
        .block-container {
            margin-left: 300px !important;
            max-width: calc(100% - 300px) !important;
        }
    }

    /* Sidebar Button Styling */
    div.stButton > button {
        background: transparent !important;
        color: var(--text-muted) !important;
        border: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding-left: 0px !important;
        transition: var(--transition) !important;
    }

    div.stButton > button:hover {
        color: var(--gold) !important;
        background: rgba(255, 176, 0, 0.05) !important;
        transform: translateX(5px);
    }
    
    .gold-text { color: var(--gold); }
    
    /* Movie Card Styling */
    .movie-card-container {
        transition: var(--transition);
        border-radius: var(--radius);
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .movie-card-container:hover {
        transform: scale(1.05);
        border-color: var(--gold);
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: var(--gold) !important;
    }
    </style>
    """, unsafe_allow_html=True)
