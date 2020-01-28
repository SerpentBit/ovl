import ovl

# filter contours that are larger than 200 pixels
# and are approximately a circle and then sort by size

contour_filters = [ovl.area_filter(min_area=200), ovl.circle_filter(min_area_ratio=0.7), ovl.dec_area_sort()] 

threshold = ovl.YELLOW_HSV # Define the wanted color to detect 

yellow_circle = Vision(threshold=threshold,
                       contour_filters=contour_filters,
                       camera=0, # open the first connected camera
                       image_filters=image_filters)

while True:
    image = yellow_circle.get_filtered_image()
    contours, filtered_image = yellow_circle.detect(image)
    directions = yellow_circle.get_directions(contours, filtered_image)
    
    print(directions) # prints out the (x, y) coordinates of the largest target

