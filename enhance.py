from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import io

# =========================================
# PRODUCT CLEAN (Background Removal)
# =========================================
def clean_product_image(image):

    image = image.convert("RGB")

    # Remove background
    input_bytes = io.BytesIO()
    image.save(input_bytes, format="PNG")

    output_bytes = remove(input_bytes.getvalue())

    image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # White background
    white_bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
    image = Image.alpha_composite(white_bg, image).convert("RGB")

    # Enhancement
    image = image.filter(ImageFilter.SHARPEN)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.15)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.2)

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.05)

    return image


# =========================================
# NORMAL PHOTO ENHANCEMENT
# =========================================
# =========================================
# NORMAL PHOTO ENHANCEMENT
# =========================================
# =========================================
# ADVANCED PHOTO ENHANCEMENT
# =========================================
def enhance_photo(image, mode="Natural"):

    image = image.convert("RGB")

    # ---------------------------------
    # NATURAL
    # ---------------------------------
    if mode == "Natural":

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.05)

        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.12)

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.02)

    # ---------------------------------
    # SHARP
    # ---------------------------------
    elif mode == "Sharp":

        image = image.filter(ImageFilter.SHARPEN)

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)

        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)

    # ---------------------------------
    # BRIGHT
    # ---------------------------------
    elif mode == "Bright":

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.15)

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.05)

    # ---------------------------------
    # SOCIAL MEDIA
    # ---------------------------------
    elif mode == "Social Media":

        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)

        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.15)

    return image