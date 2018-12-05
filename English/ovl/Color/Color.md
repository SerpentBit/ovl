# The Color Object
The `Color` object represents a color range.
The `Color` object consists of 2 lists the length of 3
each list is a [h, s, v] range one is the lower bound and the other is a high bound.

`Color` is used for creating a mask of the image, all pixels with a color that is in the range of the `Color` object
are white in the mask and pixels who arent in the range are black.
