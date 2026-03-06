import streamlit as st
from services import supabase_api as auth_service

def render_login_page():
    """Dedicated auth screen with fixed layout (ISSUE: No disappearing navbar)."""
    col1, col2 = st.columns([1.3, 1], gap="large")
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1A4D2E 0%, #07090D 100%); padding: 4rem; border-radius: 30px; height: 600px; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(255,255,255,0.05); margin-top: 50px;">
                <h1 style="color: #FFB000; font-size: 48px;">MovieBuddy</h1>
                <p style="color: white; font-size: 18px; opacity: 0.8;">Explore the world of cinema. Sign in to sync your watchlist.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
        mode = st.radio("Access", ["Login", "Sign Up"], horizontal=True, key="auth_radio")
        email = st.text_input("Email", key="auth_email")
        password = st.text_input("Password", type="password", key="auth_pass")
        
        if st.button("Enter MovieBuddy", type="primary", use_container_width=True):
            if mode == "Login":
                res, err = auth_service.sign_in(email, password)
                if not err:
                    st.session_state.user = res.user
                    st.rerun()
                else: st.error(err)
            else:
                res, err = auth_service.sign_up(email, password)
                if not err: st.success("Verification email sent!")
                else: st.error(err)
