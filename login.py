import streamlit as st

from auth import (
    send_otp,
    verify_otp,
    google_login,
    supabase
)

# =====================================================
# HANDLE GOOGLE CALLBACK
# =====================================================

query_params = st.query_params

if "code" in query_params:

    try:

        code = query_params["code"]

        supabase.auth.exchange_code_for_session({
            "auth_code": code
        })

        user_data = supabase.auth.get_user()

        if user_data and user_data.user:

            st.session_state.user = user_data.user

            st.query_params.clear()

            st.rerun()

    except Exception as e:

        st.error(f"Google login failed: {str(e)}")

# =====================================================
# UI
# =====================================================

st.title("🚀 AI Product Image Cleaner")

st.subheader("Login")

# =====================================================
# GOOGLE LOGIN
# =====================================================

google_url = google_login()

if google_url:

    st.link_button(
        "🔵 Continue with Google",
        google_url
    )

st.markdown("---")

# =====================================================
# EMAIL OTP LOGIN
# =====================================================

email = st.text_input("Email")

if st.button("Send OTP"):

    try:

        send_otp(email)

        st.session_state.otp_email = email

        st.success("OTP sent to your email")

    except Exception as e:

        st.error(str(e))

# =====================================================
# VERIFY OTP
# =====================================================

if "otp_email" in st.session_state:

    otp = st.text_input("Enter OTP")

    if st.button("Verify OTP"):

        try:

            res = verify_otp(
                st.session_state.otp_email,
                otp
            )

            if res and res.user:

                st.session_state.user = res.user

                st.success("Login successful!")

                st.rerun()

            else:

                st.error("Invalid OTP")

        except Exception as e:

            st.error(str(e))