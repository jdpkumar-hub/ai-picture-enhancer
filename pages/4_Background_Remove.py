import streamlit as st
from PIL import Image
from services.sidebar import render_sidebar
from services.load_css import load_css
from services.remove_bg_service import remove_background
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
# =========== SIDEBAR =================================

st.title("🪄 Background Removal")

uploaded = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded:

    img = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Original")

    if st.button("Remove Background"):

        result = remove_background(img)

        with col2:
            st.image(result, caption="Transparent")

        img_bytes = image_to_bytes(
            result,
            fmt="PNG"
        )

        st.download_button(
            "📥 Download PNG",
            data=img_bytes,
            file_name="removed_bg.png",
            mime="image/png"
        )