from unittest import TestCase

import pytest
import os
import skimage.io as si
import numpy as np
from photomosaic.image_distance.image_distance import ImageDistance, CandidateImageDistanceGrid
from photomosaic.exceptions import InvalidTypeException, InvalidShapeException


class TestImageDistance(TestCase):
    # We load the images from the resources directory
    test_dir = os.path.dirname(__file__)
    img_3x4_000000 = si.imread(os.path.join(test_dir, 'resources', '3x4_000000.png'))
    img_3x4_123456 = si.imread(os.path.join(test_dir, 'resources', '3x4_123456.png'))
    img_3x4_d29c55 = si.imread(os.path.join(test_dir, 'resources', '3x4_d29c55.png'))
    img_3x4_ffffff = si.imread(os.path.join(test_dir, 'resources', '3x4_ffffff.png'))
    img_3x4_black_stripe = si.imread(os.path.join(test_dir, 'resources', '3x4_black_stripe.png'))
    img_3x4_white_stripe = si.imread(os.path.join(test_dir, 'resources', '3x4_white_stripe.png'))
    img_4x3_000000 = si.imread(os.path.join(test_dir, 'resources', '4x3_000000.png'))

    def test_different_shapes(self):
        """Test that two image arrays of different shapes raises the appropriate exception"""
        with pytest.raises(InvalidShapeException):
            ImageDistance(self.img_3x4_ffffff, self.img_4x3_000000)

    def test_incorrect_dtype(self):
        """Test that an image array of incorrect datatype raises the appropriate exception"""
        changed_type = self.img_3x4_ffffff.astype(int)
        with pytest.raises(InvalidTypeException):
            ImageDistance(self.img_3x4_ffffff, changed_type)

    def test_white_vs_black(self):
        """Test that a plain white and plain black image have the maximum distance"""
        distance = ImageDistance(self.img_3x4_ffffff, self.img_3x4_000000)
        assert distance == pytest.approx(255)

    def test_alternating_stripe(self):
        """Test that two inverted images of white and black have the maximum distance"""
        distance = ImageDistance(self.img_3x4_white_stripe, self.img_3x4_black_stripe)
        assert distance == pytest.approx(255)

    def test_white_stripe(self):
        """Test that two images that are identical in 75% of pixels and different in 25% have 25% of the max distance"""
        distance = ImageDistance(self.img_3x4_white_stripe, self.img_3x4_000000)
        assert distance == pytest.approx(63.75)

    def test_complex_vs_bw(self):
        """Test that we can calculate the image distance between a complex shade and black and white"""
        # The complex image is always 123456 in hex, which is (18, 52, 86) in decimal
        # This has an average distance of 52 to black (0, 0, 0) and 203 to white (255, 255, 255)
        # As the image we compare to is 25% black and 75% white, we expect the average distance to be 165.25
        distance = ImageDistance(self.img_3x4_black_stripe, self.img_3x4_123456)
        assert distance == pytest.approx(165.25)

    def test_complex_vs_complex(self):
        """Test that we can calculate the image distance between two images of complex shades"""
        # The first image is 123456 in hex, which is (18, 52, 86) in decimal
        # The second image is d29c55 in hex, which is (210, 156, 85) in decimal
        # This gives pixel distances of (192, 104, 1), which average to 99
        distance = ImageDistance(self.img_3x4_123456, self.img_3x4_d29c55)
        assert distance == pytest.approx(99)


class TestCandidateImageDistanceGrid(TestCase):
    # We construct a series of sample arguments that will be used in the tests
    # The candidate will be a 1x1 image of FF000000
    sample_candidate_image = np.array([[[255, 0, 0]]], dtype=np.uint8)
    # The target image will be a 2x2 grid of FF0000,00FF00,0000FF,FF00FF
    sample_target_images = np.array([
        [
            np.array([[[255, 0, 0]]], dtype=np.uint8),
            np.array([[[0, 255, 0]]], dtype=np.uint8)
        ],
        [
            np.array([[[0, 0, 255]]], dtype=np.uint8),
            np.array([[[255, 0, 255]]], dtype=np.uint8)
        ]])

    def test_calculate_distances(self):
        """Test that the comparison can be correctly calculated"""
        expected_distances = np.array([[0, 170], [170, 85]])
        cd = CandidateImageDistanceGrid(self.sample_candidate_image, self.sample_target_images)
        cd.calculate()
        assert cd.grid_shape == (2, 2)
        assert cd.comparison_shape == (1, 1)
        assert expected_distances == cd.distance_grid

    def test_different_comparison_target_shapes(self):
        """Test that if the candidate image is a different shape to the target images the appropriate exception is raised"""
        test_candidate_image = np.array([[[255, 0, 0], [255, 0, 0]]], dtype=np.uint8)
        with pytest.raises(InvalidShapeException):
            CandidateImageDistanceGrid(test_candidate_image, self.sample_target_images)

    def test_inconsistent_target_shapes(self):
        """Test that if the target images are not all the same shape the appropriate exception is raised"""
        test_target_images = self.sample_target_images.copy()
        test_target_images[0, 0] = np.array([[[255, 0, 0], [255, 0, 0]]], dtype=np.uint8)
        with pytest.raises(InvalidShapeException):
            CandidateImageDistanceGrid(self.sample_candidate_image, test_target_images)

    def test_incorrect_candidate_dtype(self):
        """Test that if the candidate image does not have the correct dtype the appropriate exception is raised"""
        test_candidate_image = np.array([[[255, 0, 0]]], dtype=np.int)
        with pytest.raises(InvalidTypeException):
            CandidateImageDistanceGrid(test_candidate_image, self.sample_target_images)

    def test_incorrect_target_dtype(self):
        """Test that if the target image does not have the correct type the appropriate exception is raised"""
        test_target_images = np.array([
            [
                np.array([[[255, 0, 0]]], dtype=np.int),
                np.array([[[0, 255, 0]]], dtype=np.int)
            ],
            [
                np.array([[[0, 0, 255]]], dtype=np.int),
                np.array([[[255, 0, 255]]], dtype=np.int)
            ]])
        with pytest.raises(InvalidTypeException):
            CandidateImageDistanceGrid(self.sample_candidate_image, test_target_images)
