import streamlit as st
from PIL import Image
import io

from auth import logout
from enhance import (
    deblur_sharpen,
    upscale,
    enhance_face,
    clean_product_image,
    enhance_photo,
    image_to_bytes,
)

# ── Auth guard ────────────────────────────────────────────────
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.success(f"Welcome {st.session_state.user.email}")
if st.sidebar.button("Logout"):
    logout()
    st.session_state.user = None
    st.switch_page("app.py")
    st.stop()

# ── Page ──────────────────────────────────────────────────────
st.title("AI Enhance Workspace")

# Pull Replicate token once (from st.secrets, never from user input)
try:
    REPLICATE_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
    has_ai = True
except Exception:
    has_ai = False

# ── Mode selector ─────────────────────────────────────────────
MODES = {
    "HD Enhance (quick)":            "hd",
    "Portrait Enhance (quick)":      "portrait",
    "Ultra Sharp (quick)":           "ultrasharp",
    "Product Clean (remove bg)":     "product",
    "Deblur / Sharpen — Free":       "deblur_free",
    "Upscale 4× — Free (Lanczos)":   "upscale_free",
    "Face Enhance — Free":           "face_free",
    "Deblur / Sharpen — AI (NAFNet)":"deblur_ai",
    "Upscale 4× — AI (Real-ESRGAN)": "upscale_ai",
    "Face Enhance — AI (GFPGAN)":    "face_ai",
}

mode_label = st.selectbox("Enhancement Mode", list(MODES.keys()))
mode       = MODES[mode_label]

if mode.endswith("_ai") and not has_ai:
    st.warning("Set REPLICATE_API_TOKEN in your Streamlit secrets to use AI modes.")

# ── Upload ────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Original", use_container_width=True)

    if st.button("Enhance Image", disabled=(mode.endswith("_ai") and not has_ai)):
        with st.spinner("Processing..."):
            use_ai = mode.endswith("_ai")
            token  = REPLICATE_TOKEN if use_ai else ""

            if mode in ("hd", "portrait", "ultrasharp"):
                label_map = {"hd": "HD Enhance", "portrait": "Portrait Enhance", "ultrasharp": "Ultra Sharp"}
                result = enhance_photo(img, label_map[mode])

            elif mode == "product":
                result = clean_product_image(img)

            elif mode in ("deblur_free", "deblur_ai"):
                result = deblur_sharpen(img, use_ai=use_ai, api_token=token)

            elif mode in ("upscale_free", "upscale_ai"):
                result = upscale(img, scale=4, use_ai=use_ai, face_enhance=False, api_token=token)

            elif mode in ("face_free", "face_ai"):
                result = enhance_face(img, use_ai=use_ai, api_token=token)

        with col2:
            st.image(result, caption="Enhanced", use_container_width=True)

        # Download (BytesIO, no disk write)
        img_bytes = image_to_bytes(result, fmt="PNG")
        st.download_button(
            label="Download Enhanced Image",
            data=img_bytes,
            file_name="enhanced_image.png",
            mime="image/png",
        )
