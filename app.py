import streamlit as st
from auth import get_user

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Product Image Cleaner",
    page_icon="🚀",
    layout="wide"
)

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