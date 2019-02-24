# Ovl-Python (Owl)

Python Module for Computer Vision Object Tracking and Detection mainly for the FIRST® Robotics Competition Program

The Library was written by Ori Ben-Moshe.

Copyright (©) 2018 - 2019, Ori Ben-Moshe, all rights reserved.

The following python module dependencies are needed:

  - OpenCV Version 2.x, 3.x & 4.x ([for more information on how to install](https://github.com/1937Elysium/Ovl-Python/blob/master/Installing%20Opencv.md))
  
  - matplotlib
  
  - numpy
  
  - scipy
  
  - sklearn (0.20 for python 2.7 & 3.4)
 

OVL is officially supported for the following python versions: 2.7 and 3.4+

## Installation:

Using `pip`:
</br>
`python -m pip install ovl`

For a light weight version that does not include the calibration sub-module:
</br>
`python -m pip install ovl-light`


In order to update use the `--update` flag.
e.g:
`python -m pip install --upgrade ovl`

Download the files directly:

[Current Version](https://github.com/1937Elysium/Ovl-Python/tree/master/Archives/Current%20Release) from the Archives.

Documentation for the Library is available in [English](https://github.com/1937Elysium/Ovl-Python/tree/master/English) and [Hebrew](https://github.com/1937Elysium/Ovl-Python/blob/master/Hebrew/Introduction.md).
Great sample code (in english) is [here](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/Constructer%20(__init__).md).


### Known Issues:
If you find a bug please post it in the issues section!
- `Vision.json_serialize` and `Vision.json_deserialize` are not updated
- `Vision.Vision.__str__` and `Vision.Vision.__repr__`
- `Color.Color.apply_hsv_vector`, `Color.Color.apply_hsv_high`, `Color.Color.apply_hsv_low`, `Color.Color.light()`, `Color.Color.dark()` raise an error even when they shouldn't
- `Filters.rotated_rectangle_filter` is missing a default parameter
- `Vision.Vision.camera_setup()` has a recursion error with a `Camera.Camera` object
