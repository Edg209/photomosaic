import json
import os
from unittest import TestCase, mock

import pytest
from photomosaic.parse import InputParser
from photomosaic.exceptions import InvalidShapeException


@mock.patch('shutil.copyfile')
@mock.patch('os.mkdir')
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

    def test_parse_correct(self, mocked_mkdir, mocked_copy):
        """Test that a correctly formatted input will set up the correct folder structure and populate them with the correct images"""
        mocked_open = mock.mock_open(read_data=json.dumps(self.sample_parameters))
        with mock.patch('builtins.open', mocked_open):
            ip = InputParser('dummy_file_path')
            ip.parse()
            mocked_open.assert_called_once_with('dummy_file_path', 'r')
            mocked_mkdir.assert_any_call(self.sample_parameters['photomosaic_folder'])
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_candidate_images'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'comparison_target_images'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'output_candidate_images'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'output_layouts'))
            mocked_mkdir.assert_any_call(os.path.join(self.sample_parameters['photomosaic_folder'], 'output_images'))
            mocked_copy.assert_called_once_with(self.sample_parameters['target_image'], os.path.join(self.sample_parameters['photomosaic_folder'], 'target_image.png'))

    def test_folder_already_exists(self, mocked_mkdir, mocked_copy):
        """Test that if the photomosaic folder already exists the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['photomosaic_folder'] = os.path.join(self.test_dir, 'parse_test_candidates')
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(FileExistsError):
                InputParser('dummy_file_path')

    def test_missing_target_image(self, mocked_mkdir, mocked_copy):
        """Test that if the target image does not exist the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['target_image'] = os.path.join(self.test_dir, 'does_not_exist.png')
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(FileNotFoundError):
                InputParser('dummy_file_path')

    def test_missing_candidate_image_folder(self, mocked_mkdir, mocked_copy):
        """Test that if the candidate image folder does not exist the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['candidate_image_folder'] = os.path.join(self.test_dir, 'does_not_exist')
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(FileNotFoundError):
                InputParser('dummy_file_path')

    def test_invalid_grid_shape(self, mocked_mkdir, mocked_copy):
        """Test that if the grid x and y dimensions are not positive integers the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['grid_x'] = 1.5
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
        test_parameters = self.sample_parameters.copy()
        test_parameters['grid_x'] = -2
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')

    def test_invalid_output_shape(self, mocked_mkdir, mocked_copy):
        """Test that if the output x and y dimensions are not positive integers the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['output_y'] = 1.5
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
        test_parameters = self.sample_parameters.copy()
        test_parameters['output_y'] = -2
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')

    def test_invalid_comparison_shape(self, mocked_mkdir, mocked_copy):
        """Test that if the comparison x and y dimensions are not positive integers the appropriate exception is raised"""
        test_parameters = self.sample_parameters.copy()
        test_parameters['comparison_x'] = 1.5
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
        test_parameters = self.sample_parameters.copy()
        test_parameters['comparison_x'] = -2
        mocked_open = mock.mock_open(read_data=json.dumps(test_parameters))
        with mock.patch('builtins.open', mocked_open):
            with pytest.raises(InvalidShapeException):
                InputParser('dummy_file_path')
