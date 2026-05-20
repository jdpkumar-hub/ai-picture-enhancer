import streamlit as st
import os
from pathlib import Path
from PIL import Image

from auth import logout
from services.load_css import load_css
from services.sidebar import render_sidebar
from services.auth_guard import require_login

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

from services.picsart_api import (
    picsart_face_enhance
)

from services.history_service import (
    save_history
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
# AUTH CHECK
# =====================================================

if "user" not in st.session_state:

    st.warning("Please login first")

    st.switch_page("app.py")

    st.stop()

if st.session_state.user is None:

    st.warning("Please login first")

    st.switch_page("app.py")

    st.stop()

# =============LOGIN REQUIED ====================
require_login()
# =====================================================

# =========== SIDEBAR =================================
render_sidebar()
# =====================================================


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

# =====================================================
# UPLOAD
# =====================================================

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

            # ==========================================
            # QUICK ENHANCE
            # ==========================================

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

            # ==========================================
            # PRODUCT CLEAN
            # ==========================================

            elif mode == "product":

                result = clean_product_image(img)

            # ==========================================
            # DEBLUR
            # ==========================================

            elif mode in (
                "deblur_free",
                "deblur_ai"
            ):

                result = deblur_sharpen(
                    img,
                    use_ai=use_ai,
                    api_token=token
                )

            # ==========================================
            # UPSCALE
            # ==========================================

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

            # ==========================================
            # FREE FACE
            # ==========================================

            elif mode == "face_free":

                result = enhance_face(
                    img,
                    use_ai=False
                )

            # ==========================================
            # PICSART FACE AI
            # ==========================================

            elif mode == "face_ai":

                os.makedirs(
                    "temp",
                    exist_ok=True
                )

                input_path = "temp/input.png"

                output_path = "temp/output.png"

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

        # ==========================================
        # SHOW RESULT
        # ==========================================

        with col2:

            st.image(
                result,
                caption="Enhanced",
                use_container_width=True
            )

        # ==========================================
        # SAVE HISTORY
        # ==========================================

        try:

            os.makedirs("temp", exist_ok=True)

            original_path = "temp/history_original.png"

            enhanced_path = "temp/history_enhanced.png"

            img.convert("RGB").save(original_path)

            result.convert("RGB").save(enhanced_path)

            save_history(
                st.session_state.user.email,
                mode_label,
                original_path,
                enhanced_path
            )

        except Exception as e:

            st.error(
                f"History Save Failed: {str(e)}"
            )

        # ==========================================
        # DOWNLOAD
        # ==========================================

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