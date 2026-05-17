import streamlit as st
from PIL import Image
from services.sidebar import render_sidebar
from services.load_css import load_css
from services.product_photo_service import product_photo_ai
from enhance import image_to_bytes

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

st.title("🛍 AI Product Photography")


# =========== SIDEBAR =================================
render_sidebar()
# =====================================================

uploaded = st.file_uploader(
    "Upload Product Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded:

    img = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Original")

    if st.button("Generate Product Photo"):

        result = product_photo_ai(img)

        with col2:
            st.image(result, caption="AI Product")

        img_bytes = image_to_bytes(
            result,
            fmt="PNG"
        )

        st.download_button(
            "📥 Download Product Photo",
            data=img_bytes,
            file_name="product_ai.png",
            mime="image/png"
        )