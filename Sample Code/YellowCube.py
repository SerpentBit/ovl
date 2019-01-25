# Simple Object Detection of a yellow cube (The 2018 FRC game piece - the PowerUp! cube)
from ovl.Vision import Vision
from ovl.Color import BuiltInColors
from ovl.Filters import area_filter
from ovl.Sorters import descending_area_sort
from ovl.Directions import x_center_directions
from cv2 import GaussianBlur


v = Vision(filters=[area_filter, descending_area_sort],
           # Filter Contours that aren't large enough and then sort them from large to small - our target is the Largest
           color=BuiltInColors.yellow_hsv.dark(50),
           # Find objects that are yellow and increase the V range by 50 (.dark() function) for darker illumination conditions
           camera_port=0,
           # Connect to the USB camera in 0 (Change to 1 on a laptop with a built-in camera)
           network_port='vision_result',
           connection_dst='10.XX.XX.2', 
           # IP of the destination to which the result is sent, change XX.XX for to your team number
           width=320,  # Wanted width of frames taken with the camera (320 is default)
           height=240,  # Wanted height of frames taken with the camera (240 is default),
           directions_function=x_center_directions,
           target_amount=1  # Amount of objects (contours) to be found (default is 1)
           )

while True:
    img = v.get_image()  # take an image from the camera
    
    v.get_contours(img)  # get contours that are of the given color
    
    v.apply_all_filters()  # apply all given filters (and sorter) functions
    
    directions = v.get_directions() # get the directions needed for the robot 
    
    # see ovl-Python/English/ovl/Vision/__init__ for more information
    
    if directions is False: # if no object was found send failed value (default is 9999) 
      directions = v.failed_value 
    
    if contourArea(v.contours[0]) > v.width * v.height * 0.5:
      directions = 5000  # Stop condition: if the object is right infront (at least half the image) of us stop by sending 5000 
    
    v.send_to_destination(directions)
           
