'''
This pipeline detects red squares 
It also includes a director object and a connection
Which simplifies passing data to the target

******************************************************
NOTE: this example code uses NetworkTablesConnection
which is used specifically for the FIRST Robotics Competition
in order to connect to the RoboRIO controller
You can easily replace it with a different connections
'''

import ovl

# for other ways to connect run the following python code: help(NetworkTablesConnection)
TEAM_NUMBER = 1937 

threshold = RED_HSV

contour_filters = [ovl.area_filter(min_area_ratio=150),
                   ovl.straight_rectangle_filter(min_area_ratio=0.7),
                   ovl.dec_area_sort()]

director = ovl.Director(directing_function=ovl.x_center_directions, failed_detection=9999,
                        target_amount=1,)

camera = ovl.Camera(0, image_width=640, image_height=480)

roborio = ovl.NetworkTablesConnection(roborio=TEAM_NUMBER, table_key="SmartDashboard")

image_filters = [ovl.gaussian_blur((5, 5))]

red_square = ovl.Vision(threshold=threshold,
                        contour_filters=contour_filters,
                        director=director,
                        camera=camera,
                        image_filters=image_filters
                        )

while True:
    image = red_square.get_filtered_image()
    contours, filtered_image = red_square.detect(image)
    directions = red_square.get_directions(contours, image)
    red_square.send(directions)
