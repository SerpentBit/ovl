# Directions.xy_center_directions

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour_list | No Default | list or ndarray (numpy array) | N/A | A list of contours / a single contour |
| target_amount | No default | int | N/A | The minimum amount of contours in the list |
| img_size | No default | tuple(int, int) | N/A | The image the contours were taken from |

Returns the dierction the robot needs to drive based on the average of both x and y values of the centers
 of all contours in `contour_list`. </br>
If there is an error, the returned value is ![Vision.failed_value](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/Constructer%20(__init__).md)
which is defaulted to '9999'.

Exmaple:
```
# This is a hypothetical situation
# We will presume there are 3 contours in the contour_list
# Their centres are: (160, 10), (140, 50), (300, 100)
>>> img_size = (320, 160)
>>> target_amount = 3
>>> xy_center_directions(contour_list, target_amount, img_size)
'12000636' # Returned Width_Value = 1200, Height_Value = 636
```
