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

def upload_image(file_bytes, folder="originals"):

    filename = f"{folder}/{uuid.uuid4()}.png"

    supabase.storage.from_("images").upload(
        filename,
        file_bytes,
        {"content-type": "image/png"}
    )

    public_url = supabase.storage.from_("images").get_public_url(filename)

    return public_url, filename
    

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
# =========================================
# DELETE HISTORY
# =========================================
def delete_history_item(item_id, original_path, enhanced_path):
    try:
        # Delete images from bucket
        supabase.storage.from_("images").remove([
            original_path,
            enhanced_path
        ])

        # Delete DB row
        supabase.table("history").delete().eq("id", item_id).execute()

        return True

    except Exception as e:
        print(e)
        return False


# =========================================
# DELETE HISTORY
# =========================================        
