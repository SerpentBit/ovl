# Filters.rotated_square_filter

| Parameter Name | Default value | Types | Value range | Description | 
| :---: |  :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array)| N/A | The list of the contours that the function filters out |
| min_area_ratio | 0.8 | float | 0<x<1 | The minimum ratio between the contour and the area of the **straight** bounding rectangle |
| min_len_ratio | 0.95 | float | 0<x<1 | the minimum ratio between the diagonal of the bounding rect and the diameter of the enclosing circle|
| max_len_ratio | 1.05 | float | x>1 | the maximum ratio between the diagonal of the bounding rect and the diameter of the enclosing circle|

## *Minimum Area Ratio*
The minimum area ratio between the contour and the rotating bounding rectangle. 

## *Minimum Length ratio*
The minimum ratio between the Diameter of the enclosing circle and the diagonal of the bounding rectangle.

## *Maximum Length ratio*
The maximum ratio between the Diameter of the enclosing circle and the diagonal of the bounding rectangle.


The `rotated_square_filter` also makes sure the outline approximation of the shape has 4 sides and that the
bounding rectangle is approximately square. The `rotated_square_filter` searches for the bounding rectangle with the smallest
area regardless of angle.
