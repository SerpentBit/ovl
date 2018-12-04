# Filters.triangle_filter

| Parameter Name | Default value | Types | Value range | Description | 
| :---: |  :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array)| N/A | The list of the contours that the function filters out |
| min_area_ratio | 0.8 | float | 0<x<1 | The minimum ratio between the contour and the area of the  bounding triangle |

## *Minimum Area Ratio*
The minimum area ratio between the contour and the bounding triangle. 

The `triangle_filter` also makes sure the outline approximation of the shape has 3 sides.
