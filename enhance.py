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
def enhance_photo(image):

    image = image.convert("RGB")

    # Gentle enhancement
    image = image.filter(ImageFilter.SMOOTH)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.08)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.1)

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.03)

    return image