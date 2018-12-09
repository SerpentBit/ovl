# Sorters.descending_area_sort

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array)| N/A | The list of the contours that the function filters out |
| **kwargs | No default | N/A | N/A | Does not use any additional paramaters |

Returns the contour list sorted by area from smallest to largest.

Code example:
```
v = Vision(..., Sorters=ascending_area_sort)
```

