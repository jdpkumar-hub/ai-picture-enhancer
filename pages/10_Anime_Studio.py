import streamlit as st
from PIL import Image
from services.sidebar import render_sidebar
from services.load_css import load_css
from services.anime_service import anime_style
from enhance import image_to_bytes
from services.auth_guard import require_login

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

st.title("🎨 Anime Studio")

# =============LOGIN REQUIED ==========================
require_login()
# =====================================================

# =========== SIDEBAR =================================
render_sidebar()
# =====================================================

uploaded = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded:

    img = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Original")

    if st.button("Convert To Anime"):

        result = anime_style(img)

        with col2:
            st.image(result, caption="Anime")

        img_bytes = image_to_bytes(
            result,
            fmt="PNG"
        )

        st.download_button(
            "📥 Download Anime",
            data=img_bytes,
            file_name="anime.png",
            mime="image/png"
        )