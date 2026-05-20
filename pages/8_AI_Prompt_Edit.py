import streamlit as st
from PIL import Image
from services.sidebar import render_sidebar
from services.load_css import load_css
from services.prompt_edit_service import prompt_edit
from enhance import image_to_bytes
from services.auth_guard import require_login

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

st.title("🤖 AI Prompt Editing")

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

prompt = st.text_input(
    "Describe edit",
    placeholder="Make image brighter and sharper"
)

if uploaded:

    img = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Original")

    if st.button("Apply AI Edit"):

        result = prompt_edit(
            img,
            prompt
        )

        with col2:
            st.image(result, caption="AI Edited")

        img_bytes = image_to_bytes(
            result,
            fmt="PNG"
        )

        st.download_button(
            "📥 Download Edited Image",
            data=img_bytes,
            file_name="ai_edit.png",
            mime="image/png"
        )