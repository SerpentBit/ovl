import time


def numeral_name_convention(image_number):
    return "image" + str(image_number)


def time_name_convention(image_number):
    return f"image{image_number}:{time.strftime('%a-%d-%b-%Y-%H:%M:%S', time.gmtime())}"
