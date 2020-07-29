import ovl

BLUE = ovl.Color([100, 75, 50], [135, 255, 255])

camera = ovl.Camera(0)

image_filters = [ovl.gaussian_blur((5, 5))]

hexagon_contour_filters = [ovl.area_filter(min_area=300),
                           ovl.polygon_filter(side_amount=6,
                                              min_area_filter=0.7,
                                              min_len_ratio=0.5,
                                              min_angle_ratio=0.6),
                           ovl.area_sort()]

ball_contour_filters = [ovl.area_filter(min_area=200),
                        ovl.circle_filter(min_area_ratio=0.65),
                        ovl.area_sort()]

hexagon_director = ovl.Director(ovl.xy_center_directions,
                                failed_detection=9999,
                                target_amount=2)

ball_director = ovl.Director(ovl.target_amount_directions,
                             failed_detection=9999,
                             target_amount=2)

red_ball_amount_counter = ovl.Vision(threshold=ovl.RED_HSV,
                                     contour_filters=ball_contour_filters,
                                     camera=camera,
                                     image_filters=image_filters)

two_blue_hexagons = ovl.Vision(threshold=BLUE,
                               contour_filters=hexagon_contour_filters,
                               camera=camera,
                               image_filters=image_filters)

vision_controller = ovl.AmbientVision(main_vision=two_blue_hexagons,
                                      ambient_vision=red_ball_amount_counter,
                                      main_amount=5)

while True:
    image = vision_controller.get_image()
    contours, filtered_image = vision_controller.detect(image)
    directions = vision_controller.get_directions(contours, filtered_image)
    print("Directions:", directions)

    vision_controller.send(directions)
