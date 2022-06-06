import numpy as np

from .open_image import open_image


# TODO: Add http fetching support
# TODO: Docstring
def source_to_image(source):
    """
    Converts a source to an image.
    :param source: The source to convert.
    :return: The image.
    """
    if isinstance(source, str):
        return open_image(source)
    elif isinstance(source, np.ndarray):
        return source
    else:
        raise ValueError(f"Invalid source type {source}.")


# TODO: Create Image class that can be used to manipulate images.
# TODO: Docstring
class Image:
    def __init__(self, image):
        self.image = image
