import streamlit as st

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

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.image(
        "assets/logo.png",
        width=240
    )

    st.caption("🚀 Smart image Enhancer")

    st.markdown(
        "<div class='sidebar-divider'></div>",
        unsafe_allow_html=True
    )

    # ==========================================
    # MENU
    # ==========================================

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.switch_page("app.py")
        
    if st.button("✨ Enhance",use_container_width=True):
            st.switch_page("pages/1_Enhance.py")
       

    if st.button(
        "📜 History",
        use_container_width=True
    ):
        st.switch_page("pages/2_History.py")

    st.markdown(
        "<div class='sidebar-divider'></div>",
        unsafe_allow_html=True
    )

    # ==========================================
    # LOGOUT
    # ==========================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

        st.session_state.user = None

        st.switch_page("app.py")

        st.stop()

    # ==========================================
    # USER
    # ==========================================

    st.success(
        f"Welcome {st.session_state.user.email}"
    )


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