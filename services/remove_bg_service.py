import io
import requests
import streamlit as st

from PIL import Image

PICSART_API_KEY = st.secrets["PICSART_API_KEY"]

def remove_background(img):

    url = "https://api.picsart.io/tools/1.0/removebg"

    buffer = io.BytesIO()

    img.save(buffer, format="PNG")

    buffer.seek(0)

    files = {
        "image": ("image.png", buffer, "image/png")
    }

    headers = {
        "X-Picsart-API-Key": PICSART_API_KEY
    }

    response = requests.post(
        url,
        headers=headers,
        files=files
    )

    if response.status_code != 200:
    
        print(response.text)
        raise Exception(
            f"API Error: {response.text}"
        )

    result = response.json()

    image_url = result["data"]["url"]

    image_response = requests.get(image_url)

    return Image.open(
        io.BytesIO(image_response.content)
    )