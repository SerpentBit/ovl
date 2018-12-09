# Geometry.get_fill_ratio_circle


| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour | No default | ndarray (numpy array) | N/A | A numpy array that defines a group of points. |
| reverse_div | False | boolean | N/A | Whether the circle's area should be divided by the contour or the opposite. |


`get_fill_ratio_straight` is a function that takes a contour, finds the smallest circle that encloses it, 
finds that circle's and the contour's area and returns their ratio. If `reverse_div` is false, the function returns the 
contour's area divided by the circle's area, else, it returns the circle's area divided by the contour's area.
