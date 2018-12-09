# Geometry

Geometry contains various Geometrical and mathematical functions that perform calculations needed
throughout the Ovl Module 

The full list of functions:

- sin - sine function that uses degrees.

- cos - cosine function that uses degrees.

- tan - tangent funcion that uses degrees.

- calculate_math_expression - returns the result of the expression with the given value.

- get_circle_area - calculates the area of a circle with the given radius.

- distance_between_points - calculates the distance between to given points

- get_fill_ratio_straight - returns the ratio between the area of the given contour and the area of the straight bounding rectangle.

- get_fill_ratio_rotating - returns the ratio between the area of the given contour and the area of the rotating bounding rectangle. 

- get_fill_ratio_triangle - returns the ratio between the area of the given contour and the area of the bounding triangle.

- get_fill_ratio_circle - returns the ratio between the area of the given contour and the area of the smallest enclosing circle.

- get_contour_center - returns the x, y coordinates of the center of a given contour (center of mass, average of distances from edge).

- n_polygon_angle -  returns the inner angle of a regular convex polygon (regular polygon) with n sides.

- n_polygon_area -  returns the area of a regular convex polygon (regular polygon) with  given n sides and length .

- get_approximation - returns a list of x, y coordinates of the approximation of the vertices of a given contour.

- circle_rating - a rating of how close a contour is to being a circle.
