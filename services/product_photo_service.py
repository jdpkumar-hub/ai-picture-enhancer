from PIL import ImageFilter


def product_photo_ai(image):

    image = image.filter(
        ImageFilter.DETAIL
    )

    image = image.filter(
        ImageFilter.SHARPEN
    )

    return image