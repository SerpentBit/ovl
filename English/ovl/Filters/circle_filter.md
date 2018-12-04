#Filters.circle_filter

| Parameter Name | Default value | Types | Value range | Description | 
| :---: |  :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array)| N/A | The list of the contours that the function filters out |
| min_area_ratio | 0.85 | float | 0 < x < 1 | The minimum ratio between the contour and the area of the smallest circle that encloses the contour |
| min_len_ratio | 0.9 | float | 0 < x < 1 | The minimum ratio between the Diameter of the enclosing circle and the bounding rect of the contour |


