import requests
import streamlit as st
import tempfile
import time

API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json"
}

# =========================================
# AI FACE RESTORE
# =========================================
def restore_face(uploaded_file):

    # Save uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:

        temp.write(uploaded_file.read())

        temp_path = temp.name

    # Upload image to temporary hosting
    files = {
        "file": open(temp_path, "rb")
    }

    # Create prediction
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json={
            "version": "42fed1c497afce8b1f6e6b7b9d7fdd5f7d0b7e4f4f8df6f8d6f8d5f8d6f8d5",
            "input": {
                "image": "https://replicate.delivery/pbxt/YOUR_IMAGE_URL",
                "face_enhance": True
            }
        }
    )

    prediction = response.json()

    prediction_url = prediction["urls"]["get"]

    # Wait for completion
    while True:

        result = requests.get(
            prediction_url,
            headers=headers
        ).json()

        if result["status"] == "succeeded":
            return result["output"]

        elif result["status"] == "failed":
            raise Exception("AI restoration failed")

        time.sleep(2)