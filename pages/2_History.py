import streamlit as st
from pathlib import Path
from services.sidebar import render_sidebar

from auth import (
    supabase,
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
    st.switch_page("app.py")
    st.stop()

if st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

# =====================================================
# SIDEBAR
# =====================================================
render_sidebar()
# =====================================================
# PAGE
# =====================================================

st.title("📜 History")
user_email = st.session_state.user.email

# =====================================================
# FETCH HISTORY
# =====================================================

response = supabase.table(
    "history"
).select("*").eq(
    "user_email",
    user_email
).order(
    "created_at",
    desc=True
).execute()

rows = response.data

# =====================================================
# EMPTY
# =====================================================

if not rows:

    st.info("No history found")

# =====================================================
# DISPLAY HISTORY
# =====================================================

for row in rows:

    st.subheader(row["enhancement_type"])

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            row["original_url"],
            caption="Original",
            use_container_width=True
        )

    with col2:

        st.image(
            row["enhanced_url"],
            caption="Enhanced",
            use_container_width=True
        )

    st.caption(row["created_at"])

    # ==========================================
    # DELETE BUTTON
    # ==========================================

    if st.button(
        f"🗑 Delete",
        key=row["id"]
    ):

        try:

            # Delete DB row
            supabase.table("history").delete().eq(
                "id",
                row["id"]
            ).execute()

            st.success("History deleted")

            st.rerun()

        except Exception as e:

            st.error(f"Delete failed: {str(e)}")

    st.divider()