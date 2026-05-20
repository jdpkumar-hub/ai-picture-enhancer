import streamlit as st


def require_login():

    if (
        "user" not in st.session_state
        or st.session_state.user is None
    ):

        st.warning("Please login first")

        st.switch_page("app.py")

        st.stop()