# Geometry.circle_rating


| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour | No default | ndarray (numpy array) | N/A | A numpy array that defines a group of points. |
| area_factor | 0.9 | int, float | 0 < x ≤ 1 | The tolerance of the contour's area compared to the smallest enclosing circle's area. |
| radius_factor | 0.8 | int, float | 0 < x ≤ 1 | The tolerance of the contour's radius compared to the smallest enclosing circle's radius. |

`circle.rating` is a function that receives a contour, finds the smallest circle and straight rectangle that enclose it, 
uses them in order to find the contour's fill ratio and radius ratio, multiplies each one with its tolerance and multiplies the results.
The function returns a rating of how close the contour is to being a full circle. The perfect score is one.

Code example?
