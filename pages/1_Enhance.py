import streamlit as st
from PIL import Image

from auth import logout
from enhance import (
    clean_product_image,
    enhance_photo
)

# =====================================================
# AUTH CHECK
# =====================================================

if "user" not in st.session_state:

    st.switch_page("app.py")

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

# =====================================================
# MAIN PAGE
# =====================================================

st.title("🚀 AI Enhance Workspace")

st.write(
    "Upload image and apply AI enhancement"
)

# =====================================================
# MODE
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

    # =============================================
    # ORIGINAL
    # =============================================

    with col1:

        st.image(
            img,
            caption="Original Image",
            use_container_width=True
        )

    # =============================================
    # BUTTON
    # =============================================

    if st.button("✨ Enhance Image"):

        with st.spinner("AI enhancing image..."):

            if photo_mode == "Product Clean":

                result = clean_product_image(img)

            else:

                result = enhance_photo(
                    img,
                    photo_mode
                )

        # =========================================
        # RESULT
        # =========================================

        with col2:

            st.image(
                result,
                caption="Enhanced Image",
                use_container_width=True
            )

        # =========================================
        # DOWNLOAD
        # =========================================

        result.save("enhanced.png")

        with open("enhanced.png", "rb") as f:

            st.download_button(

                "📥 Download Enhanced Image",

                f,

                file_name="enhanced_image.png",

                mime="image/png"
            )