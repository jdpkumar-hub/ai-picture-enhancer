import streamlit as st
from PIL import Image

from services.load_css import load_css
from services.restore_service import restore_old_photo
from enhance import image_to_bytes

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# =====================================
# SIDEBAR
# =====================================

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

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

    if st.button("✨ Enhance", use_container_width=True):
        st.switch_page("pages/1_Enhance.py")

    if st.button("🪄 Remove Background", use_container_width=True):
        st.switch_page("pages/4_Background_Remove.py")

    if st.button("🧓 Restore Photo", use_container_width=True):
        st.switch_page("pages/5_Old_Photo_Restore.py")

    if st.button("🧼 Remove Objects", use_container_width=True):
        st.switch_page("pages/6_Object_Removal.py")


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