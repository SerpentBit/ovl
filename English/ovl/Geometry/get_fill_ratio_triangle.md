# Geometry.get_fill.ratio.triangle


| Parameter Name | Default value | Types | Value range | Description | 
| :---: |  :---: | :---: | :---: | :---: |
| contour | No default | ndarray (numpy array) | N/A | A numpy array that defines a group of points. |
| reverse_div | False | boolean | N/A | Whether the triangle's area should be divided by the contour or the opposite. |

`get_fill_ratio_triangle` is a function that takes a contour, finds the smallest triangle that encloses it,
finds that triangle's and the contour's area and returns their ratio. If `reverse_div` is false, 
the function returns the contour's area divided by the triangle's area, else, it returns the triangle's area divided by the contour's area.
</br>
</br>

<b>The triangle may be of any type.</b>

</br>
</br>

Code example:
```
Ori's stuffs
```
Result:
