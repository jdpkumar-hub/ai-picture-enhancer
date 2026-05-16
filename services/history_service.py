from datetime import datetime
from auth import supabase


def save_history(
    user_email,
    enhancement_type,
    original_path,
    enhanced_path
):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    original_name = f"{timestamp}_original.png"

    enhanced_name = f"{timestamp}_enhanced.png"

    # ==========================================
    # Upload Original
    # ==========================================

    with open(original_path, "rb") as f:

        supabase.storage.from_("images").upload(
            original_name,
            f
        )

    # ==========================================
    # Upload Enhanced
    # ==========================================

    with open(enhanced_path, "rb") as f:

        supabase.storage.from_("images").upload(
            enhanced_name,
            f
        )

    # ==========================================
    # Public URLs
    # ==========================================

    original_url = supabase.storage.from_(
        "images"
    ).get_public_url(original_name)

    enhanced_url = supabase.storage.from_(
        "images"
    ).get_public_url(enhanced_name)

    # ==========================================
    # Save Database Record
    # ==========================================

    supabase.table("history").insert({

        "user_email": user_email,

        "original_url": original_url,

        "enhanced_url": enhanced_url,

        "enhancement_type": enhancement_type

    }).execute()