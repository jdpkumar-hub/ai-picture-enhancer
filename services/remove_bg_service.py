#from rembg import remove
from PIL import Image
import io


def remove_background(image):

    buffer = io.BytesIO()

    image.save(buffer, format="PNG")

    output = remove(buffer.getvalue())

    result = Image.open(io.BytesIO(output))

    return result