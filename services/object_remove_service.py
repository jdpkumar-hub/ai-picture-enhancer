from PIL import ImageFilter


def remove_objects(image):

    image = image.filter(
        ImageFilter.SMOOTH_MORE
    )

    return image