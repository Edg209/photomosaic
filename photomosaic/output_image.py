import os

import numpy as np
import skimage.io as si


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

    def __init__(self, image_grid: np.ndarray, image_directory: str):
        """
        Construct an OutputImage of the chosen optimal images at each location on the grid.

        :param image_grid: numpy.nparray of the names of the images to be used at each point in the grid.
        :param image_directory: str of the path where each of the images in the image grid is located
        """
        self.grid_shape = image_grid.shape
        self.candidate_images = {image_name: si.imread(os.path.join(image_directory, image_name)) for image_name in np.unique(image_grid)}
        self._image_grid = image_grid
        self.assembled_image = None

    def assemble(self):
        self.assembled_image = np.vstack(np.hstack(self.candidate_images[cell] for cell in row)for row in self._image_grid)

    def output_to_png(self, filepath: str):
        si.imsave(filepath, self.assembled_image)
