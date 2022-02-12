import ovl

target_filters = [ovl.percent_area_filter(min_area=0.005),
                  ovl.circle_filter(min_area_ratio=0.7),
                  ovl.area_sort()]

threshold = ovl.Color([20, 100, 100], [55, 255, 255])

yellow_circle = ovl.Vision(threshold=threshold,
                           target_filters=target_filters,
                           camera=0,  # open the first connected camera
                           image_filters=[ovl.gaussian_blur()])

while True:
    image = yellow_circle.get_image()
    targets, filtered_image = yellow_circle.detect(image)
    directions = yellow_circle.get_directions(targets, filtered_image)

    print(directions)  # prints out the (x, y) coordinates of the largest target
