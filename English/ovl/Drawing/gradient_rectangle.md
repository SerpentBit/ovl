# Drawing.gradient_rectangle


| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
|image |No default | str, ndarray (numpy array) | N/A  | The image on which the rectangle should be drawn |
| start_point | No default | tuple (int, int) | (0 to image width, 0 to image height)| The left top corner of the rectangle|
|dimesions| No Default | tuple (int, int) | (0 to larger image dimension, 0 to larger image dimension) |
|angle| 360 (random value)| float (angle in degrees) |  0 to 359| The angle of rotation in degrees around the top left corner|
| color | (0,0,0) (RGB for black)| tuple (int, int, int)| (0 to 255, 0 to 255, 0 to 255) depends on color space| The starting color of the rectangle|
|gradient | ('2*x', '2*x', '2*x')| tuple (str, str, str)| N/A| The grade of the shape, see [Grade]()|

</br>

## *Gradient*
Gradient is a tuple that defines the change in color for every pixel in the shape.
The string is a mathemtical function where the symbol x is the pixels index.
Each index in the gradient is a change in a different value
If the image is in the RGB color space then the first index is the change in the R value,
the second index in the G Value and the third in the B Value.
All of the functions available are:

| symbol| function| example| description|
|:---:|:---:|:---:|:---:|
|x | N/A | x| change is simply based on the index|
|+| addition| 5 + x| pixel plus 5|
|-| subtract| x - 3| pixel minus 3|
|*| multiplication| 2*x| pixel times 2|
| / | division| x/3| x divided by 3|
|%| modulus| x%2| the remainder of x divided by 2|
|**| exponant| x**2| x*x|
|log()| logarithim function| log(x,2) log(x)| log x in base 2 log x in base e|
|sin()| sine function| sin(30)| sine of 30 (0.5)|
|cos()| cosine function| cos(-120)| cosine of -120 (-0.5)|
|tan()| tangent function| tan(45)| tangent of 45 (1)|
|()| parentheses| 3*(x-2)| subtracts 2 from x and then multiplies by 3|
|fact()| factorial| fact(x)| the factorial of x|

</br>

## Grade Codes
Grade codes determine where the gradient starts
there are 8 blur codes:

|Code|Meaning| Inner Code (do not use)|
|:---:|:---:|:---:|
|GRADE_N| Gradient from top to bottom|0|
|GRADE_NW|Gradient from the top left corner|1|
|GRADE_W|Gradient from left to right|2|
|GRADE_SW|Gradient from the bottom left corner|3|
|GRADE_S|Gradient from bottom to top|4|
|GRADE_SE|Gradient from the bottom right corner|5|
|GRADE_E|Gradient from right to left|6|
|GRADE_NE|Gradient from the top right corner|7|
|GRADE_CENTER|Gradient from the center of the shape|8|

</br>


Code example:
```
img = white_image(width=320, height=240)  # create a blank white image
g = ('0.75*x', '0.75*x', '0.75*x')
gradient_rectangle(img, (50, 50), (100, 100), angle=25, color=(0, 25, 0), gradient=g, grade=ovl.Drawing.GRADE_NW)
```
</br>

Result:

![](https://github.com/1937Elysium/Ovl-Python/blob/master/Pictures/Sample%20Pictures/gradient_rotated_rectangle.png)
