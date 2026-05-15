import streamlit as st

from auth import (
    login,
    signup,
    reset_password,
    google_login
)

# =====================================================
# LOGIN SCREEN
# =====================================================

def show_login():

    st.title("🚀 AI Product Image Cleaner")

    menu = st.selectbox(
        "Menu",
        ["Login", "Signup", "Reset Password"]
    )

    # =================================================
    # LOGIN
    # =================================================

    if menu == "Login":

        st.subheader("Login")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            try:

                res = login(email, password)

                if res.user:

                    st.session_state.user = res.user

                    st.success("Login successful!")

                    st.switch_page(
                        "pages/1_Enhance.py"
                    )

            except Exception as e:

                st.error(str(e))

        st.markdown("---")

        google_url = google_login()

        if google_url:

            st.link_button(
                "🔵 Continue with Google",
                google_url
            )

    # =================================================
    # SIGNUP
    # =================================================

    elif menu == "Signup":

        st.subheader("Create Account")

        email = st.text_input(
            "Signup Email"
        )

        password = st.text_input(
            "Signup Password",
            type="password"
        )

        if st.button("Create Account"):

            try:

                signup(email, password)

                st.success(
                    "Account created successfully"
                )

            except Exception as e:

                st.error(str(e))

    # =================================================
    # RESET PASSWORD
    # =================================================

    elif menu == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input(
            "Reset Email"
        )

        if st.button("Send Reset Email"):

            try:

                reset_password(email)

                st.success(
                    "Reset email sent"
                )

            except Exception as e:

                st.error(str(e))