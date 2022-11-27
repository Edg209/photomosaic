import os
from unittest import TestCase

import numpy as np
import skimage.io as si
from main.output_image import OutputImage


class TestOutputImage(TestCase):
    test_dir = os.path.dirname(__file__)
    sample_image_grid = np.array([['3x4_white_stripe.png', '3x4_white_stripe.png', '3x4_white_stripe.png', '3x4_white_stripe.png'],
                                  ['3x4_black_stripe.png', '3x4_black_stripe.png', '3x4_black_stripe.png', '3x4_black_stripe.png'],
                                  ['3x4_white_stripe.png', '3x4_white_stripe.png', '3x4_white_stripe.png', '3x4_white_stripe.png'],
                                  ['3x4_white_stripe.png', '3x4_white_stripe.png', '3x4_white_stripe.png', '3x4_white_stripe.png'],
                                  ])
    sample_image_directory = os.path.join(test_dir, 'resources')
    sample_expected_image = si.imread(os.path.join(sample_image_directory, '12x16_stripes.png'))

    def test_assemble(self):
        """Test that we can correctly assemble an output image from a grid of chosen candidate images"""
        oi = OutputImage(self.sample_image_grid, self.sample_image_directory)
        oi.assemble()
        assert np.array_equal(self.sample_expected_image, oi.assembled_image)
