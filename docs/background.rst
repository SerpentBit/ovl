.. background

===========
Background
===========

Ovl Simplifies much of the task of creating computer vision pipelines

In order to reduce the task of creating the pipeline ovl has a heavy use of partial functions,
here is a simple recap of partial functions.


Partial functions
=================

Partial function is a function that takes arguments in 2 stages.

This is a partial functions life cycle:

1. First Call - load arguments to create a loaded partial function

2. Second and all consecutive calls - actually calls the function with the parameters


For an example we will use gaussian_blur, a function that takes an image and blurs it.

The cv2 version of this function receives its image and some other and blurs the image

As a partial function gaussian blur acts as following:

.. code-block::

    import ovl

    loaded_function = ovl.gaussian_blur(kernel_size=(5,5), sigma_x=5)  # First call

    image1 = ovl.open_image("image.png")
    image2 = ovl.open_image("image.png")

    blurred_image1 = loaded_function(image1) # Second Call
    blurred_image2 = loaded_function(image2) # Third Call

    ovl.display_image(blurred_image1)
    ovl.display_image(blurred_image2)


This behaviour of multiple calls allows the creation of filter functions in ovl

Filter functions have 2 main types, image_filter functions and target_filter functions

image filters are functions that modify the image in a certain way
examples of this is rotating the image, blurring it, sharpening or any other change of the image

target_filters are functions that interact with the targets detected in the image,
you can read more on target_filters in getting started


Thresholding
============

This part is mostly relevant if you are not familiar with image thresholding.

Thresholding  is a pattern of detect objects by find contours of shapes in a binary image


binary image is an image of the same size of your original image but instead of pixels having a value of a color
or a greyscale value, each pixel has a value of 1 or 0, true or false, on or off.

The binary image (also called a mask), is created by thresholding an image, that means setting some sort of threshold on values
of the image, for example a color value (color, multi color range), a greyscale values (binary thresholding),
edges in the image (canny edge detection) or by background vs foreground (otsu).

After creating the binary image contours (outline of our targets) are found.

You can find more resources on thresholding here:

* Binary and Otsu - https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html

* Color - https://docs.opencv.org/master/da/d97/tutorial_threshold_inRange.html

* Canny Edge Detection - https://www.docs.opencv.org/master/da/d22/tutorial_py_canny.html

