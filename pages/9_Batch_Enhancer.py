import streamlit as st
from PIL import Image
from services.sidebar import render_sidebar
from services.load_css import load_css
from enhance import enhance_photo

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

st.title("📦 Batch Enhancer")
# =========== SIDEBAR =================================
render_sidebar()
# =====================================================
files = st.file_uploader(
    "Upload Multiple Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if files:

    st.success(f"{len(files)} images uploaded")

    if st.button("Enhance All"):

        for file in files:

            img = Image.open(file)

            result = enhance_photo(
                img,
                "HD Enhance"
            )

            st.image(
                result,
                caption=file.name
            )