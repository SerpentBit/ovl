# Ovl-Python 
 ![ovl logo](https://user-images.githubusercontent.com/45563197/76566629-d4301300-64b5-11ea-9868-40ecde73dcaa.png)

Python Module for Computer Vision Object Tracking and Detection mainly for the FIRST® Robotics Competition Program
*You can follow up on changes in for the current version in the [changelog folder](https://github.com/1937Elysium/Ovl-Python/tree/master/changelogs)*
*There have been significant changes from the previous version - [changelog](https://github.com/1937Elysium/Ovl-Python/tree/master/changelogs/2020.1.5)*

### Dependencies:

The following python module dependencies are needed:

 - OpenCV 
  
 - numpy
  
The following python modules are optional for certain features:


 - NetworkTables (pyNetworkTables) for `NetworkTableConnection` (installed automatically)
 
 - sklearn (scikit-learn) for `HSVCalibration` creation (not needed for use in `Vision`)

 - PySerial (pyserial) for `SerialConnection`

OVL is officially supported for python 3.5+ only!

Installation:

Using `pip`:
<br>
  `python -m pip install ovl`

## Usage:

The library uses simple yet highly customizable syntax to create
 a vision pipeline using the `Vision` object


A pipeline that detects a yellow circle:
```
import ovl

# filter contours that are larger than 200 pixels
# and are approximately a circle and then sort by size

contour_filters = [ovl.area_filter(min_area=200),
                   ovl.circle_filter(min_area_ratio=0.7),
                   ovl.area_sort()]

image_filters = [ovl.gaussain_blur()]

threshold = ovl.YELLOW_HSV  # Define the wanted color to detect 

yellow_circle = ovl.Vision(threshold=threshold,
                           contour_filters=contour_filters,
                           camera=0,  # open the first connected camera
                           image_filters=image_filters)

while True:
    image = yellow_circle.get_filtered_image()
    contours, filtered_image = yellow_circle.detect(image)
    directions = yellow_circle.get_directions(contours, filtered_image)

    print(directions)  # prints out the (x, y) coordinates of the largest target


```
There are more code examples and usages [here](https://github.com/1937Elysium/Ovl-Python/tree/master/code%20examples)
<br>
<br>

## Documentation
The Hebrew and English documentation have been removed for being outdated all functions
and classes now have in code documentation.
This includes code examples, recommended usage reference to further
documentation and more.

There are multiple code examples [here](https://github.com/1937Elysium/Ovl-Python/tree/master/code%20examples)

Simply use the built-in `help` on a class/function:
```
help(ovl.Vision)

help(ovl.contour_filter)

help(ovl.area_filter)
```

<br>
<br>

