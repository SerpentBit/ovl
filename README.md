# OVL - Object Vision Library

![OVL Logo](https://user-images.githubusercontent.com/45563197/76566629-d4301300-64b5-11ea-9868-40ecde73dcaa.png)

Python Module for Computer Vision Object Tracking and Detection mainly for the FIRST® Robotics Competition Program

Ovl support complex yet modular computer vision pipelines that are easy to create and modify.

Easy to create and setup for beginners and flexible for pros

*You can follow up on changes in for the current version in
the [changelog folder](https://github.com/1937Elysium/Ovl-Python/tree/master/changelogs)*

## Documentation

There are multiple code examples [here](https://github.com/1937Elysium/Ovl-Python/tree/master/code%20examples)

Documentation is available [here](https://ovl.readthedocs.io/)

### Dependencies:

The following python module dependencies are needed:

- OpenCV

- numpy

The following python modules are optional for certain features:

- NetworkTables (pyNetworkTables) for `NetworkTableConnection` (installed automatically)

OVL is officially supported for python 3.7+

Installation:

Using `pip`:
<br>
`python -m pip install ovl[cv]`

For the full installation of all features use:
`python -m pip install ovl[full]`

For the frc related features use the frc option:
`python -m pip install ovl[frc]`

> Note that ovl doesn't come with the precompiled version of
> opencv for python automatically. If you wish to compile opencv for yourself -
> simply refrain from using the cv flag during installation.
> `python -m pip install ovl`

## Usage:

The library uses simple yet highly customizable syntax to create a vision pipeline using the `Vision` object

A pipeline that detects a yellow circle:

```
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


```

There are more code examples and usages [here](https://github.com/1937Elysium/Ovl-Python/tree/master/code%20examples)
