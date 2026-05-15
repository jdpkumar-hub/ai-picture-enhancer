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

    # =================================================
    # OTP LOGIN
    # =================================================

    email = st.text_input("Email")

    if st.button("Send OTP"):

        if email:

            try:

                send_otp_login(email)

                st.session_state.otp_email = email

                st.success("OTP sent to email")

            except Exception as e:

                st.error(f"OTP failed: {str(e)}")

        else:

            st.warning("Enter email")

    # =================================================
    # VERIFY OTP
    # =================================================

    if "otp_email" in st.session_state:

        otp = st.text_input("Enter OTP")

        if st.button("Verify OTP"):

            try:

                res = verify_otp(
                    st.session_state.otp_email,
                    otp
                )

                if res.user:

                    st.session_state.user = res.user

                    st.success("Login successful!")

                    st.switch_page("pages/1_Enhance.py")

            except Exception as e:

                st.error(f"Verification failed: {str(e)}")