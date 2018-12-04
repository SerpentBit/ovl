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
The low bound's saturation and/or value are changed to match the specific image.

### *4. Getting the Contours*
Before you read this make sure you understand what [contours]() are and how the [hsv color space work]().
At the time of creating this file OVL only supports color based contour detection and not simply edge detection.
Future patches will include additional methods of detecting contours.

In OVL Contours are found only by creating a mask of the image where the pixels within a wanted range are white
and everything else is black. Then contours are then found by edge detection on the image mask (The Image that is only black and white)
In order to get contours we use the `get_contours` function to get contours from an image.
Unlike CV2, Color (Ranges of color, not a specific tone) in OVL are defined using the Color and MultiColor Objects.
Read more about them in their documentations: [Color](), [MultiColor]()

For now just know that they represent a range for color.

>Note: Currently only the Hsv color space is supported, RGB BGR and LAB will be supported in an upcoming patch.

The color object consists of a low hsv bound and a high hsv bound and any color counts as in that range
if the color's h value is in the larger that the low bound's h value and smaller oe equal to the high bound h value
For example:
```
color = [h ,  s  , v ]
tone1 = [87, 160, 150]
tone2 = [87, 90, 150]
green = Color(low=[45, 100, 100], high=[75, 255, 255])
```
in this example `tone1` is within the green color range beacause all of the values are within the bounds declared by 
the green color object. On the other hand `tone2` is not, beacuse it's v value is below the lower bound.
Remember all values (h s v) must be in the range.

In the code below only the `color` parameter is displayed beacuse that is only relevant to us currently.
Even though the following code is valid it is recommended to use a function that also applies filters
and that can deal with MultiColor objects. (When getting contours for MultiColor objects use [MultiColor.get_contours()]()
Example image & code:

```
v = Vision(..., color=BuiltInColors.green)
img = 'Drive:/path/to/image/Shapes.png'
v.get_contours(img)
v.display_contours(img)

```

Result:


Like in OpenCV for python OVL uses Numpy arrays for images and contours.

## The Objects
There are 3 objects used in the main process 


```
Vision(filters, directions_functions, target amount,
```
