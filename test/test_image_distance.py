from unittest import TestCase

import pytest
import os
import skimage.io as si

test_dir = os.path.dirname(__file__)

class TestImageDistance(TestCase):

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
