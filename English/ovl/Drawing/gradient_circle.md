# Drawing.gradient_cirle


| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
|image |No default | str, ndarray (numpy array) | N/A  | The image on which the circle should be drawn |
| start_point | No default | tuple (int, int) | (0 to image width, 0 to image height)| The center of the circle|
|dimesions| No Default | int| 0 to half the smaller dimension | The radius of the circle|
| tanget_angle| 360 (random value)| float (angle in degrees) |  0 to 359| The angle of rotation from which the gradient starts|
| color | (0,0,0) (RGB for black)| tuple (int, int, int)| (0 to 255, 0 to 255, 0 to 255) depends on color space| The starting color of the circle|
|gradient | ('2*x', '2*x', '2*x')| tuple (str, str, str)| N/A| The grade of the shape, see [Grade](https://github.com/1937Elysium/Ovl-Python/new/master/English/ovl/Drawing#gradient)|

</br>
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
</br>

Code example:
```
img = white_image(width=320, height=240)  # create a blank white image
g = ('1.75*x', '1.75*x', '1.75*x')
gradient_circle(img, (50, 50), 50, tangent_angle=25, color=(25, 50, 25), gradient=g)

```

result:

![](https://github.com/1937Elysium/Ovl-Python/blob/master/Pictures/Sample%20Pictures/gradient_circle.png)
