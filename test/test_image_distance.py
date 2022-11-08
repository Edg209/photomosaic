from unittest import TestCase

import pytest
import os
import skimage.io as si


class TestImageDistance(TestCase):
    # We load the images from the resoures directory
    test_dir = os.path.dirname(__file__)
    img_3x4_000000 = si.imread(os.path.join(test_dir, 'resources', '3x4_000000.png'))
    img_3x4_123456 = si.imread(os.path.join(test_dir, 'resources', '3x4_123456.png'))
    img_3x4_d29c55 = si.imread(os.path.join(test_dir, 'resources', '3x4_d29c55.png'))
    img_3x4_ffffff = si.imread(os.path.join(test_dir, 'resources', '3x4_ffffff.png'))
    img_3x4_black_stripe = si.imread(os.path.join(test_dir, 'resources', '3x4_black_stripe.png'))
    img_3x4_white_stripe = si.imread(os.path.join(test_dir, 'resources', '3x4_white_stripe.png'))

    def test_different_shapes(self):
        """Test that two image arrays of different shapes raises the appropriate exception"""
        raise NotImplementedError

    def test_incorrect_dtype(self):
        """Test that an image array of incorrect datatype raises the appropriate exception"""
        raise NotImplementedError

    def test_white_vs_black(self):
        """Test that a plain white and plain black image have the maximum distance"""
        raise NotImplementedError

    def test_alternating_stripe(self):
        """Test that two inverted images of white and black have the maximum distance"""
        raise NotImplementedError

    def test_white_stripe(self):
        """Test that two images that are identical in 75% of pixels and different in 25% have 25% of the max distance"""
        raise NotImplementedError

    def test_complex_vs_bw(self):
        """Test that we can calculate the image distance between a complex shade an black and white"""
        raise NotImplementedError

    def test_complex_vs_complex(self):
        """Test that we can calculate the image distance between two images of complex shades"""
        raise NotImplementedError
