# Ovl-Python 
Python Module for Computer Vision Object Tracking and Detection mainly for the FIRST® Robotics Competition Program

*There have been significant changes from the previous version - [changelog](#major-changes-from-previous-patch)*

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


A pipeline that detects a yellow circle:
```
import ovl

# filter contours that are larger than 200 pixels
# and are approximately a circle and then sort by size

contour_filters = [ovl.area_filter(min_area=200),
                   ovl.circle_filter(min_area_ratio=0.7),
                   ovl.dec_area_sort()] 

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


```

<br>
<br>

## Documentation
The Hebrew and English documentation have been removed for being outdated all functions
and classes now have in code documentation.
This includes code examples, recommended usage reference to further
documentation and more.

There are multiple code examples [here](https://github.com/1937Elysium/Ovl-Python/tree/master/code%20examples)

simply use `help` on a class/function:
```
help(ovl.Vision)

help(ovl.contour_filter)

help(ovl.area_filter)
```

<br>
<br>

## Major changes from previous patch:

### Dependency changes:
Now only CV2 and numpy are mandatory dependencies all other are optional:
 - sklearn is only needed for calibration
 - networktables is only needed for NetworkTableConnection
 - PySerial is only needed for SerialConnection

### Additions:
The new version has brought many new additions

#### Vision
Major `Vision` object overhaul:
 - removed many redundant functions
 - removed obsolete parameters, cleaned overall usage
 - extracted network settings to the new `Connection` object
 - Constructor has been rewritten to be quicker and less complex
 - direction functions and target amount have been extracted to new `Director` object
 - Vision.get_contours -> Vision.find_contours
 - Vision.get_contours_mask -> Vision.find_contours_in_mask
 
Other Vision related additions
- New Vision-like, `AmbientVision`, allows 2 Visions to be run at once by taking "turns"
- New Vision-like `MultiVision`, allows of multiple visions to be run and swapped, supports AmbientVision

#### Connection
- New object Connection, represents a connection
- New connection NetworkTableConnection
- New connection SerialConnection

#### Threshold
New functions for displaying images: `stitch_images`, `show_image`
New image filter `crop_image`, can crop a rectangle out of an image
New object `Threshold`, converts an image to a binary image
New Threshold object CannyEdge
New Direction Utility CameraSettings, defines camera calibrations, offset and other unique changes
New object CameraCalibration, can be used to Calibrate an camera
New object DirectionMonitor, Alters directions according to various situations

#### Images and Utilities
-  photo_array extracted from `Vision`, now a standalone utility function
- Naming conventions for photo array are now functions, custom ones can be created

#### Contour filters
Now Filters can be preloaded with their parameters using the matching XXXX_filter Decorator:
- New Filter Decorator, contour_filter turns a function to a contour filter that iterates on a list of contours
- New Filter Decorator, conditional_contour_filter turns a function that filters one contour to a contour filter
- New Filter Decorator, image_filter turns a function to a image filter that modifies the given image somehow
- New contour filter, `circle_filter`, detects simple circles based on fill ratio

#### Color and MultiColor
- Color and MultiColor now inherit from Threshold
- Color has been rewritten for a cleaner usage

#### Director:
New object `Director`, Handles directing from a final list of targets (contours):
 - Receives a directing function that receives a list of contours and the image
 - Receives a list of DirectionMonitors that alter the directions
 - The directing function returns the initial direction
 - The list of Direction monitors are then applied on the result which is returned

#### Other changes:
- Camera object now automatically starts
- BuiltInColors no longer a class
- serializing all objects have been temporarily removed, they will be re-added in an upcoming patch

### Renames:

- circle_filter -> constraining_circle_filter
- Calibration -> HSVCalibration
- get_fill_ratio_triangle -> triangle_fill_ratio
- get_fill_ratio_straight -> rectangle_fill_ratio
- get_fill_ratio_rotating -> rotating_rectangle_fill_ratio
- get_fill_ratio_circle -> circle_fill_ratio
- get_contour_center -> contour_center
- get_approximation -> contour_approximation
- get_lengths_and_angles -> contour_lengths_and_angles
- n_sided_polygon_angle -> regular_polygon_angle

### Removals:
 - ToolClass
 - ToolError

### Upcoming Changes and Additions
 - Serialization and Deserialization to json of all objects
 - CompoundVision, a vision like object that can has multiple changeable configurations
 - Filter flow control, for complex logical combinations of contour filters and conditional contour filters
 - HSVCalibration overhaul
 - OVLRaspbian, a Raspbian based image for easy strap-booting on RaspberryPI
 - Graphing tools for data analysis of performance and function
 - Live Graphing and Graph Streaming for Graph Capabilities
 - A debugger tool for tuning `Vision` pipelines and detections for ease of use and work efficiency
 
 Have a feature you are interested in? Consider suggesting it or contributing!
