import streamlit as st
from pathlib import Path

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
        "👤 Profile",
        use_container_width=True
    ):
        st.switch_page("pages/3_Profile.py")

    st.markdown(
        "<div class='sidebar-divider'></div>",
        unsafe_allow_html=True
    )
    if st.button(
        "🪄 Remove Background",
        use_container_width=True
    ):
        st.switch_page(
            "pages/4_Background_Remove.py"
        )

    if st.button(
        "🧓 Restore Photo",
        use_container_width=True
    ):
        st.switch_page(
            "pages/5_Old_Photo_Restore.py"
        )

    if st.button(
        "🧼 Remove Objects",
        use_container_width=True
    ):
        st.switch_page(
            "pages/6_Object_Removal.py"
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