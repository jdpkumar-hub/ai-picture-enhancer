from PIL import ImageEnhance


def prompt_edit(image, prompt):

    if "bright" in prompt.lower():

        enhancer = ImageEnhance.Brightness(image)

        image = enhancer.enhance(1.3)

    if "sharp" in prompt.lower():

        enhancer = ImageEnhance.Sharpness(image)

        image = enhancer.enhance(2.0)

    return image