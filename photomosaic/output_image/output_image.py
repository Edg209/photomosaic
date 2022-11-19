import numpy as np


class OutputImage(object):
    """
    An object that represents an image composed of several candidate images arranged in a grid.

    Attributes:
        grid_shape: A tuple giving the x,y size of the grid of images.
        candidate_images: A dict that maps the name a candidate image to a numpy.ndarray of the RGB values of that image.
        assembled_image: A numpy.ndarray of RGB values of the assembled image.

    Methods:
        assemble: Populate assembled_image with the RGB values of the assembled image
        output_to_png: Save the values of assembled_image as a png file
    """

    def __init__(self, image_grid: np.ndarray):
        """
        Construct an OutputImage of the chosen optimal images at each location on the grid.

        :param image_grid: numpy.nparray of the names of the images to be used at each point in the grid.
        """
        raise NotImplementedError

    def assemble(self):
        raise NotImplementedError

    def output_to_png(self):
        raise NotImplementedError
