import numpy as np
from exceptions import InvalidTypeException, InvalidShapeException


def image_distance(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Calculate the image distance between two images of the same shape.
    The image distance is the average of all the pixel distances of the two images.

    Each image is represented by a ndarray of shape (X,Y,3). X and Y are the same between both images.
    Along the third axis the value of the pixel is given in RGB format - three integers between 0 an 255.
    To calculate the pixel distance, we treat each pixel as a point in 3 dimensional space, and find the L1 distance.
    As each of R, G or B distance can be between 0 and 255, the pixel distance is between 0 and 765.
    We will shortcut and find the average of all RGB distances, equivalent to the L1 distance divided by 3.

    :rtype: float
    :param img1: numpy.ndarray of the RGB values of one of the images. Must have datatype numpy.uint8.
    :param img2: numpy.ndarray of the RGB values of the second image. Must have datatype numpy.uint8.
    :return: float of the image distance. Is in the range [0,255].
    """
    if img1.shape != img2.shape:
        raise InvalidShapeException
    if img1.dtype != np.uint8 or img2.dtype != np.uint8:
        raise InvalidTypeException
    img_diff = img1 - img2
    # For any particular location, if img1 is greater than or equal to img2, img_diff will contain the absolute difference.
    # If img1 is less than img2 at that location, img_diff will contain another uint8 that is equivalent to the negative value of the difference.
    # We can therefore multiply by -1 in the locations where img1 is less than img2 to get a ndarray of all the absolute differences.
    negative_mask = img1 < img2
    img_distances = np.negative(img_diff, where=negative_mask, out=img_diff)
    return np.average(img_distances)


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
        Construct a CandidateImageDistanceGrid for a candidate image

        :param candidate_image: a numpy.ndarray of shape (X,Y,3) where (X,Y) is the comparison shape and each entry has dtype uint8
        :param target_images: a numpy.ndarray of shape (A,B,X,Y,3) where (A,B) is the grid shape and each (X,Y,3) is a numpy.ndarray of the same shape and dtype as candidate_image
        """
        # Check that candidate_image is of the shape (X,Y,3)
        if len(candidate_image.shape) != 3:
            raise InvalidShapeException
        if candidate_image.shape[2] != 3:
            raise InvalidShapeException
        self.comparison_shape = candidate_image.shape[:2]
        # Check that grid_shape is of the shape (A,B,X,Y,3)
        if len(target_images.shape) != 5:
            raise InvalidShapeException
        if target_images.shape[2:4] != self.comparison_shape:
            raise InvalidShapeException
        if target_images.shape[4] != 3:
            raise InvalidShapeException
        self.grid_shape = target_images.shape[:2]
        # Check that candidate_image is the correct dtype
        if candidate_image.dtype != np.uint8:
            raise InvalidTypeException
        # Check that target_images is the correct dtype
        if target_images.dtype != np.uint8:
            raise InvalidTypeException
        # We have passed all input checks at this point
        self._candidate_image = candidate_image
        self._target_images = target_images
        self.distance_grid = None

    def calculate(self):
        distances = [[image_distance(self._candidate_image, cell) for cell in row] for row in self._target_images]
        self.distance_grid = np.array(distances)

    def output_to_csv(self, filepath: str):
        np.savetxt(filepath, self.distance_grid, delimiter=',')
