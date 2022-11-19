import json
import os.path
from photomosaic.exceptions import InvalidShapeException


class InputParser(object):
    """
    An object that represents the input to set up a photomosaic.

    Attributes:
        photomosaic_folder: The folder that will be generated to contain all files related to this photomosaic
        target_image: The path of the file containing the target image
        candidate_image_folder: The folder that contains the candidate images to be used in the photomosaic
        grid_shape: A tuple giving the x,y size of the grid of images
        output_shape: A tuple giving the x,y size of each of the candidate images
        comparison_shape: A tuple giving the x,y size of each of the comparison images

    Methods:
        parse: Generate the folder structure and populate the candidate and output image folders
    """

    def __init__(self, parameters_json: str):
        """
        Construct an InputParser to parse the inputs for a photomosaic and create the necessary files and folders.

        :param parameters_json: A string giving the path to a json file that contains the parameters for the photomosaic
        """
        with open(parameters_json, 'r') as parameters_file:
            parameters = json.loads(parameters_file.read())
        # We test that the photomosaic folder does not exist
        if os.path.isdir(parameters['photomosaic_folder']):
            raise FileExistsError
        self.photomosaic_folder = parameters['photomosaic_folder']
        # We check that the target image and the folder of candidate images exist
        if not os.path.isfile(parameters['target_image']):
            raise FileNotFoundError
        self.target_image = parameters['target_image']
        if not os.path.isdir(parameters['candidate_image_folder']):
            raise FileNotFoundError
        self.candidate_image_folder = parameters['candidate_image_folder']
        # We test that each of the grid, output and comparison shapes are positive integers
        try:
            self.grid_shape = (int(parameters['grid_x']), int(parameters['grid_y']))
            self.output_shape = (int(parameters['output_x']), int(parameters['output_y']))
            self.comparison_shape = (int(parameters['comparison_x']), int(parameters['comparison_y']))
            if self.grid_shape != (parameters['grid_x'], parameters['grid_y']) or \
               self.output_shape != (parameters['output_x'], parameters['output_y']) or \
               self.comparison_shape != (parameters['comparison_x'], parameters['comparison_y']):
                raise InvalidShapeException
        except ValueError:
            raise InvalidShapeException
        if self.grid_shape[0] < 1 or self.grid_shape[1] < 1 or self.output_shape[0] < 1 or self.output_shape[1] < 1 or self.comparison_shape[0] < 1 or self.comparison_shape[1] < 1:
            raise InvalidShapeException
    def parse(self):
        raise NotImplementedError
