import streamlit as st
from pathlib import Path

from auth import (
    supabase,
    get_user
)

from login import show_login
from services.load_css import load_css

st.markdown(
    load_css(),
    unsafe_allow_html=True
)
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Product Image Cleaner",
    page_icon="🚀",
    layout="wide"
)

hide_streamlit_style = """
<style>

[data-testid="stSidebarNav"] {
    display: none;
}

</style>
"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)

st.markdown("""
<style>

section[data-testid="stSidebar"] {
    width: 120px !important;
}

</style>
""", unsafe_allow_html=True)
#=====================================SIDE BAR ========
with st.sidebar:

    st.image(
        "assets/logo.png",
        width=220
    )

    st.markdown("# AI Image Enhancer")

    st.caption("🚀 Smart image Enhancer")

    st.markdown(
        "<div class='sidebar-divider'></div>",
        unsafe_allow_html=True
    )

    if st.button("🏠 Home"):
        st.switch_page("app.py")

    if st.button("✨ Enhance"):
        st.switch_page("pages/1_Enhance.py")

    if st.button("📜 History"):
        st.switch_page("pages/2_History.py")

    if st.button("👤 Profile"):
        st.switch_page("pages/3_Profile.py")

    st.markdown(
        "<div class='sidebar-divider'></div>",
        unsafe_allow_html=True
    )

    st.caption("Built by JDP Kumar 🚀")
# =====================================================
# QUERY PARAMS
# =====================================================

query_params = st.query_params

# =====================================================
# PASSWORD RECOVERY
# =====================================================

if "type" in query_params:

    if query_params["type"] == "recovery":

        st.title("🔒 Reset Password")

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Update Password"):

            if new_password != confirm_password:

                st.error("Passwords do not match")

            elif len(new_password) < 6:

                st.error("Password too short")

            else:

                try:

                    supabase.auth.update_user({
                        "password": new_password
                    })

                    st.success(
                        "Password updated successfully!"
                    )

                    st.info(
                        "Please login again"
                    )

                except Exception as e:

                    st.error(str(e))

        st.stop()

# =====================================================
# GOOGLE LOGIN CALLBACK
# =====================================================

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

            st.switch_page("pages/1_Enhance.py")

    except Exception as e:

        st.error(f"Google login failed: {str(e)}")

# =====================================================
# SESSION
# =====================================================

if "user" not in st.session_state:

    st.session_state.user = get_user()

# =====================================================
# ROUTING
# =====================================================

if st.session_state.user:

    st.switch_page("pages/1_Enhance.py")

else:

    show_login()