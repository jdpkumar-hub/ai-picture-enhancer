from PIL import ImageFilter


def restore_old_photo(image):

    image = image.filter(
        ImageFilter.SHARPEN
    )

    image = image.filter(
        ImageFilter.DETAIL
    )

    return image