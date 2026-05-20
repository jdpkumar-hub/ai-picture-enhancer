from PIL import (
    Image,
    ImageEnhance,
    ImageFilter
)


def remove_background(img):

    img = img.convert("RGBA")

    result = ImageEnhance.Contrast(
        img
    ).enhance(1.2)

    result = result.filter(
        ImageFilter.SHARPEN
    )

    return result