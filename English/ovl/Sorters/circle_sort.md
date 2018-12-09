# Sorters.circle_sort

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array)| N/A | The list of the contours that the function filters out |
| area_limit | 0.9 | int, float | N/A | For area_limit look at ![Geometry.circle_rating](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Geometry/circle_rating.md) |
| radius_limit | 0.8 | int, float | N/A | For radius_limit look at ![Geometry.circle_rating](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Geometry/circle_rating.md) |

Returns the `contour_list` sorted by how similar they are to a circle (from most to least).

Code example:
```
v = Vision(..., Sorters=circle_sort)
```

