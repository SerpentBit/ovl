# 0.2.5.1
## Main Changes:
 - Erosion and Dilation fucntions in `ImageFilters` - with a default kernel of 5 on 5 for ease of use
 - Multiple bug fixes in the `Color`, `Vision`, `Filters` and `ImageFilters` modules
 - `Vision.Vision.grab_and_process` a function that gets an image finds contours and filters them 
 (get_applied_image/get_image, get_contours and apply_all_filters in one function)
 
## Bug Fixes:
 - Fixed an error with `Color` caused by an outdated operation
 - Fixed an error where `Vision.camera_setup` would be stuck recursively
 - `Vision` will now correctly apply all morphological functions passed
 - `ImageFilters.adaptive_brightness` will no longer go out of bounds when image to brighter than wanted
 - `Vision.Display_Image`'s delay can be set, default is no delay (This also affects `Vision.Vision.display_contours`
 
