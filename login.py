import streamlit as st

from auth import (
    google_login,
    send_otp_login,
    verify_otp
)

# =====================================================
# LOGIN PAGE
# =====================================================

def show_login():

    st.title("🚀 AI Product Image Cleaner")

    st.subheader("Login")

    # =================================================
    # GOOGLE LOGIN
    # =================================================

    google_url = google_login()

    if google_url:

        st.link_button(
            "🔵 Continue with Google",
            google_url
        )

    st.markdown("---")

