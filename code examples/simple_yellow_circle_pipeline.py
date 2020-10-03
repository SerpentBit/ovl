import ovl

# filter contours that are larger than 200 pixels
# and are approximately a circle and then sort by size

target_filters = [ovl.area_filter(min_area=200),
                   ovl.circle_filter(min_area_ratio=0.7),
                   ovl.area_sort()]

threshold = ovl.YELLOW_HSV  # Define the wanted color to detect

yellow_circle = ovl.Vision(threshold=threshold,
                           target_filters=target_filters,
                           camera=0,  # open the first connected camera
                           image_filters=[ovl.gaussian_blur()])

while True:
    image = yellow_circle.get_image()
    contours, filtered_image = yellow_circle.detect(image)
    directions = yellow_circle.get_directions(contours, filtered_image)

    print(directions)  # prints out the (x, y) coordinates of the largest target