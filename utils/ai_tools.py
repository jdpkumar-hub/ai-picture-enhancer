"""
utils/ai_tools.py
-----------------
AI pipeline helpers shared across pages.
FIX: file was a placeholder containing only its own filename.
     Now contains real utility functions.
"""

import streamlit as st
import replicate
import requests
import base64
import time


# =====================================================
# CHECK REPLICATE TOKEN
# Call at startup to surface config errors early.
# =====================================================

def check_replicate_token() -> bool:
    try:
        token = st.secrets.get("REPLICATE_API_TOKEN", "")
        return bool(token and len(token) > 10)
    except Exception:
        return False


# =====================================================
# IMAGE BYTES → BASE64 DATA URI
# Replicate accepts base64 data URIs directly so we
# don't need a separate image hosting step.
# =====================================================

def to_data_uri(image_bytes: bytes, mime: str = "image/png") -> str:
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"


# =====================================================
# POLL REPLICATE PREDICTION
# Shared polling loop used by both restore modules.
# =====================================================

def poll_prediction(
    prediction_url: str,
    headers: dict,
    timeout: int = 120,
    interval: int = 2
) -> dict:
    elapsed = 0
    while elapsed < timeout:
        result = requests.get(prediction_url, headers=headers).json()
        status = result.get("status")
        if status == "succeeded":
            return result
        if status == "failed":
            raise RuntimeError(
                f"Prediction failed: {result.get('error', 'unknown')}"
            )
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"Prediction timed out after {timeout}s")


# =====================================================
# RUN REAL-ESRGAN (SDK shortcut)
# Simple wrapper so pages don't import replicate directly.
# =====================================================

REAL_ESRGAN_MODEL = "nightmareai/real-esrgan:42fed1c4974dafd699e2b6c4371cc3b346cc4e74"

def run_real_esrgan(image_bytes: bytes, scale: int = 4, face_enhance: bool = True):
    data_uri = to_data_uri(image_bytes)
    output   = replicate.run(
        REAL_ESRGAN_MODEL,
        input={
            "image":        data_uri,
            "scale":        scale,
            "face_enhance": face_enhance
        }
    )
    return output
