.. _getting_started:

=========================
Getting Started with OVL
=========================

Vision Object
=============

The main functionality offered by ovl is the *Vision* object.
Vision represents a Computer Vision detection pipeline used to guide and streamline Computer Vision.

The Vision object takes an image as its input, it can be either a color or greyscale image.

The Vision has 4 stages, each one is a logical process on the image or data extracted from it.
You can use some or all of them, depending on your application.
Each

1. Processing
2. Detection
3. Filtering
4. Conversion & Usage

If this is your first time writing a computer vision pipeline you should start by writing a pipeline only with stage
2 and 3!


Processing
==========

Processing the first stage in the pipeline and focuses on preparing the input image for Detection
Although not required at first it is usually important for improving reliability.

.. code-block::

    import ovl

    image_filters = [ovl.gaussian_blur((5,5), sigma_x=5), ovl.rotate_image(90)]

    pipeline = ovl.Vision(image_filters=image_filters, camera=0)

    while True:
        image = pipeline.get_image()

        filtered_image = pipeline.apply_image_filters(image)

        ovl.display_image(filtered_image, display_loop=True)


Detection
=========

Detection is the most important stage, it is responsible for detecting the object(s) wanted or any other
detection action relevant for the pipeline.

Detection can use a number of algorithms, such as color detection, Canny edge detection, binary thresholding, haar-cascade,
and many more.

The object used to detect is called Detector, there are some built in detectors, such as Threshold Detector which
can be used to apply detections that find contours in a binary image, This includes Canny Edge Detection, Color based
thresholding  (finding an object in the image using color), Binary Thresholding (including Otsu binarization),

After the detection stage you should pass a list of object(s) either a contour, bounding rectangle or any other
way to describe targets.



Filtering
=========

Filtering is a stage that expands on the raw targets found in the Detection Stage

Filtering is a stage with 3 functions:

1. Remove objects that were detected in the previous stage that are
2. In applications that implement some form of pairing or grouping
3. Sort the targets by some property (size, shape, location in image etc.)




Conversion & Usage
==================

Conversion & Usage is the the final stage of the pipeline and is used a stage to gap detection values which exist
only in your image to values that have meaning to what you want to do.

For example, if you want to create a pipeline that detects if a red light or green light is turned or none at all.
The information you would get after filtering would be there is an object (in the color red or green) with its center at (x,y) in
the image or that no object was detected. But this doesnt help use return an answer of:

1. there is a red object
2. there is a green object
3. there is no object

In order

.. note::

    Remember to consider the case of no detected objects!

There are 2 main objects used in this stage Director and Connection.

The Director object is used to take the result of the Detection and Filtering stages and convert them
to data that can be used by your application.

The director does 3 things:
1. Select the "target_amount" of targets that are considered to have passed all the stages (this stage can be skipped by passing
math.inf or 0 - no limit) if there are not enough, return failed value

2. Applies the direction_function on the target and the image - this converts

3. `Direction Modifiers <ovl.direction\_modifiers.direction\_modifier>`, these are object that add logical layers


.. code-block::

    import ovl

    director = ovl.Director(direction_function=ovl.target_amount=2, failed_value=)








