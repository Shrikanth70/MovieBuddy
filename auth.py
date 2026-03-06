import streamlit as st
import supabase_service as auth

def render_auth_page():
    """Render a single-instance authentication page with unique keys and fixed layout."""
    # Use col1 (1.3) for Hero and col2 (1.0) for Form
    col1, col2 = st.columns([1.3, 1], gap="large")
    
    with col1:
        # Single Hero Card (ISSUE: No duplication)
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1A4D2E 0%, #07090D 100%); padding: 4rem; border-radius: 30px; height: 600px; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(255,255,255,0.05); margin-top: 50px;">
                <h1 style="font-size: 48px; color: #FFB000;">MovieBuddy</h1>
                <p style="color: white; font-size: 18px; opacity: 0.8;">Your personal gateway to cinematic excellence. Join us and explore thousands of movies.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
        
        # Check for email verification code in URL
        if st.query_params.get("code"):
            st.success("✅ Email verified! Please sign in below.")
            st.query_params.clear()

        # Auth Toggle with unique key (ISSUE: radio duplication)
        auth_mode = st.radio(
            "Access Mode", 
            ["Login", "Sign Up"], 
            horizontal=True, 
            key="auth_mode_selector_unique"
        )
        
        email = st.text_input("Email", key="auth_email_unique")
        password = st.text_input("Password", type="password", key="auth_password_unique")
        
        submit_label = "Sign In" if auth_mode == "Login" else "Create Account"
        
        if st.button(submit_label, type="primary", use_container_width=True, key="auth_submit_unique"):
            if not email or not password:
                st.warning("Please enter your credentials.")
            else:
                with st.spinner("Processing..."):
                    if auth_mode == "Login":
                        res, err = auth.sign_in(email, password)
                        if not err:
                            st.session_state.user = res.user
                            st.rerun()
                        else:
                            st.error(f"Login failed: {err}")
                    else:
                        res, err = auth.sign_up(email, password)
                        if not err:
                            st.success("Verification email sent! Check your inbox.")
                        else:
                            st.error(f"Signup failed: {err}")
