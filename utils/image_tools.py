"""
utils/image_tools.py
--------------------
Image utility helpers shared across pages.
FIX: file was a placeholder containing only its own filename.
     Now contains real utility functions.
"""

from PIL import Image
import io
import numpy as np


# =====================================================
# LOAD IMAGE SAFELY
# Returns None instead of crashing on bad files.
# =====================================================

def load_image(uploaded_file) -> Image.Image | None:
    try:
        uploaded_file.seek(0)
        return Image.open(uploaded_file).copy()
    except Exception:
        return None


# =====================================================
# IMAGE → BYTES (for st.download_button / Supabase upload)
# Handles RGBA→PNG auto-conversion (JPEG has no alpha).
# =====================================================

def image_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    if img.mode == "RGBA" and fmt.upper() in ("JPEG", "JPG"):
        fmt = "PNG"
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.read()


# =====================================================
# RESIZE TO MAX DIMENSION
# Keeps aspect ratio; avoids OOM on huge uploads.
# =====================================================

def resize_max(img: Image.Image, max_dim: int = 2048) -> Image.Image:
    w, h = img.size
    if max(w, h) <= max_dim:
        return img
    scale = max_dim / max(w, h)
    return img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)


# =====================================================
# SIDE-BY-SIDE NUMPY ARRAY (for debug / comparison)
# =====================================================

def side_by_side(img_a: Image.Image, img_b: Image.Image) -> np.ndarray:
    a = np.array(img_a.convert("RGB"))
    b = np.array(img_b.convert("RGB"))
    # Pad to same height
    h = max(a.shape[0], b.shape[0])
    def pad(x, h):
        if x.shape[0] < h:
            pad = np.zeros((h - x.shape[0], x.shape[1], 3), dtype=x.dtype)
            return np.vstack([x, pad])
        return x
    return np.hstack([pad(a, h), pad(b, h)])
