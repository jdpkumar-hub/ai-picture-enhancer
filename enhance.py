from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import numpy as np
import cv2
import io

# =====================================================
# CLEAN PRODUCT IMAGE
# FIX: rembg returns RGBA — split alpha before OpenCV,
#      reattach after processing so transparency is kept.
# =====================================================

def clean_product_image(img):

    # Convert to RGB first
    img = img.convert("RGB")

    # Remove background → returns RGBA
    output = remove(img)

    # Split into RGB + Alpha
    np_img = np.array(output)          # shape: H x W x 4
    rgb    = np_img[:, :, :3]          # BGR-compatible (OpenCV wants 3ch)
    alpha  = np_img[:, :, 3]           # transparency mask

    # Noise reduction on RGB only
    denoise = cv2.fastNlMeansDenoisingColored(
        rgb,
        None,
        10,
        10,
        7,
        21
    )

    # Sharpen
    kernel = np.array([
        [0, -1,  0],
        [-1,  5, -1],
        [0, -1,  0]
    ])
    sharpen = cv2.filter2D(denoise, -1, kernel)

    # Reattach alpha channel
    result_np = np.dstack([sharpen, alpha])   # H x W x 4
    result = Image.fromarray(result_np, "RGBA")

    # Enhance contrast (PIL works on RGBA fine)
    contrast = ImageEnhance.Contrast(result)
    result = contrast.enhance(1.15)

    # FIX: Only ONE sharpening pass — removed duplicate ImageEnhance.Sharpness
    # (cv2.filter2D already sharpened above; double-sharpen causes halos)

    return result


# =====================================================
# PHOTO ENHANCE
# FIX: removed double-sharpening in HD Enhance mode.
#      Each mode now uses a single, intentional pipeline.
# =====================================================

def enhance_photo(img, mode="HD Enhance"):

    img = img.convert("RGB")
    np_img = np.array(img)

    # Denoise
    denoise = cv2.fastNlMeansDenoisingColored(
        np_img,
        None,
        8,
        8,
        7,
        21
    )

    result = Image.fromarray(denoise)

    if mode == "HD Enhance":
        # Contrast boost + moderate sharpness (single pass)
        result = ImageEnhance.Contrast(result).enhance(1.2)
        result = ImageEnhance.Sharpness(result).enhance(1.6)

    elif mode == "Portrait Enhance":
        # Smooth skin tones, gentle contrast lift
        result = result.filter(ImageFilter.SMOOTH_MORE)
        result = ImageEnhance.Contrast(result).enhance(1.1)

    elif mode == "Ultra Sharp":
        # Strong sharpening kernel THEN PIL sharpness — intentional two-step
        kernel = np.array([
            [0, -1,  0],
            [-1,  5, -1],
            [0, -1,  0]
        ])
        sharp_np = cv2.filter2D(np.array(result), -1, kernel)
        result = Image.fromarray(sharp_np)
        result = ImageEnhance.Sharpness(result).enhance(1.8)

    return result


# =====================================================
# IMAGE TO BYTES BUFFER
# Helper used by pages to avoid writing to disk
# (disk writes are unreliable on Streamlit Cloud).
# =====================================================

def image_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    # RGBA images must stay PNG; JPEG doesn't support alpha
    if img.mode == "RGBA" and fmt.upper() == "JPEG":
        fmt = "PNG"
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.read()
