import streamlit as st
import os

from PIL import Image

from auth import logout

from services.picsart_api import (
    picsart_face_enhance
)

from enhance import (
    deblur_sharpen,
    upscale,
    enhance_face,
    clean_product_image,
    enhance_photo,
    image_to_bytes,
)

# =====================================================
# AUTH
# =====================================================

if "user" not in st.session_state:

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
# PAGE
# =====================================================

st.title("✨ AI Enhance Workspace")

# =====================================================
# REPLICATE TOKEN
# =====================================================

try:

    REPLICATE_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

    has_ai = True

except:

    has_ai = False

# =====================================================
# MODES
# =====================================================

MODES = {

    "HD Enhance (quick)": "hd",

    "Portrait Enhance (quick)": "portrait",

    "Ultra Sharp (quick)": "ultrasharp",

    "Product Clean (remove bg)": "product",

    "Deblur / Sharpen — Free": "deblur_free",

    "Upscale 4× — Free": "upscale_free",

    "Face Enhance — Free": "face_free",

    "Deblur / Sharpen — AI": "deblur_ai",

    "Upscale 4× — AI": "upscale_ai",

    "Face Enhance — AI (PicsArt)": "face_ai",
}

mode_label = st.selectbox(
    "Enhancement Mode",
    list(MODES.keys())
)

mode = MODES[mode_label]

uploaded = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

# =====================================================
# MAIN
# =====================================================

if uploaded:

    img = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            img,
            caption="Original",
            use_container_width=True
        )

    if st.button("✨ Enhance Image"):

        with st.spinner("Processing..."):

            use_ai = mode.endswith("_ai")

            token = REPLICATE_TOKEN if has_ai else ""

            # -----------------------------------------
            # QUICK MODES
            # -----------------------------------------

            if mode == "hd":

                result = enhance_photo(
                    img,
                    "HD Enhance"
                )

            elif mode == "portrait":

                result = enhance_photo(
                    img,
                    "Portrait Enhance"
                )

            elif mode == "ultrasharp":

                result = enhance_photo(
                    img,
                    "Ultra Sharp"
                )

            # -----------------------------------------
            # PRODUCT
            # -----------------------------------------

            elif mode == "product":

                result = clean_product_image(img)

            # -----------------------------------------
            # DEBLUR
            # -----------------------------------------

            elif mode in (
                "deblur_free",
                "deblur_ai"
            ):

                result = deblur_sharpen(
                    img,
                    use_ai=use_ai,
                    api_token=token
                )

            # -----------------------------------------
            # UPSCALE
            # -----------------------------------------

            elif mode in (
                "upscale_free",
                "upscale_ai"
            ):

                result = upscale(
                    img,
                    scale=4,
                    use_ai=use_ai,
                    face_enhance=False,
                    api_token=token
                )

            # -----------------------------------------
            # FREE FACE ENHANCE
            # -----------------------------------------

            elif mode == "face_free":

                result = enhance_face(
                    img,
                    use_ai=False
                )

            # -----------------------------------------
            # PICSART FACE AI
            # -----------------------------------------

            elif mode == "face_ai":

                os.makedirs(
                    "temp",
                    exist_ok=True
                )

                input_path = "temp/input.jpg"

                output_path = "temp/output.jpg"

                img.save(input_path)

                enhanced = picsart_face_enhance(
                    input_path,
                    output_path
                )

                if enhanced:

                    result = Image.open(output_path)

                else:

                    st.error(
                        "PicsArt enhancement failed"
                    )

                    st.stop()

        # =================================================
        # SHOW RESULT
        # =================================================

        with col2:

            st.image(
                result,
                caption="Enhanced",
                use_container_width=True
            )

        # =================================================
        # DOWNLOAD
        # =================================================

        img_bytes = image_to_bytes(
            result,
            fmt="PNG"
        )

        st.download_button(
            label="📥 Download Enhanced Image",
            data=img_bytes,
            file_name="enhanced_image.png",
            mime="image/png",
        )