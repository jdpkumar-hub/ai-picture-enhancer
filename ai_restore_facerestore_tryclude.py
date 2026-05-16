import requests
import streamlit as st
import tempfile
import time
import os
import base64

# =====================================================
# REPLICATE CONFIG
# Real-ESRGan model version (official, not placeholder)
# =====================================================

REAL_ESRGAN_VERSION = "42fed1c4974dafd699e2b6c4371cc3b346cc4e74"

# =====================================================
# AI FACE RESTORE  (manual REST API — no SDK)
# FIX: removed hardcoded fake model hash and fake image URL.
#      Now uploads image as base64 data URI directly in
#      the prediction payload — no separate hosting needed.
# =====================================================

def restore_face(uploaded_file):

    api_token = st.secrets["REPLICATE_API_TOKEN"]

    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }

    # Reset pointer then read bytes
    uploaded_file.seek(0)
    image_bytes = uploaded_file.read()

    # Encode image as base64 data URI (Replicate accepts this)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_uri = f"data:image/png;base64,{b64}"

    # Create prediction
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json={
            "version": REAL_ESRGAN_VERSION,
            "input": {
                "image":        data_uri,
                "scale":        4,
                "face_enhance": True
            }
        }
    )

    if response.status_code != 201:
        raise Exception(
            f"Replicate API error {response.status_code}: {response.text}"
        )

    prediction     = response.json()
    prediction_url = prediction["urls"]["get"]

    # Poll until done
    max_wait = 120   # seconds
    elapsed  = 0

    while elapsed < max_wait:

        result = requests.get(prediction_url, headers=headers).json()

        status = result.get("status")

        if status == "succeeded":
            return result["output"]

        elif status == "failed":
            raise Exception(
                f"AI restoration failed: {result.get('error', 'unknown error')}"
            )

        time.sleep(2)
        elapsed += 2

    raise TimeoutError("AI restoration timed out after 120 seconds")
