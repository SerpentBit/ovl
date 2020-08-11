"""
A Simple program that display a rotated (180 degrees) and blurred (using gaussian blur) of the
live feed of the first (0) connected camera and utilizes the high-FPS realtime oriented Ovl Camera
"""
import ovl

CAMERA_PORT = 0

image_filters = [ovl.gaussian_blur(), ovl.rotate_image()]

pipeline = ovl.Vision(image_filters=image_filters,
                      camera=CAMERA_PORT,
                      ovl_camera=True)

while True:
    image = pipeline.get_image()
    blurred_image = pipeline.apply_image_filters(image)
    ovl.display_image(blurred_image, display_loop=1)
