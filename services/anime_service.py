from PIL import ImageFilter


def anime_style(image):

    image = image.filter(
        ImageFilter.EDGE_ENHANCE_MORE
    )

    return image