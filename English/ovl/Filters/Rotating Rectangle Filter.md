# Filters.rotating_rectangle_filter

| Parameter Name | Default value | Types | Value range | Description | 
| :---: |  :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array) | N/A | The list of the contours that the function filters out |
| min_area_ratio | 0.8 | float | 0<x<1 | The minimum ratio between the contour and the area of the **rotating** bounding rectangle |

## *Minimum Area Ratio*
The minimum area ratio between the contour and the rotating bounding rectangle. 

The `rotating_rectangle_filter` also makes sure the outline approximation of the shape has 4 sides.

Rotating bounding rectangle compared to a straight bounding rectangle:

![](https://github.com/1937Elysium/Ovl-Python/blob/master/Pictures/Rotated%20Bounding%20Rectangle.png)
