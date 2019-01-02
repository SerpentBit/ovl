# Geometry.get_lengths_and_angles


| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| contour | No default | ndarray (numpy array) | N/A | A numpy array that defines a group of points. |
| approximation_coefficient | 0.02 | int, float | x > 0 | The approximation coeffiecient given to the Approximation function, see ApproxPolyDP from the opencv documentation| 


`get_lengths_and_angles` is a function that receives a contour and returns three arrays, an array with coordinates of the contour's angles, the angles' sizes and the sides' lengths.
