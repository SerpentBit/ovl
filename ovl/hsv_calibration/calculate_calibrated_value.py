def calculate_calibrated_value(image_mean, vector):
    """
     Solves the calibration equation that finds the optimal low bound value for
            the saturation and value.
    :param image_mean: the mean if the image of which
    :param vector: the dictionary containing the coefficients and group mean.
     Calculated using Color HSVCalibration
    :return: the optimal low bound
    """
    data_mean = vector['mean'][0]
    z_mean = data_mean[0] * vector['coefficient1'] + data_mean[1] * vector['coefficient2']
    return (z_mean - (image_mean * vector['coefficient1'])) / vector['coefficient2']
