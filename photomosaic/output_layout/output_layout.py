import numpy as np

class OutputLayout(object):
    """
    An object that represents a layout of output images that resemble a target image.

    Attributes:
         grid_shape: A tuple giving the x,y size of the grid of images
         candidate_images: A set of each strings of the names of each of the candidate images
         image_grid: A numpy.ndarray of strings of the names of the optimal image to use at each location of the grid

    Methods:
        calculate: populate image_grid with the optimal image names
        output_to_csv: Save the values of image_grid to a csv file
    """

    def __init__(self, image_distances: dict[str, np.ndarray]):
        """
        Construct an OutputLayout of the optimal images at each location on the grid

        :param image_distances: a dict where each key is the name of a candidate image and each value is a numpy.ndarray giving the image distance of the candidate at each location of the grid
        """
        raise NotImplementedError

    def calculate(self):
        raise NotImplementedError

    def output_to_csv(self):
        raise NotImplementedError
