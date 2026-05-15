import streamlit as st

from auth import (
    supabase,
    get_user
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Product Image Cleaner",
    page_icon="🚀",
    layout="wide"
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

            # Remove code from URL
            st.query_params.clear()

            st.rerun()

    except Exception as e:

        st.error(f"Google login failed: {str(e)}")

# =====================================================
# RESTORE USER SESSION
# =====================================================

if "user" not in st.session_state:
    st.session_state.user = get_user()

# =====================================================
# ROUTING
# =====================================================

if st.session_state.user:

    st.switch_page("pages/1_Enhance.py")

else:

    from login import *