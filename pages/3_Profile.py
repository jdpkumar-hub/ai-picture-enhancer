import streamlit as st
from auth import logout

# =====================================================
# AUTH CHECK
# =====================================================

if "user" not in st.session_state:

    st.switch_page("app.py")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.success(
    f"Welcome {st.session_state.user.email}"
)

if st.sidebar.button("Logout"):

    logout()

    st.session_state.user = None

    st.switch_page("app.py")

# =====================================================
# PAGE
# =====================================================

st.title("👤 Profile")

st.write(
    f"Logged in as: {st.session_state.user.email}"
)