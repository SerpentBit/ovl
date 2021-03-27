import enum


class SerializeType(enum):
    Generic = 0
    Iterable = 1
    Object = 2
    FilterFunction = 3
    Device = 4


def validate_loaded_vision(loaded_vision):
    """
    Verifies the a loaded vision (Dictionary) contains the the necessary
            Attributes to create a Vision object

    :param loaded_vision: A dictionary containing raw data of the Vision object
    :return:
    """
    return loaded_vision


def loads_vision(serialized_vision):
    """
    Loads a Vision object from a json string.

    :param serialized_vision:
    :return:
    """
    raise NotImplementedError()
    # loaded_vision = loads(serialized_vision)
    # if not validate_loaded_vision(loaded_vision):
    #     raise ValueError("The vision loaded was incomplete")


def load_vision(vision_file):
    """
    Loads a Vision object from a json string.

    :param vision_file: path to the vision file (a json file)
    :return:
    """
    raise NotImplementedError()
    # with open(vision_file, "r") as vision:
    #     return load_serialized_vision(loads(vision.read()))


def dumps_vision(vision):
    vision_dictionary = {}


def dump_vision(file, vision):
    pass
