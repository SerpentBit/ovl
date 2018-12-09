# Directions

Direction contains various functions which return a value that present the direction the robot needs to drive to (The returned values are between 0 to 2000: 
0 for sharp left, 1000 for straight, and 2000 for sharp right). The driving direction is based on the average x and y values of the given contours.

The full list of functions:

- validate - Checks if the given contour_list is the okay length.
- xy_center_directions - Returns the dierction the robot needs to drive based on both x and y.
- y_center_directions - Returns the dierction the robot needs to drive based on y.
- x_center_directions - Returns the dierction the robot needs to drive based on x.
