import streamlit as st
from services.sidebar import render_sidebar
from auth import (
    logout
)

from services.load_css import load_css

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# =====================================================
# AUTH CHECK
# =====================================================

if "user" not in st.session_state:

    st.warning("Please login first")

    st.switch_page("app.py")

    st.stop()

if st.session_state.user is None:

    st.warning("Please login first")

    st.switch_page("app.py")

    st.stop()

# =========== SIDEBAR =================================
render_sidebar()
# =====================================================
    # ==========================================
    # USER
    # ==========================================

    st.success(
        f"Welcome {st.session_state.user.email}"
    )


# =====================================================
# HEADER
# =====================================================

    st.title("👤 Profile")

# =====================================================
# PROFILE INFO
# =====================================================

st.subheader("Account Information")

st.write(
    f"📧 Email: {st.session_state.user.email}"
)

# Optional metadata
try:

    created_at = st.session_state.user.created_at

    st.write(f"📅 Account Created: {created_at}")

except:
    pass