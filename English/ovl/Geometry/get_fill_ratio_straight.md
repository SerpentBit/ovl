# Geometry.get_fill_ratio_straight


| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour | No default | ndarray (numpy array) | N/A | A numpy array that defines a group of points. |
| reverse_div | False | boolean | N/A | Whether the rectangle's area should be divided by the contour or the opposite. |


`get_fill_ratio_straight` is a function that takes a contour, finds the smallest, straight rectangle that encloses it, 
finds that rectangle's and the contour's area and returns their ratio and the rectangle's width and height. If `reverse_div` is false, the function returns the contour's area divided by the rectangle's area, else, it returns the rectangle's area divided by the contour's area.

</br>
</br>

Code example:
```
img_path = 'C:\Users\USER\Desktop\image.png'
image = cv2.imread(img_path)
get_fill_ratio_straight(image)
```

</br>

The given image will look like this:
</br>
</br>


![](https://github.com/1937Elysium/Ovl-Python/blob/master/Pictures/Sample%20Pictures/fill_ratio.png)
