# Ovl-Python (pronounced: Owl)

Python Module for Computer Vision Object Tracking and Detection mainly for the FIRST® Robotics Competition Program

### Dependencies:

The following python module dependencies are needed:

 - OpenCV 
  
 - numpy
  
The following python modules are optional for certain features:


 - NetworkTables (pyNetworkTables) for: NetworkTableConnection
 
 - sklearn (scikit-learn): HSVCalibration

OVL is officially supported for python 3.5+!

Installation:

Using `pip`:
<br>
  `python -m pip install ovl`


## Usage:

The library uses simple yet highly customizable syntax to create
 a vision pipeline using the `Vision` object


A pipeline that detects 1 yellow circle:
```
import ovl

# filter contours that are larger than 200 pixels
# and are approximately a circle
# and then sort by size

contour_filters = [ovl.area_filter(min_area=200),
           ovl.circle_filter(min_area_ratio=0.7),
           ovl.dec_area_sort()] 

threshold = ovl.YELLOW_HSV # Define the wanted color to detect 

# open the first connected camera 

camera = ovl.Camera(0) 

yellow_circle = Vision(threshold=threshold,
                       contour_filters=contour_filters,
                       camera=camera,
                       image_filters=image_filters)

while True:
    image = yellow_circle.get__filtered_image()
    contours, image = yellow_circle.detect(image)

    directions = yellow_circle.get_directions(contours, image)
    
    print(directions) # prints out the (x, y) coordinates of the largest target
```
<br>
<br>
Find 2 retro reflective tapes and find their center.

```

```

