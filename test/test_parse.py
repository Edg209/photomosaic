import os
from unittest import TestCase

import pytest
from photomosaic.input_parse.parse import InputParser


class TestParse(TestCase):
    test_dir = os.path.dirname(__file__)
    sample_parameters = {'photomosaic_folder': os.path.join(test_dir, 'parse_test'),
                         'target_image': os.path.join(test_dir, 'resources', '3x4_white_stripe.png'),
                         'candidate_image_folder': os.path.join(test_dir, 'parse_test_candidates'),
                         'grid_x': 4,
                         'grid_y': 4,
                         'output_x': 6,
                         'output_y': 8,
                         'comparison_x': 3,
                         'comparison_y': 4
                         }

    def test_parse_correct(self):
        """Test that a correctly formatted input will set up the correct folder structure and populate them with the correct images"""
        raise NotImplementedError

    def test_folder_already_exists(self):
        """Test that if the photomosaic folder already exists the appropriate exception is raised"""
        raise NotImplementedError

    def test_missing_target_image(self):
        """Test that if the target image does not exist the appropriate exception is raised"""
        raise NotImplementedError

    def test_missing_candidate_image_folder(self):
        """Test that if the candidate image folder does not exist the appropriate exception is raised"""
        raise NotImplementedError

    def test_invalid_grid_shape(self):
        """Test that if the grid x and y dimensions are not positive integers the appropriate exception is raised"""
        raise NotImplementedError

    def test_invalid_output_shape(self):
        """Test that if the output x and y dimensions are not positive integers the appropriate exception is raised"""
        raise NotImplementedError

    def test_invalid_comparison_shape(self):
        """Test that if the comparison x and y dimensions are not positive integers the appropriate exception is raised"""
        raise NotImplementedError
