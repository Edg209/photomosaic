from unittest import TestCase

import numpy as np
import pytest
from photomosaic.output_layout.output_layout import OutputLayout
from photomosaic.exceptions import InvalidShapeException

class TestOutputLayout(TestCase):

    sample_distances = {
        'img1' : np.array([[10,20],[30,40]]),
        'img2' : np.array([[15,15],[15,15]]),
        'img3' : np.array([[50,5],[50,50]])
    }

    def test_calculate(self):
        """Test that we can correctly calculate the optimal images for a series of candidate images"""
        ol = OutputLayout(self.sample_distances)
        ol.calculate()
        expected_img_grid = np.ndarray([['img1','img3'],['img2','img2']])
        assert expected_img_grid == ol.image_grid

    def test_inconsistent_grid_shape(self):
        """Test that if the grid shapes are not all the same shape the appropriate exception is raised"""
        test_distances = self.sample_distances.copy()
        test_distances['img2'] = np.array([[15,15],[15,15],[15,15]])
        with pytest.raises(InvalidShapeException):
            OutputLayout(test_distances)