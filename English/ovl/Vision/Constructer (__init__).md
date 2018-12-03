# Vision Object Constructer:
Vision is the main object in the OVL module, the object can interact with the various functions in the module.
> A Reminder: This documentation is meant for begginers and advanced programmers alike, so there are bound to be
>             longer and more descriptive explanations.

The Vision is the object that controls the whole process of vision for your robot,
Taking images, finding contours, applying filters, applying sorters, finding directions and sending to the RoboRIO connected the results.
But we are getting ahead of ourselves.

**For the table denoting the parameters and kwargs for the Vision object scroll to the end of the page**

First we must understand the objects used and the basic flow.

## The Flow
The Vision object performs a specific niche in computer vision that is targeted for FRC robots though it can be used for robots in general.
Color detection and then contour filtering based on various wanted properties.
The Flow:
1. Config camera
2. Take the image
3. Apply Calibration
4. Get Contours
5. Apply Filter Functions
6. Get Directions for the Robot
7. Send the Directions to the Robot (RoboRIO)

All of these steps are managed by the vision object.
Note that the last 2 optional and are steps for FIRST Robotics Teams Mainly

Lets go over the flow step by step.

### *1. Configuring the Camera*
**Note: It is possible to 
Open the camera object and configure it (set) its size to the width and height passed to the Vision object
The camera used is selected by passing the port number.

#### Camera Port
`Attribute: camera_port=None -> integer >= 0 or str for video files.`

If there is only 1 camera connected to the device pass: `camera_port=0`
When developing the code on a laptop or PC make sure you are using the port refering to the camera.
If you have one additional camera connected try changing to `camera_port=1` and making sure you return to 0 when finalizing the code.

#### Width and Height 
`Attribure: width=240 -> interger > 0, height=240 (in pixels) -> integer > 0`

Width and Height parameters passed to the Vision object determine the size (in pixels) images taken by the camera will be
default is `width=320` and `height=240`

It is also possible to apply the vision object to a video file by passing the video file path instead of port.
```
Vision(camera_port='path/to/some/video/file.mp4')
```

### *2. Taking the image*

Even though the Flow dictates we take an image from the camera we opened in [step 1](https://github.com/1937Elysium/Ovl-Python/new/master/English#1-configuring-the-camera)
Sometimes, especially during debugging we want to check our Vision process on a specific image and it is possible using 
functions like `single_frame()` or `apply_sample()` (These Functions can be found [here]())

### *3. Apply the Calibration*
`Attribute: calibration_file -> str the calibration json file OR swv and/or vwv -> dictionaries containing weight vectors`
If you are learning for the first time how to use OVL, skip to [step 4](https://github.com/1937Elysium/Ovl-Python/new/master/English#4-getting-the-contours) of the flow

For those of you who stuck around, at this stage we apply our calibration based on the saturation and value value of the mean of our Image
and the Calibration json file that was returned from the calibration program.
The code solves the equation in order to find the matching low bound for the current image based on the calibration images
and the Linear Discriminant analysis preformed on those images.

### *4. Getting the Contours*

## The Objects
There are 3 objects used in the main process 


```
Vision(filters, directions_functions, target amount,
```
