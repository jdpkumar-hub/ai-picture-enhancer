import streamlit as st

from auth import supabase

st.title("📜 History")

user_email = st.session_state.user.email

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

if not rows:

    st.info("No history found")

for row in rows:

    st.subheader(row["enhancement_type"])

    col1, col2 = st.columns(2)

    with col1:
        st.image(row["original_url"])

    with col2:
        st.image(row["enhanced_url"])

    st.caption(row["created_at"])

    st.divider()