import json
import os
from unittest import TestCase, mock

import numpy as np
import pytest
import skimage.io as si
from photomosaic.parse import InputParser
from photomosaic.exceptions import InvalidShapeException


@mock.patch('skimage.io.imsave')
@mock.patch('shutil.copyfile')
@mock.patch('os.mkdir')
class TestParse(TestCase):
    test_dir = os.path.dirname(__file__)
    sample_parameters = {'photomosaic_folder': os.path.join(test_dir, 'parse_test'),
                         'target_image': os.path.join(test_dir, 'resources', '3x4_white_stripe.png'),
                         'candidate_image_folder': os.path.join(test_dir, 'parse_test_candidates'),
                         'grid_x': 4,
                         'grid_y': 3,
                         'output_x': 8,
                         'output_y': 6,
                         'comparison_x': 1,
                         'comparison_y': 1
                         }
    img_3x4_white_stripe = si.imread(os.path.join(test_dir, 'resources', '3x4_white_stripe.png'))

    def test_parse_correct(self, mocked_mkdir, mocked_copy, mocked_imsave):
        """Test that a correctly formatted input will set up the correct folder structure and populate them with the correct images"""
        mocked_json_load = mock.Mock(return_value=self.sample_parameters)
        pixel_000000 = np.array([[[0, 0, 0]]], dtype=np.uint8)
        pixel_ffffff = np.array([[[255, 255, 255]]], dtype=np.uint8)
        output_000000 = np.array([[[0, 0, 0] for y in range(6)] for x in range(8)])
        output_ffffff = np.array([[[255, 255, 255] for y in range(6)] for x in range(8)])
        with mock.patch('json.load', mocked_json_load):
            ip = InputParser('dummy_file_path')
            ip.parse()
            # Asserting that we attempt to read the JSON of parameters from the location given
            mocked_json_load.assert_called_once_with('dummy_file_path')
            # Asserting that the folder structure is created
            mocked_mkdir.assert_any_call(self.sample_parameters['photomosaic_folder'])
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_candidate_images'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'image_distances'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'output_candidate_images'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'output_layouts'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'output_images'))
            # Asserting that the original target image is copied
            mocked_copy.assert_called_once_with(self.sample_parameters['target_image'], os.path.join(self.sample_parameters['photomosaic_folder'], 'target_image.png'))
            # For asserting calls with a ndarray, we can't use assert_any_call directly, we have to instead use retrieve the call list and check the contents
            # We instead set up a dict with the path as the keys and ndarray as the values
            imsave_calls = {call[0][0]: call[0][1] for call in mocked_imsave.call_args_list}
            # Asserting that the comparison target images are saved
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '0x0.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '0x1.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '0x2.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '1x0.png')], pixel_ffffff)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '1x1.png')], pixel_ffffff)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '1x2.png')], pixel_ffffff)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '2x0.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '2x1.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '2x2.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '3x0.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '3x1.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images', '3x2.png')], pixel_000000)
            # Asserting that the comparison candidate images are saved
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_candidate_images', '3x4_000000.png')], pixel_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_candidate_images', '3x4_ffffff.png')], pixel_ffffff)
            # Asserting that the output candidate images are saved
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'output_candidate_images', '3x4_000000.png')], output_000000)
            assert np.array_equal(imsave_calls[os.path.join(self.sample_parameters['photomosaic_folder'], 'output_candidate_images', '3x4_ffffff.png')], output_ffffff)

    def test_folder_already_exists(self, mocked_mkdir, mocked_copy, mocked_imsave):
        """Test that if the photomosaic folder already exists the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['photomosaic_folder'] = os.path.join(self.test_dir, 'parse_test_candidates')
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(FileExistsError):
                InputParser('dummy_file_path')

    def test_missing_target_image(self, mocked_mkdir, mocked_copy, mocked_imsave):
        """Test that if the target image does not exist the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['target_image'] = os.path.join(self.test_dir, 'does_not_exist.png')
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(FileNotFoundError):
                InputParser('dummy_file_path')

    def test_missing_candidate_image_folder(self, mocked_mkdir, mocked_copy, mocked_imsave):
        """Test that if the candidate image folder does not exist the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['candidate_image_folder'] = os.path.join(self.test_dir, 'does_not_exist')
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(FileNotFoundError):
                InputParser('dummy_file_path')

    def test_invalid_grid_shape(self, mocked_mkdir, mocked_copy, mocked_imsave):
        """Test that if the grid x and y dimensions are not positive integers the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['grid_x'] = 1.5
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
        test_parameters = self.sample_parameters.copy()
        test_parameters['grid_x'] = -2
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')

    def test_invalid_output_shape(self, mocked_mkdir, mocked_copy, mocked_imsave):
        """Test that if the output x and y dimensions are not positive integers the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['output_y'] = 1.5
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
        test_parameters = self.sample_parameters.copy()
        test_parameters['output_y'] = -2
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')

    def test_invalid_comparison_shape(self, mocked_mkdir, mocked_copy, mocked_imsave):
        """Test that if the comparison x and y dimensions are not positive integers the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['comparison_x'] = 1.5
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
        test_parameters = self.sample_parameters.copy()
        test_parameters['comparison_x'] = -2
        mocked_json_load = mock.Mock(return_value=test_parameters)
        with mock.patch('json.load', mocked_json_load):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
