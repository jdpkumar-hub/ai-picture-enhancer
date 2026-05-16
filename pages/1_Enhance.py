import streamlit as st
from PIL import Image
import io

from auth import logout
from enhance import (
    clean_product_image,
    enhance_photo,
    image_to_bytes
)

# =====================================================
# AUTH CHECK
# FIX: st.stop() added so the rest of the page does NOT
#      execute for unauthenticated users after redirect.
# =====================================================

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.success(
    f"Welcome {st.session_state.user.email}"
)

if st.sidebar.button("Logout"):
    logout()
    st.session_state.user = None
    st.switch_page("app.py")
    st.stop()

# =====================================================
# MAIN PAGE
# =====================================================

st.title("🚀 AI Enhance Workspace")

st.write("Upload an image and apply AI enhancement.")

# =====================================================
# MODE SELECTOR
# =====================================================

photo_mode = st.selectbox(
    "Enhancement Mode",
    [
        "HD Enhance",
        "Portrait Enhance",
        "Ultra Sharp",
        "Product Clean"
    ]
)

# =====================================================
# UPLOAD
# =====================================================

uploaded = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

# =====================================================
# PROCESS
# =====================================================

if uploaded:

    img = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            img,
            caption="Original Image",
            use_container_width=True
        )

    if st.button("✨ Enhance Image"):

        with st.spinner("AI enhancing image..."):

            if photo_mode == "Product Clean":
                result = clean_product_image(img)
            else:
                result = enhance_photo(img, photo_mode)

        with col2:
            st.image(
                result,
                caption="Enhanced Image",
                use_container_width=True
            )

        # =============================================
        # DOWNLOAD
        # FIX: use BytesIO buffer instead of writing to
        #      disk — disk writes fail on Streamlit Cloud.
        # =============================================

        img_bytes = image_to_bytes(result, fmt="PNG")

        st.download_button(
            label="📥 Download Enhanced Image",
            data=img_bytes,
            file_name="enhanced_image.png",
            mime="image/png"
        )
