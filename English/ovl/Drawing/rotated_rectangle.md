# Drawing.rotated_rectangle

Draws a rectangle rotated around its gives start point (the top left corner)

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
|image |No default | str, ndarray (numpy array) | N/A  | The image on which the rectangle should be drawn |
| start_point | No default | tuple (int, int) | (0 to image width, 0 to image height)| The left top corner of the rectangle|
|dimesions| No Default | tuple (int, int) | (0 to larger image dimension, 0 to larger image dimension) |
|angle| 360 (random value)| float (angle in degrees) |  0 to 359| The angle of rotation in degrees around the top left corner|
| color | (0,0,0) (RGB for black)| tuple (int, int, int)| (0 to 255, 0 to 255, 0 to 255) depends on color space| The color of the rectangle|
| thickness | 1| int| x > 1| The thickness of the shape in pixels|

Example code:

```
image = ovl.Drawing.white_image(width=640, height=480) # create an empty image that is white

ovl.Drawing.rotated_rectangle(image, (50, 100), (100, 150), angle=45,  color=(255, 0, 0), thickness=3)
```

Result:

![](https://github.com/1937Elysium/Ovl-Python/blob/master/Pictures/Sample%20Pictures/blank.png)
