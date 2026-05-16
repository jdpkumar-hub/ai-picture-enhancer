from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import numpy as np
import cv2

# =====================================================
# CLEAN PRODUCT IMAGE
# =====================================================

def clean_product_image(img):

    # Convert
    img = img.convert("RGB")

    # Remove background
    output = remove(img)

    # Convert to OpenCV
    np_img = np.array(output)

    # Noise reduction
    denoise = cv2.fastNlMeansDenoisingColored(
        np_img,
        None,
        10,
        10,
        7,
        21
    )

    # Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5,-1],
        [0, -1, 0]
    ])

    sharpen = cv2.filter2D(
        denoise,
        -1,
        kernel
    )

    # Convert back
    result = Image.fromarray(sharpen)

    # Enhance contrast
    contrast = ImageEnhance.Contrast(result)
    result = contrast.enhance(1.15)

    # Enhance sharpness
    sharpness = ImageEnhance.Sharpness(result)
    result = sharpness.enhance(1.4)

    return result

# =====================================================
# PHOTO ENHANCE
# =====================================================

def enhance_photo(img, mode="HD Enhance"):

    img = img.convert("RGB")

    # OpenCV convert
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

    # Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5,-1],
        [0, -1, 0]
    ])

    sharpen = cv2.filter2D(
        denoise,
        -1,
        kernel
    )

    result = Image.fromarray(sharpen)

    if mode == "HD Enhance":

        contrast = ImageEnhance.Contrast(result)
        result = contrast.enhance(1.2)

        sharpness = ImageEnhance.Sharpness(result)
        result = sharpness.enhance(1.6)

    elif mode == "Portrait Enhance":

        smooth = result.filter(
            ImageFilter.SMOOTH_MORE
        )

        contrast = ImageEnhance.Contrast(smooth)
        result = contrast.enhance(1.1)

    elif mode == "Ultra Sharp":

        sharpness = ImageEnhance.Sharpness(result)
        result = sharpness.enhance(2.2)

    return result