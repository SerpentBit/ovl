# The Color Object
The `Color` object represents a color range.
The `Color` object consists of 2 lists the length of 3
each list is a [h, s, v] range one is the lower bound and the other is a high bound.

`Color` is used for creating a mask of the image, all pixels with a color that is in the range of the `Color` object
are white in the mask and pixels who arent in the range are black.

>The color space is currently only HSV Color space, an upcoming patch will allow for additional colorspaces.

| Name | Parameter Name | Default Value | Attribute Name | Encapsulation |  Value Types | Possible Range |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |  
| Lower color range | low | No Default | low, low_bound, low_bound | Public, Private, Public| ndarray, (ndarray or list), list|depends on color space, see [here]()|
| Upper color range | high | No Default | high, high_bound, high_bound | Public, Private, Public| ndarray, (ndarray or list), list| depends on color space, see [here]()|
| Color Space| color_space | 'hsv' | color_space | Private | str (string) | see supported color spaces |

## *Supported Color Spaces*
Color spaces are ways to express color, OVL's default color space is HSV
Currently supported Color Spaces and according low and high ranges:

| Color Space | Value order | Minimum values | Maximum value |
|:-----------:|:-----------:|:--------------:|:-------------:|
| HSV| [h, s, v]| [0, 0, 0]| [179, 255, 255]|


`Color` has multiple useful functions for debugging like `.light()` and `.dark()` for quick changes to s and v values
In upcoming patches more tools will be added to use the Color Object.

`Color` is also used in the `GenerateImage` class in order to define a range of tones from which a color can be chosen for 
gradient object creation.

In order to have fast iterations of testing, There is a debugger tool that can be downloaded [here]()
The debugger has tools for quick iterations and then exporting it to a json file.
