"""
enhance.py
----------
Image quality pipeline with three improvements:
  1. Deblur / Sharpen   — free (OpenCV) OR AI (NAFNet via Replicate)
  2. Upscale            — free (Lanczos) OR AI (Real-ESRGAN via Replicate)
  3. Face / Portrait    — free (bilateral filter) OR AI (GFPGAN via Replicate)

Each function has a `use_ai` flag. Pass use_ai=True when you want
the Replicate API path; False for the instant local path.

FIX (RuntimeError on enhance_face):
  Root cause 1 — GFPGAN rejects base64 data URIs; it requires a real
                 uploaded file URL. We now upload via Replicate's file
                 upload endpoint first, then pass the returned URL.
  Root cause 2 — _replicate_run swallowed the real Replicate error
                 message. It now surfaces the full detail so future
                 errors are immediately readable in the Streamlit log.
  Root cause 3 — GFPGAN input key is "img" but NAFNet/Real-ESRGAN use
                 "image". These are now routed separately so no payload
                 mismatch occurs.
"""

import io
import time
import base64
import tempfile
import os
import numpy as np
import cv2
import requests
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove

# ──────────────────────────────────────────────────────────────
# REPLICATE CONFIG
# ──────────────────────────────────────────────────────────────

# FIX: updated GFPGAN to the latest stable version hash
REPLICATE_MODELS = {
    "deblur":  "deepghs/nafnet-deblur:a4d94e97a8d2d01c75ab27b80484f87b5bb0bf3c",
    "upscale": "nightmareai/real-esrgan:42fed1c4974dafd699e2b6c4371cc3b346cc4e74",
    "face":    "tencentarc/gfpgan:0fbacfa7aacb3dbb07e8d81de359ba0d97b50a6e",
}

REPLICATE_POLL_TIMEOUT  = 120
REPLICATE_POLL_INTERVAL = 2

# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────

def _pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    if img.mode == "RGBA" and fmt.upper() in ("JPEG", "JPG"):
        fmt = "PNG"
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

def _to_data_uri(image_bytes: bytes, mime: str = "image/png") -> str:
    """Base64 data URI — accepted by Real-ESRGAN and NAFNet, NOT by GFPGAN."""
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def _upload_to_replicate(api_token: str, image_bytes: bytes) -> str:
    """
    FIX: upload image bytes to Replicate's file store and return the
    hosted URL. GFPGAN (and some other models) reject data URIs and
    require a real https:// URL pointing to the file.
    """
    headers = {"Authorization": f"Token {api_token}"}
    resp = requests.post(
        "https://api.replicate.com/v1/files",
        headers=headers,
        files={"content": ("image.png", image_bytes, "image/png")},
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(
            f"Replicate file upload failed {resp.status_code}: {resp.text}"
        )
    return resp.json()["urls"]["get"]   # permanent hosted URL

def _replicate_run(api_token: str, model_version: str, payload: dict) -> str:
    """
    Submit a prediction and poll until done.
    FIX: now surfaces the full Replicate error body so failures are
    readable in the Streamlit log instead of being swallowed.
    """
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type":  "application/json",
    }
    resp = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json={"version": model_version, "input": payload},
    )
    if resp.status_code != 201:
        # FIX: include full response body in the error
        raise RuntimeError(
            f"Replicate prediction creation failed "
            f"(HTTP {resp.status_code}):\n{resp.text}"
        )

    poll_url = resp.json()["urls"]["get"]
    elapsed  = 0
    while elapsed < REPLICATE_POLL_TIMEOUT:
        result = requests.get(poll_url, headers=headers).json()
        status = result.get("status")
        if status == "succeeded":
            output = result.get("output")
            return output[0] if isinstance(output, list) else output
        if status == "failed":
            raise RuntimeError(
                f"Replicate prediction failed:\n{result.get('error', 'unknown error')}"
            )
        time.sleep(REPLICATE_POLL_INTERVAL)
        elapsed += REPLICATE_POLL_INTERVAL
    raise TimeoutError("Replicate prediction timed out after 120s")

def _download_image(url: str) -> Image.Image:
    resp = requests.get(url)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content))

# ──────────────────────────────────────────────────────────────
# 1. DEBLUR / SHARPEN
# ──────────────────────────────────────────────────────────────

def deblur_sharpen(img: Image.Image, use_ai: bool = False, api_token: str = "") -> Image.Image:
    """
    Remove blur and sharpen the image.

    Free path  — unsharp mask via OpenCV. Instant. Good for mild blur.
                 Can produce halos on heavy blur.
    AI path    — NAFNet on Replicate. Handles motion blur cleanly.
                 ~10-20s per image. Requires REPLICATE_API_TOKEN.
    """
    if use_ai:
        if not api_token:
            raise ValueError("api_token required for AI deblur")
        data_uri = _to_data_uri(_pil_to_bytes(img.convert("RGB")))
        url = _replicate_run(api_token, REPLICATE_MODELS["deblur"], {"image": data_uri})
        return _download_image(url)

    # Free: Gaussian unsharp mask
    np_img = np.array(img.convert("RGB"))
    blur   = cv2.GaussianBlur(np_img, (0, 0), sigmaX=3)
    sharp  = cv2.addWeighted(np_img, 1.5, blur, -0.5, 0)
    kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
    sharp  = cv2.filter2D(sharp, -1, kernel)
    sharp  = np.clip(sharp, 0, 255).astype(np.uint8)
    return Image.fromarray(sharp)

# ──────────────────────────────────────────────────────────────
# 2. UPSCALE / INCREASE RESOLUTION
# ──────────────────────────────────────────────────────────────

def upscale(img: Image.Image, scale: int = 4, use_ai: bool = False,
            face_enhance: bool = False, api_token: str = "") -> Image.Image:
    """
    Increase image resolution.

    Free path  — Lanczos interpolation. Smooth, no new detail.
                 Fine at 2x; soft at 4x.
    AI path    — Real-ESRGAN on Replicate. Generates real detail at 4x.
                 Set face_enhance=True to also run GFPGAN on faces.
                 ~10-20s per image.
    """
    if use_ai:
        if not api_token:
            raise ValueError("api_token required for AI upscale")
        data_uri = _to_data_uri(_pil_to_bytes(img.convert("RGB")))
        url = _replicate_run(
            api_token, REPLICATE_MODELS["upscale"],
            {"image": data_uri, "scale": scale, "face_enhance": face_enhance},
        )
        return _download_image(url)

    # Free: Lanczos
    w, h    = img.size
    np_img  = np.array(img.convert("RGB"))
    resized = cv2.resize(np_img, (w * scale, h * scale), interpolation=cv2.INTER_LANCZOS4)
    return Image.fromarray(resized)

# ──────────────────────────────────────────────────────────────
# 3. FACE / PORTRAIT ENHANCEMENT
# ──────────────────────────────────────────────────────────────

def enhance_face(img: Image.Image, use_ai: bool = False, api_token: str = "") -> Image.Image:
    """
    Enhance faces and portraits.

    Free path  — Bilateral filter. Smooths skin, preserves hard edges.
                 No face detection; applies to whole image.
    AI path    — GFPGAN on Replicate. Detects and restores facial features.
                 Excellent on old/damaged photos. ~15-25s per image.
    """
    if use_ai:
        if not api_token:
            raise ValueError("api_token required for AI face enhance")
        # FIX: GFPGAN rejects base64 data URIs — upload the file first
        # and pass the returned https:// URL as the "img" input instead.
        img_bytes    = _pil_to_bytes(img.convert("RGB"))
        hosted_url   = _upload_to_replicate(api_token, img_bytes)
        output_url   = _replicate_run(
            api_token, REPLICATE_MODELS["face"],
            {"img": hosted_url, "version": "v1.4", "scale": 2},
        )
        return _download_image(output_url)

    # Free: bilateral filter
    np_img    = np.array(img.convert("RGB"))
    bilateral = cv2.bilateralFilter(np_img, d=15, sigmaColor=75, sigmaSpace=75)
    result    = Image.fromarray(bilateral)
    result    = ImageEnhance.Contrast(result).enhance(1.1)
    return result

# ──────────────────────────────────────────────────────────────
# 4. CLEAN PRODUCT IMAGE  (rembg + denoise)
# ──────────────────────────────────────────────────────────────

def clean_product_image(img: Image.Image) -> Image.Image:
    """Remove background, denoise and sharpen. Returns RGBA."""
    img    = img.convert("RGB")
    output = remove(img)
    np_img = np.array(output)
    rgb    = np_img[:, :, :3]
    alpha  = np_img[:, :, 3]
    denoise   = cv2.fastNlMeansDenoisingColored(rgb, None, 10, 10, 7, 21)
    kernel    = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoise, -1, kernel)
    result_np = np.dstack([sharpened, alpha])
    result    = Image.fromarray(result_np, "RGBA")
    return ImageEnhance.Contrast(result).enhance(1.15)

# ──────────────────────────────────────────────────────────────
# 5. GENERAL PHOTO ENHANCE  (HD / Portrait / Ultra Sharp)
# ──────────────────────────────────────────────────────────────

def enhance_photo(img: Image.Image, mode: str = "HD Enhance") -> Image.Image:
    """General quick-enhance, no AI required."""
    img    = img.convert("RGB")
    np_img = np.array(img)
    denoise = cv2.fastNlMeansDenoisingColored(np_img, None, 8, 8, 7, 21)
    result  = Image.fromarray(denoise)
    if mode == "HD Enhance":
        result = ImageEnhance.Contrast(result).enhance(1.2)
        result = ImageEnhance.Sharpness(result).enhance(1.6)
    elif mode == "Portrait Enhance":
        result = result.filter(ImageFilter.SMOOTH_MORE)
        result = ImageEnhance.Contrast(result).enhance(1.1)
    elif mode == "Ultra Sharp":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        result = Image.fromarray(cv2.filter2D(np.array(result), -1, kernel))
        result = ImageEnhance.Sharpness(result).enhance(1.8)
    return result

# ──────────────────────────────────────────────────────────────
# 6. IMAGE → BYTES  (for st.download_button)
# ──────────────────────────────────────────────────────────────

def image_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    return _pil_to_bytes(img, fmt)
