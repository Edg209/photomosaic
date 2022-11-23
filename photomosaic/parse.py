import json
import os.path
import shutil

from photomosaic.exceptions import InvalidShapeException
import skimage.io as si
import skimage.transform as st


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
        self._create_directories()
        self._resize_images()

    def _create_directories(self):
        os.mkdir(self.photomosaic_folder)
        os.mkdir(os.path.join(self.photomosaic_folder, 'comparison_candidate_images'))
        os.mkdir(os.path.join(self.photomosaic_folder, 'comparison_target_images'))
        os.mkdir(os.path.join(self.photomosaic_folder, 'output_candidate_images'))
        os.mkdir(os.path.join(self.photomosaic_folder, 'output_layouts'))
        os.mkdir(os.path.join(self.photomosaic_folder, 'output_images'))
        shutil.copyfile(self.target_image, os.path.join(self.photomosaic_folder, 'target_image.png'))

    def _resize_images(self):
        original_target_image = si.imread(self.target_image)
        candidate_image_names = {image_name for image_name in os.listdir(self.candidate_image_folder) if image_name.lower().endswith('.png')}
        # For each candidate image, it is resized and saved twice - once as a comparison image and once as an output image
        for candidate_image_name in candidate_image_names:
            candidate_image = si.imread(os.path.join(self.candidate_image_folder), candidate_image_name)
            comparison_image = st.resize(candidate_image, self.comparison_shape)
            output_image = st.resize(candidate_image, self.output_shape)
            si.imsave(os.path.join(self.photomosaic_folder, 'comparison_candidate_images', candidate_image_name), comparison_image)
            si.imsave(os.path.join(self.photomosaic_folder, 'output_candidate_images', candidate_image_name), output_image)
