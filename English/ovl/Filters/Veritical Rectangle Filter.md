# Filters.Vertical_rectangle_filter

| Parameter Name | Default value | Types | Value range | Description | 
| :---: |  :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array)| N/A | The list of the contours that the function filters out |
| min_area_ratio | 0.85 | float | 0<x<1 | The minimum ratio between the contour and the area of the **straight** bounding rectangle |

## *Minimum Area Ratio*
The minimum area ratio between the contour and the straight bounding rectangle. 

The Vertical rectangle filter also makes sure the outline approximation of the shape has 4 sides and that the height
of the Bounding Rectangle is longer than its width.
