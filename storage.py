from supabase import create_client
import streamlit as st
import uuid

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================================
# UPLOAD IMAGE
# =========================================
def upload_image(file_bytes, filename):

    path = f"{uuid.uuid4()}_{filename}"

    supabase.storage.from_("images").upload(
        path,
        file_bytes
    )

    url = supabase.storage.from_("images").get_public_url(path)

    return url

# =========================================
# SAVE HISTORY
# =========================================
def save_history(email, original_url, enhanced_url):

    supabase.table("image_history").insert({
        "user_email": email,
        "original_url": original_url,
        "enhanced_url": enhanced_url
    }).execute()

# =========================================
# GET HISTORY
# =========================================
def get_history(email):

    data = supabase.table("image_history") \
        .select("*") \
        .eq("user_email", email) \
        .order("created_at", desc=True) \
        .execute()

    return data.data
