import streamlit as st
from PIL import Image
from services.sidebar import render_sidebar
from services.load_css import load_css
from services.restore_service import restore_old_photo
from enhance import image_to_bytes
from services.auth_guard import require_login

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# =============LOGIN REQUIED ==========================
require_login()
# =====================================================

# =========== SIDEBAR =================================
render_sidebar()
# =====================================================

st.title("🧓 Old Photo Restore")

uploaded = st.file_uploader(
    "Upload Old Photo",
    type=["png", "jpg", "jpeg"]
)

if uploaded:

    img = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Old Photo")

    if st.button("Restore Photo"):

        result = restore_old_photo(img)

        with col2:
            st.image(result, caption="Restored")

        img_bytes = image_to_bytes(
            result,
            fmt="PNG"
        )

        st.download_button(
            "📥 Download Restored Photo",
            data=img_bytes,
            file_name="restored_photo.png",
            mime="image/png"
        )