"""
This pipeline detects red squares calculates directions according to its
position compared to the center of the image and
returns the directions to move in (1 to -1 where 1 is a hard right and -1 is hard left)
It also includes connection object
Which simplifies passing data to the target that acts on the detection
******************************************************
NOTE: this example code uses NetworkTablesConnection
which is used specifically for, the FIRST Robotics Competition
in order to connect to the RoboRIO controller
You can easily replace it with a different connections
"""
import ovl


# for other ways to connect to your RoboRIO run the following python code: help(NetworkTablesConnection)
TEAM_NUMBER = "1937"

threshold = ovl.HSV.red

contour_filters = [ovl.area_filter(min_area=150),
                   ovl.straight_rectangle_filter(min_area_ratio=0.7),
                   ovl.area_sort()]

director = ovl.Director(directing_function=ovl.xy_normalized_directions,
                        failed_detection="Could not detect!",
                        target_selector=1)


camera = ovl.Camera(0, image_width=640, image_height=480)

roborio = ovl.NetworkTablesConnection(roborio=TEAM_NUMBER, table_name="SmartDashboard", table_key="vision_directions")

image_filters = [ovl.gaussian_blur((5, 5))]

red_square = ovl.Vision(threshold=threshold,
                        target_filters=contour_filters,
                        director=director,
                        camera=camera,
                        image_filters=image_filters)

while True:
    image = red_square.get_image()
    contours, filtered_image = red_square.detect(image)
    directions = red_square.get_directions(contours, image)
    print(directions)

    # red_square.send(directions)  # Comment when not running with a connected RoboRIO
