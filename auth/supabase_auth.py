import streamlit as st
from services import supabase_api as auth_service

def render_login_page():
    """Refined auth screen with balanced 1.2:1 ratio and vertical centering."""
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True) # Top spacing
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1A4D2E 0%, #07090D 100%); padding: 4rem; border-radius: 30px; height: 500px; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(255,255,255,0.05);">
                <h1 style="color: #FFB000; font-size: 56px; margin-bottom: 0;">MovieBuddy</h1>
                <p style="color: white; font-size: 20px; opacity: 0.8; font-weight: 400;">The ultimate cinematic discovery platform.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True) # Vertical centering for form
        st.markdown('<h2 style="font-weight: 800; margin-bottom: 2rem;">Welcome Back</h2>', unsafe_allow_html=True)
        mode = st.radio("Access", ["Login", "Sign Up"], horizontal=True, key="auth_radio", label_visibility="collapsed")
        email = st.text_input("Email", key="auth_email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", key="auth_pass", placeholder="Enter your password")
        
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
