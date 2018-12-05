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
`Parameter: camera_port=None -> integer >= 0 or str for video files.`

If there is only 1 camera connected to the device pass: `camera_port=0`
When developing the code on a laptop or PC make sure you are using the port refering to the camera.
If you have one additional camera connected try changing to `camera_port=1` and making sure you return to 0 when finalizing the code.

#### Width and Height 
`Parameter: width=240 -> interger > 0, height=240 (in pixels) -> integer > 0`

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
#  color = [h ,  s  , v ]
>>> tone1 = [87, 160, 150]
>>> tone2 = [87, 90, 150]
>>> green = Color(low=[45, 100, 100], high=[75, 255, 255])
>>> green.in_range(tone1)
True
>>> green.in_range(tone2)
False
```
In this example `tone1` is within the green color range beacause all of the values are within the bounds declared by 
the green color object thus it returns `True`. On the other hand `tone2` is not, beacuse it's v value is below the lower bound
and thus returns `False`.
>Remember all values (h s v) must be in the range for the color to be in the Color object range.

In the code below only the `color` parameter is displayed beacuse that is only relevant to us currently.
Even though the following code is valid it is recommended to use a function that also applies filters
and that can deal with MultiColor objects. (When getting contours for MultiColor objects use [MultiColor.get_contours()]()
> Note: we are using image in the png format, other formats are supported as well.
Example image & code:

```
v = Vision(..., color=BuiltInColors.green)
img = '/path/to/image/Shapes.png'
v.get_contours(img)
v.display_contours(img)

```

Result:

Original Image:
![](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/Shapes.png)


Contours found:
![](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/ShapesResult.png)

Like in OpenCV for python OVL uses Numpy arrays for images and contours.

### *5.Applying Filter Functions*
As we saw in the previous step getting the contours with color detection finds what we want but sometimes it also finds
objects that we don't want. Thats why Filter Functions exist, to remove contours that don't oblige to the characteristics that
we are looking for.

For those who are a tad rusty on their python  heres a quick refresh on functions.
Functions in python are defined as followed.
Functions like classes, modules and every other piece of data in python is an object.
A functions object is basically a group of code that can be called.
so when we call a function without parentheses we are telling python:
"Here is a bunch of code, don't execute it yet though"

```
def some_function():
    print(5)
b = somefunction  
```

The variable `b` now holds the function `some_function`
Filter Functions are literal functions (created with the def keyword in python)
that are passed to the Vision object without being called.
So if we now execute the following code:

```
>>> b()
5
```

What basically happened is that we called the variable `b` and the variable `b` holds the function `some_function`
so python calls the function `some_function`

Using this mechanism we gain a powerful capability, we can call specific functions you the programmer wants,
when the Vision object needs to.


#### *So why are we not calling the functions right away*?
The Idea is we want the vision object to call these functions for us every time we find contours while going over live footage, a video file a series of images or even 
not only that we want to be able to call custom made fucntions in addition to existing ones (They located in ovl.Filters)

#### *Filters*
`Attribute: filters -> a list of function object that take a list of contours and returns one`

Functions provide the Vision object with the guidelines on what characteristics our target object
(or objects) are.
Lets look at the result from earlier:


![](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/ShapesResult.png)


Let's say we want to find only the rectangle, we can use the filter function `Filters.horizontal_rectangle_filter`
and apply the filter using the `Vision.apply_filter` function on our contours.
The code:
```
v = Vision(... , color=BuiltInColors.green_hsv)  # Define our Vision Object

img = '/path/to/image/Shapes.png'  # Path to our image

v.apply_sample(img=img)  # find contours for the range given

v.apply_filter(Filters.horizontal_rectangle_filter) # apply the horizontal_rectangle_filter

v.display_contours(img)  # display the contours we found

```

The Result:
![](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/ShapesFiltered.png)

We can see only the rectangle passed the filter and its our final result!

We found what we wanted!

We can do the same thing for the circle using `circle_filter`.

The code:
```
v = Vision(... , color=BuiltInColors.green_hsv)  # Define our Vision Object

img = '/path/to/image/Shapes.png'  # Path to our image

v.apply_sample(img=img)  # find contours for the range given

v.apply_filter(Filters.circle_filter) # apply the circle_filter

v.display_contours(img)  # display the contours we found

```

The Result:

![](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/ShapesSecondFiltered.png)

Oh no! Our filter also found the hexagon! But we only wanted the circle!
In order to find only the circle we need to tighten the range of the defenition of circle
we do that by changing the parameter given to the filter function (more exaplanations [here](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/Constructer%20(__init__).md#parameters))
After Changing the `min_area_ratio` parameter this is our result:

![](https://github.com/1937Elysium/Ovl-Python/blob/master/English/ovl/Vision/ShapesCircleFiltered.png)

#### *Parameters*
`Parameter: parameters -> a list of lists that contain additional parameter for the filter functions`

Sometimes we want to set different parameters to filter functions we pass, a different `min_area` limit for an `area_filter`
A different `min_len_ratio` limit for a `circle_filter`, or some parameter for a custom filter you made.
In that case we need to pass them through the `parameters` keyword.
here is the example for a vision object with filter functions and parameters.


`Vision(filters=[area_filter, circle_filter], parameters=[[100], [0.8, 0.7]], ...)`

Lets look at this one step at a time:
`filters` takes to filter functions, `area_filter` and `circle_filter`
but we want to a set specific parameters for our vision.

If we look at the documentation we can see that area filter takes 2 additional parameters
in addition to the contour list, `min_area` and `max_area`
Circle filters takes 2 additional parameters as well, `min_area_ratio` and `min_len_ratio`
Descriptions of these parameters can be found [here]()
So by passing `[[100], [0.8, 0.7]]` we tell the vision object to call the area filter
and `circle filter` like so:

```
contours = area_filter(contours, 100)
contours = circle_filter(contours, 0.8, 0.7)
```

by passing custom parameters through `parameters` we can change existing filter functions that come with OVL
and modify filter functions you or other people built.

Some times we want to sort the final contours in a specific order based on some property of a contour.
With the Sorters sub module there are 3 built in sorters: `descending_area_sort`, `ascending_area_sort` and `circle_sort`

##### *Making Filter Functions of your own*
There is a wide diversity of existing filter functions, but sometimes we need something more tailored to our
specific needs.
In that case we can create a function ourselves and follow a couple of simple rules:

1. The name of the function must end with 'filter' or 'sort' depending if its a filter or sorter function respectively
2. The first parameter of the filter function must be a contour_list (doesnt have to be called 'contour_list')
3. The filter function must return a filter function.
4. The function must contain the following code at its start:
```
    if type(<contour list parameter name>) is not list:
        <contour list parameter name> = [<contour list parameter name>]
```
There are other optional rules for additional features, they are all documented [here]()

### *6.Get Directions for the Robot*
`Parameters: directions_function-> function object, target_amount (amount of wanted contours) -> integer > 0`
>Note: These 2 final steps are mainly for FIRST Robotics Competition teams, though they can be modified for other uses
> and robotics like projects. This does require you to create a custom directions function.

After we applied all of the filter and found our one and only Contour(s) we can can directions for our robot.
The basic directions functions (`xy_center_directions`, `y_center_directions` and `x_center_directions`)
do the same thing for the diffrent axes find the center of the contour (or the center of the between all target contours
more on that [here]()) and multiply that by the 2000 / width of the image(or height or both depending on the function) .
```
center of the contour * (2000 / (width / height))  = direction the robot needs to turn/ move to
```
Why is that you might ask? 0 to 2000 are the possible values for this calculation. -1 to 1 are the possible turning factors for 
motors in the WPILib API So the more the object is to the right side of the image it means the robot is in an angle to the left
and needs to turn to the right and vice versa.

It is reccommended to create your own directions function depending on your needs.
There are many useful functions in the ContourMixin submodule, you can find it [here]().
Additional rescoures can be found [here](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_contours/py_table_of_contents_contours/py_table_of_contents_contours.html)

### *7.Sending the data to the RoboRIO*
`Parameters: roborio_name -> str  ip or hostname, port -> int 0 to 65535, failed_value -> str`
Sending data to the RoboRIO is done by using the function `send_to_roborio`, but before we send we need to connect to it.
The connection is a udp socket. You can connect using a hostname or an IP.

```
Vision(..., roborio_name='roboRIO-1937-FRC', port=61937)
```

The code written above is an example for udp connection with the RoboRIO Controller, currently only udp connections are
supported, in an upcoming patch more diverse connection types for non-FRC Uses as well.\

## *A bit about connections*
Netork connections work like real like addresses: Your the street you live in, your house number, country and city
are the IP address or in the Roborio's case the host name - basically a name identifiying the RoboRIO in the network.
Port is essentially the apartment number in the building you live in, many connections can occur at once, so the port number
is the identifier of the application. Wondering what number to pick? It's pretty arbitrary I recommend 6+ your team's number
as you can see in the example above `roboRIO-1937-FRC` is how Elysium's roboRIO is called. Port is 6**1937**.

In an upcoming patch more connection types will be available - mainly for non-FRC Teams, Bluetooth, tcp and more.
Default will always remain udp with a hostname to find the roborio as OVL's main purpose is FRC.


### *Parameter Recap*

| Name | Parameter Name | Default Value | Attribute Name | Encapsulation |  Value Types | Possible Range |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |  
| Filter Function list | None | filters | filters | Private | list of function objects | N/A |
| Directions Functions | None | directions_function | directions | Public | directions function object | N/A |
| Image Width | width | 320 | width | Public | int | x > 0 |
| Image Height | height | 240 | height | Public | int | x > 0 |
| Color Range | color | No default | color | Public | Color or MultiColor | N/A |
| Amount of target Contours | target_amount | 1 | target_amount | Public | int | x > 1 |
| Log File path  | log_file | None | log_path |  Public | bool, str, None | N/A |




