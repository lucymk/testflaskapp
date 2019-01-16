import base64


def convert_to_base64(path):
    """Convert an image file to base64 format"""
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string
