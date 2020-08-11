"""
A pipeline that detects the center of 6 purple hexagons

"""

import ovl

SERIAL_PORT = "/dev/ttyUSB1"

dark_purple = ovl.Color([130, 100, 70], [154, 255, 255])

image_filters = [ovl.gaussian_blur(), ovl.rotate_image(angle=90), ovl.adaptive_brightness(brightness=45)]

target_filters = [ovl.percent_area_filter(minimal_percent=0.03),
                  ovl.polygon_filter(side_amount=6, min_len_ratio=0.4, min_area_ratio=0.6),
                  ovl.area_sort()]

direction_monitors = [ovl.StopIfCloseMonitor(0.6, 5000)]

director = ovl.Director(direction_monitors=direction_monitors,
                        target_amount=6,
                        failed_detection=9999,
                        directing_function=ovl.center_directions)

connection = ovl.SerialConnection(port=SERIAL_PORT)


pipeline = ovl.Vision(image_filters=image_filters,
                      target_filters=target_filters,
                      director=director,
                      camera=1,
                      ovl_camera=True,
                      threshold=dark_purple)

while True:
    image = pipeline.get_image()
    contours, filtered_image = pipeline.detect(image, verbose=True)
    directions = pipeline.get_directions(contours, filtered_image)
    if isinstance(directions, tuple):
        directions = directions[0]
    pipeline.send(directions)

