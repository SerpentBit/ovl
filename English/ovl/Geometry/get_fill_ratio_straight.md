# Geometry.get_fill_ratio_straight


| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour | No default | ndarray (numpy array) | N/A | A numpy array that defines a group of points. |
| reverse_div | False | boolean | N/A | Whether the rectangle's area should be divided by the contour or the opposite. |


`get_fill_ratio_straight` is a function that takes a contour, finds the smallest, straight rectangle that bound it fully, 
finds that rectangle's area, the contour's area and their ratio. If `reverse_div` is false, the function returns the contour's area divided by the rectangle's area, else, it returns the rectangles area divided by the contour's area.

</br>
</br>

Code example:
```
Ori's stuffs
```
Result:
