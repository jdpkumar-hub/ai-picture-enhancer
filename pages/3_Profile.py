import streamlit as st

from auth import (
    logout
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

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
    "assets/logo.png",
    width=120
)

st.sidebar.markdown("## AI Enhance")

st.sidebar.success(
    f"Welcome {st.session_state.user.email}"
)

if st.sidebar.button("✨ Enhance"):

    st.switch_page("pages/1_Enhance.py")

if st.sidebar.button("📜 History"):

    st.switch_page("pages/2_History.py")

if st.sidebar.button("🚪 Logout"):

    logout()

    st.session_state.user = None

    st.switch_page("app.py")

    st.stop()

# =====================================================
# HEADER
# =====================================================

col1, col2 = st.columns([1, 5])

with col1:

    st.image(
        "assets/logo.png",
        width=80
    )

with col2:

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