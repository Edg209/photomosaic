import numpy as np
import skimage.io as si

def ImageDistance(img1: np.ndarray, img2:np.ndarray) -> float:
    """
    Calculate the image distance between two images of the same shape.
    The image distance is the average of all the pixel distances of the two images.

    Each image is represented by a ndarray of shape (X,Y,3). X and Y are the same between both images.
    Along the third axis the value of the pixel is given in RGB format - three integers between 0 an 255.
    To calculate the pixel distance, we treat each pixel as a point in 3 dimensional space, and find the L1 distance.
    As each of R, G or B distance can be between 0 and 255, the pixel distance is between 0 and 765.

    :param img1: numpy.ndarray of the RGB values of one of the images. Must have datatype numpy.uint8.
    :param img2: numpy.ndarray of the RGB values of the second image. Must have datatype numpy.uint8.
    :return: float of the image distance. Is in the range [0,765].
    """
    raise NotImplementedError
