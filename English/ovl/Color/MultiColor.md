# MultiColor Objects

The `MultiColor` object represents an non-uniform color range.
Some times we want color ranges with varying s and v levels.
Or we want a form of red. Red requires  
The `Color` object consists of 2 lists the length of 3
each list is a [h, s, v] range one is the lower bound and the other is a high bound.

`Color` is used for creating a mask of the image, all pixels with a color that is in the range of the `Color` object
are white in the mask and pixels who arent in the range are black.

>The color space is currently only the HSV Color space, an upcoming patch will allow for additional colorspaces.

| Name | Parameter Name | Default Value | Attribute Name | Encapsulation |  Value Types | Possible Range |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |  
| Color ranges | colors | No Default | colors | Public| list of `Color` objects |depends on color space, see [here]()|
| Color Space| color_space | 'hsv' | color_space | Private | str (string) | see supported color spaces |

## *Supported Color Spaces*
Color spaces are ways to express color, OVL's default color space is HSV
Currently supported Color Spaces and according low and high ranges:

| Color Space | Value order | Minimum values | Maximum value |
|:-----------:|:-----------:|:--------------:|:-------------:|
| HSV| [h, s, v]| [0, 0, 0]| [179, 255, 255]|
