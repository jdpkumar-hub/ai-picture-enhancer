import io
import time
import base64
import numpy as np
import cv2
import requests
from services.sidebar import render_sidebar

from PIL import (
    Image,
    ImageEnhance,
    ImageFilter
)

from rembg import remove

# =====================================================
# REPLICATE MODELS
# =====================================================

REPLICATE_MODELS = {

    "deblur":
        "deepghs/nafnet-deblur:a4d94e97a8d2d01c75ab27b80484f87b5bb0bf3c",

    "upscale":
        "nightmareai/real-esrgan:42fed1c4974dafd699e2b6c4371cc3b346cc4e74",

    "face":
        "tencentarc/gfpgan:0fbacfa7aacb3dbb07e8d81de359ba0d97b50a6e",
}

REPLICATE_POLL_TIMEOUT = 120
REPLICATE_POLL_INTERVAL = 2

# =====================================================
# HELPERS
# =====================================================

def _pil_to_bytes(img: Image.Image, fmt="PNG"):

    buf = io.BytesIO()

    img.save(buf, format=fmt)

    return buf.getvalue()


def _to_data_uri(image_bytes):

    b64 = base64.b64encode(image_bytes).decode("utf-8")

    return f"data:image/png;base64,{b64}"


def _upload_to_replicate(api_token, image_bytes):

    headers = {
        "Authorization": f"Token {api_token}"
    }

    response = requests.post(
        "https://api.replicate.com/v1/files",
        headers=headers,
        files={
            "content": (
                "image.png",
                image_bytes,
                "image/png"
            )
        }
    )

    return response.json()["urls"]["get"]


def _replicate_run(api_token, model_version, payload):

    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json={
            "version": model_version,
            "input": payload
        }
    )

    if response.status_code != 201:

        raise RuntimeError(response.text)

    poll_url = response.json()["urls"]["get"]

    elapsed = 0

    while elapsed < REPLICATE_POLL_TIMEOUT:

        result = requests.get(
            poll_url,
            headers=headers
        ).json()

        status = result.get("status")

        if status == "succeeded":

            output = result.get("output")

            return output[0] if isinstance(output, list) else output

        if status == "failed":

            raise RuntimeError(result.get("error"))

        time.sleep(REPLICATE_POLL_INTERVAL)

        elapsed += REPLICATE_POLL_INTERVAL

    raise TimeoutError("Replicate timed out")


def _download_image(url):

    response = requests.get(url)

    return Image.open(io.BytesIO(response.content))

# =====================================================
# DEBLUR
# =====================================================

def deblur_sharpen(img, use_ai=False, api_token=""):

    if use_ai:

        data_uri = _to_data_uri(
            _pil_to_bytes(img.convert("RGB"))
        )

        url = _replicate_run(
            api_token,
            REPLICATE_MODELS["deblur"],
            {
                "image": data_uri
            }
        )

        return _download_image(url)

    np_img = np.array(img.convert("RGB"))

    blur = cv2.GaussianBlur(np_img, (0, 0), sigmaX=3)

    sharp = cv2.addWeighted(
        np_img,
        1.5,
        blur,
        -0.5,
        0
    )

    return Image.fromarray(sharp)

# =====================================================
# UPSCALE
# =====================================================

def upscale(
    img,
    scale=4,
    use_ai=False,
    face_enhance=False,
    api_token=""
):

    if use_ai:

        data_uri = _to_data_uri(
            _pil_to_bytes(img.convert("RGB"))
        )

        url = _replicate_run(
            api_token,
            REPLICATE_MODELS["upscale"],
            {
                "image": data_uri,
                "scale": scale,
                "face_enhance": face_enhance
            }
        )

        return _download_image(url)

    w, h = img.size

    np_img = np.array(img.convert("RGB"))

    resized = cv2.resize(
        np_img,
        (w * scale, h * scale),
        interpolation=cv2.INTER_LANCZOS4
    )

    return Image.fromarray(resized)

# =====================================================
# FACE ENHANCE
# =====================================================

def enhance_face(img, use_ai=False, api_token=""):

    if use_ai:

        img_bytes = _pil_to_bytes(
            img.convert("RGB")
        )

        hosted_url = _upload_to_replicate(
            api_token,
            img_bytes
        )

        output_url = _replicate_run(
            api_token,
            REPLICATE_MODELS["face"],
            {
                "img": hosted_url,
                "version": "v1.4",
                "scale": 2
            }
        )

        return _download_image(output_url)

    np_img = np.array(img.convert("RGB"))

    bilateral = cv2.bilateralFilter(
        np_img,
        15,
        75,
        75
    )

    return Image.fromarray(bilateral)

# =====================================================
# PRODUCT CLEAN
# =====================================================

def clean_product_image(img):

    img = img.convert("RGB")

    output = remove(img)

    np_img = np.array(output)

    rgb = np_img[:, :, :3]

    alpha = np_img[:, :, 3]

    denoise = cv2.fastNlMeansDenoisingColored(
        rgb,
        None,
        10,
        10,
        7,
        21
    )

    result_np = np.dstack([denoise, alpha])

    return Image.fromarray(result_np, "RGBA")

# =====================================================
# QUICK ENHANCE
# =====================================================

def enhance_photo(img, mode="HD Enhance"):

    img = img.convert("RGB")

    np_img = np.array(img)

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

        result = ImageEnhance.Contrast(result).enhance(1.2)

        result = ImageEnhance.Sharpness(result).enhance(1.6)

    elif mode == "Portrait Enhance":

        result = result.filter(ImageFilter.SMOOTH_MORE)

    elif mode == "Ultra Sharp":

        result = ImageEnhance.Sharpness(result).enhance(1.8)

    return result

# =====================================================
# IMAGE TO BYTES
# =====================================================

def image_to_bytes(img, fmt="PNG"):

    return _pil_to_bytes(img, fmt)