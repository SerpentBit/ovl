# 0.2.1

## Main Changes:
 - New Sub-Module - `ImageFilters`
 - New support for curve contours (open/unclosed), Filters Sorters Vision object and Geometry
 - Get contours using `Cv2.Canny` (Edge detection)
 - Get contours for a binary mask
 - Refactors and parameter changes
 
## New sub-Module:
- 2 built-in image filters - change_brightness and adaptive_brightness
- BGR to hsv "image filter" (mainly for begginer use)
- Can be passed to `Vision.image_filters` 
- Cv2 functions such as GaussianBlur MedianBlur BilateralBlur and BoxFilters can be used as well

## Additions:
- `Geometry.line_angle` - returns the angle between a contour (that is a line) and the x axis
- `Geometry.angle_between_points` - returns the angle in degrees between 2 points and the x axis
- `Geometry.open_arc_length` - arc length of an unclosed contour
- `Geometry.get_approximation_open` - get_approximation for unclosed contours
- `Sorters.inc_length_sort` - sorts unclosed contours from smallest to largest
- `Sorters.dec_length_sort` - sorts unclosed contours from largest to smallest
- `Filters.length_filter` - a filter for unclosed contours by their length
- `Vision.get_image` gets an image from the camera
- 

## Refactors:
 - `descending_area_sort` -> `dec_area_sort`
 - `ascending_area_sort` -> `inc_area_sort`

## Changes:
 - `Vision.get_directions` no longer requires any parameters - uses default values from self
 - `Vision.get_contours` can now return hierarchy using the return_hierarchy parameter

## BugFixes:
 - All `center_directions` functions now correctly
 - Made `Vision.image_filters` and `Vision.image_params` consistent

## Added Documentation:
 - All `center_directions`
 - `alert directions`
 - `Vision.apply_image_filters`
 
 
