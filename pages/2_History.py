import streamlit as st

from auth import supabase

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
# PAGE
# =====================================================

st.title("📜 History")

# =====================================================
# USER EMAIL
# =====================================================

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
# DISPLAY
# =====================================================

for row in rows:

    st.subheader(row["enhancement_type"])

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            row["original_url"],
            caption="Original"
        )

    with col2:

        st.image(
            row["enhanced_url"],
            caption="Enhanced"
        )

    st.caption(row["created_at"])

    st.divider()