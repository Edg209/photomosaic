import numpy as np
from exceptions import InvalidShapeException


class OutputLayout(object):
    """
    An object that represents a layout of output images that resemble a target image.

    Attributes:
         grid_shape: A tuple giving the x,y size of the grid of images
         candidate_images: A set of each strings of the names of each of the candidate images that are optimal at least once
         image_grid: A numpy.ndarray of strings of the names of the optimal image to use at each location of the grid

    Methods:
        calculate: Populate image_grid with the optimal image names
        output_to_csv: Save the values of image_grid to a csv file
    """

    def __init__(self, image_distances: dict[str, np.ndarray]):
        """
        Construct an OutputLayout of the optimal images at each location on the grid

        :param image_distances: a dict where each key is the name of a candidate image and each value is a numpy.ndarray giving the image distance of the candidate at each location of the grid
        """
        # We determine the value of grid_shape and make sure it is consistent
        self.grid_shape = None
        for arr in image_distances.values():
            if self.grid_shape is None:
                self.grid_shape = arr.shape
            elif self.grid_shape != arr.shape:
                raise InvalidShapeException
        self._image_distances = image_distances
        self.candidate_images = None
        self.image_grid = None

    def calculate(self):
        # We will loop over every image and choose it at a location if it has a smaller distance than any image chosen so far
        best_candidates = np.full(self.grid_shape, '', dtype=str)
        best_distances = np.full(self.grid_shape, 1000, dtype=float)  # The maximum of any distance is 255, so any calculated distance will be better than this
        for (candidate, distances) in self._image_distances.items():
            improvement_mask = distances < best_distances
            best_candidates = np.where(improvement_mask, candidate, best_candidates)
            best_distances = np.where(improvement_mask, distances, best_distances)
        self.image_grid = best_candidates
        self.candidate_images = np.unique(best_candidates)

    def output_to_csv(self, filepath: str):
        np.savetxt(filepath, self.image_grid, delimiter=',')
