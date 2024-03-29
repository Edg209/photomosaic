import argparse
import os

from parse import InputParser
from image_distance import CandidateImageDistanceGrid
from output_layout import OutputLayout
from output_image import OutputImage

import skimage.io as si

import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', level=logging.INFO)


class Photomosaic(object):
    """
    An object that represents a main.

    Attributes:
        parameters_json_path: A string that gives the path to the JSON file containing the paramters of the main
        input_parser: A main.parse.InputParser generated by the JSON of parameters
        photomosaic_folder: The working folder that will be used for the generation of the main
        comparison_candidate_images: A dict that takes as key the name of a comparison candidate image and as values a np.ndarray containing the contents of that image
        comparison_target_images: A dict that takes as key the name of a comparison target image and as values a np.ndarray containing the contents of that image
        output_candidate_images: A dict that takes as key the name of an output candidate image and as values a np.ndarray containing the contents of that image
        image_distance_grids: A dict that takes as key the name of a comparison candidate image and as values a CandidateImageDistanceGrid of that candidate image
        output_layouts: A dict that takes as key the name of a comparison candidate image and as values an OutputLayout of the optimal outputs as of that candidate image being processed
        output_images: A dict that takes as key the name of a comparison candidate image and as values an OutputImage of the optimal main as of that candidate image being processed

    Methods:
        generate: Populate each of the attributes and generate the main
    """

    def __init__(self, parameters_json_path: str):
        """
        Create a main object.

        For more details, see https://github.com/Edg209/photomosaic.

        :param parameters_json_path: Path to the JSON file containing the parameters. For more details see https://github.com/Edg209/photomosaic/blob/main/overview.md.
        """
        self.parameters_json_path = parameters_json_path
        self.input_parser = None
        self.photomosaic_folder = None
        self.comparison_candidate_images = None
        self.comparison_target_images = None
        self.output_candidate_images = None
        self.image_distance_grids = {}
        self.output_layouts = {}
        self.output_images = {}

    def generate(self):
        # We start by parsing the input
        logging.info('Starting parsing')
        self.input_parser = InputParser(self.parameters_json_path)
        self.input_parser.parse()
        self.photomosaic_folder = self.input_parser.photomosaic_folder
        # We read each of the images using imread
        logging.info('Starting image reading')
        comparison_candidate_images_folder = os.path.join(self.photomosaic_folder, 'comparison_candidate_images')
        comparison_target_images_folder = os.path.join(self.photomosaic_folder, 'comparison_target_images')
        output_candidate_images_folder = os.path.join(self.photomosaic_folder, 'output_candidate_images')
        self.comparison_candidate_images = {imgname: si.imread(os.path.join(comparison_candidate_images_folder, imgname)) for imgname in os.listdir(comparison_candidate_images_folder)}
        self.comparison_target_images = {imgname: si.imread(os.path.join(comparison_target_images_folder, imgname)) for imgname in os.listdir(comparison_target_images_folder)}
        self.output_candidate_images = {imgname: si.imread(os.path.join(output_candidate_images_folder, imgname)) for imgname in os.listdir(output_candidate_images_folder)}
        # We iterate over each of the candidate images to update our main based on that image
        logging.info(f'Starting loop over candidate images, f{len(self.comparison_target_images)} items to loop over')
        for imgname in sorted(self.comparison_candidate_images.keys()):
            logging.info(f'[{imgname}] Starting iteration')
            # We calculate the image distance grid for that candidate image, update the output layout, and generate an output image
            logging.info(f'[{imgname}] Calculating image distance grid')
            self.image_distance_grids[imgname] = CandidateImageDistanceGrid(self.comparison_candidate_images[imgname], self.input_parser.target_image_grid)
            self.image_distance_grids[imgname].calculate()
            self.image_distance_grids[imgname].output_to_csv(os.path.join(self.photomosaic_folder, 'image_distances', imgname + '.csv'))
            logging.info(f'[{imgname}] Calculating optimal output layout')
            self.output_layouts[imgname] = OutputLayout(self.image_distance_grids)
            self.output_layouts[imgname].calculate()
            self.output_layouts[imgname].output_to_csv(os.path.join(self.photomosaic_folder, 'output_layouts', imgname + '.csv'))
            logging.info(f'[{imgname}] Generating output image')
            self.output_images[imgname] = OutputImage(self.output_layouts[imgname].image_grid, os.path.join(self.photomosaic_folder, 'output_candidate_images'))
            self.output_images[imgname].assemble()
            self.output_images[imgname].output_to_png(os.path.join(self.photomosaic_folder, 'output_images', imgname))


def main(parameters_json_path: str):
    photomosaic = Photomosaic(parameters_json_path)
    photomosaic.generate()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Photomosaic generator. For more details, see https://github.com/Edg209/photomosaic.')
    arg_parser.add_argument('parameters_json_path', help='Path to a JSON file of parameters. For more details, see https://github.com/Edg209/photomosaic/blob/main/overview.md.')
    args = arg_parser.parse_args()
    main(args.parameters_json_path)
