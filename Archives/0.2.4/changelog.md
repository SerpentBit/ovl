# 0.2.4

## Main Changes:
  - New Sub-Module - `Camera` - with a high preformance `camera` object
  - Support for morphological functions in `Vision`
  - Image center proximity sort and filter
  - Image rotation image filters
  - Multiple types of morphological shape kernels built-in

## Additions:
- `Camera.Camera` - a class with a high preformance camera object
- `ImageFilters.cross_kernel` - creates a plus-shaped array to the given odd integer size (x, y)
- `ImageFilters.rectangle_kernel` - creates a rectangle (all 1) array of the given size (x, y)
- `ImageFilters.ellipse_kernel` creates an ellipse shaped kernel of the given size (x, y) 
- `ImageFilters.horizontal_line_kernel` creates an array with a line across its center, the array is of a given size (x, y)
- `ImageFilters.vertical_line_kernel` creates an array with a line accross its center (vertically), the array is of the given size (x,y)
- `ImageFilters.sharpen_image` applies a sharpening matrix on a given image.
- `ImageFilters.rotate_by_angle` rotated the image by a given angle
- `ImageFilters.rotate90_left` rotates the image 90 degrees counter clock-wise
- `ImageFilters.rotate90_right` rotates the image 90 degrees clock-wise
- `ImageFilters.rotate180` rotates the image 180 degrees - flipping it upside down
- `Sorters.image_center_sort` sorts an a given contour list by proximity (distance) to the image center  
- `Geometry.atan` returns the arc tangent in degrees
- `Geometry.y_intersection` returns the point of intersection of a given line function with a given x value (returns the value of the function at a given point)
- `Geometry.x_interseciton` returns the x value for which the given function intersects with a given y
- `Geometry.distance_from_frame` returns the distance of a point (x,y) (or contour) from the frame of the image based on the line defined by it (or the contour center) and the center of the image
- `Geometry.focal_length` calculates the focal length of the image given an iage width and horoizontal field of view (fov)
- `Geometry.vertical_angle` calculates the veritcal angle of a given point in the vertical plane of the image based on the image height and vertical field of view (fov)
- `Geometry.horizon_angle` calculates the veritcal angle of a given point in the horizontal plane of the image based on the image width and horizontal field of view (fov)
- `Filters.image_center_filter` filters out contours that aren't close enough to the center of the image propotionally to the line that starts in the image center and goes through the conotur center till the image frame
- `Filters.abs_distance_filter` filters out contours that aren`t in the given pixel distance range from the center (min and max)
- `Vision.Vision.apply_morphs` applies all given morphological functions on the given mask
- `Vision.Vision.get_applied_image` returns the image and auto applies all of the `Vision` object image filters
- `Vision.Vision.get_color_mask` returns the mask for a given image and `Color` (or `MultiColor`) object.

## Changes
- `Vision.Vision.get_directions` can now automatically send (using `Vision.Vision.send_to_destination()`
- `Vision.Vision.apply_all_filters` can now be suppressed by passing True to the parameter `suppress`
- `Vision.Vision.camera_setup` uses VideoCapture as its default camera object for now but can be told to create a `Camera.Camera` object instead by passing True to `use_camera`
- `Vision.Vision.get_contours_mask` now auto applies morphological functions (if given) can be told now to by pasing False to `apply_morphs`

## Bug Fixes
 - fixed a bug that could crash `Vision.Vision.apply_filter` when passed valid parameter
 
