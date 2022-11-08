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
    We will shortcut and find the average of all RGB distances, equivalent to the L1 distance divided by 3.

    :param img1: numpy.ndarray of the RGB values of one of the images. Must have datatype numpy.uint8.
    :param img2: numpy.ndarray of the RGB values of the second image. Must have datatype numpy.uint8.
    :return: float of the image distance. Is in the range [0,255].
    """
    raise NotImplementedError

class CandidateImageDistanceGrid(object):
    """
    An object that represents the image distance of a comparison candidate image to a grid of comparison target images.

    Attributes:
        grid_shape: A tuple giving the x,y size of the grid of comparison target images
        comparison_shape: A tuple giving the x,y size of each comparison image
        distance_grid: A numpy.ndarray of floats giving the image distance of the candidate to each target image

    Methods:
        calculate: Populate distance_grid with image distances
        output_to_csv: Save the values of distance_grid to a csv file
    """

    def __init__(self, candidate_image: np.ndarray, target_images: np.ndarray):
        """
        Construct an iterator from the candidate image

        :param candidate_image: a numpy.ndarray of shape (X,Y,3) where (X,Y) is the comparison shape and each entry has dtype uint8
        :param target_images: a numpy.ndarray of shape (A,B) where (A,B) is the grid shape and each entry is a numpy.ndarray of the same shape and dtype as candidate_image
        """
        raise NotImplementedError

    def calculate(self):
        raise NotImplementedError

    def output_to_csv(self):
        raise NotImplementedError